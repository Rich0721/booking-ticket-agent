# 高鐵自動訂票需求

## I. 需求簡介

查詢資料表[TB_BOOKING_TICKET](../../../../database/tables/TB_BOOKING_TICKET.sql)進行爬蟲預約訂票，並且將訂票結果存回資料表**TB_BOOKING_TICKET**

## II. 流程圖

## III. 需求說明

1. 查詢資料表[TB_BOOKING_TICKET](../../../../database/tables/TB_BOOKING_TICKET.sql)中**CAN_BOOKING_DATE**為當天的資料，並且根據**BOOKING_ID**排序
2. 計算當天需要訂票的資料數量，並以3的倍數進行分組，透過ThreadPoolExecutor進行多線程訂票，若當天不足3筆則以實際資料數量的線程數進行訂票
3. 啟動Driver進行模擬人為手動訂票的爬蟲功能，讀取
   1. 啟動Driver，並且連線至[高鐵訂票網站](https://irs.thsrc.com.tw)
   2. 如果遇到Cookie確認，需先點選**我同意**
   3. 根據訂票網頁填入對應的訂票資訊，請參考[Step-02](../html/thsr/Step-02.html)
      - 出發站: **START_STATION**
      - 到達站: **END_STATION**
      - 出發日期: **BOOKING_DATE**
      - 出發時間: **BOOKING_TIME**
      - 全票: **ADULT_COUNT**
      - 孩童票: **CHILD_COUNT**
      - 愛心票: **DISABLED_COUNT**
      - 敬老票: **ELDER_COUNT**
      - 大學生票: **STUDENT_COUNT**
   4. 驗證碼辨識透過**2Captcha**的normal進行辨識，將辨識結果回填至輸入框
      - API_KEY:使用os.getenv("CAPTCHA_API_KEY")取得
   5. 點選**開始查詢**
   6. 選擇對應的車次，並且點選**確認車次**，請參考[Step-03](../html/thsr/Step-03.html)
      - 如果IS_EARLY_BIRD為True，則需要確認**Search List**有沒有顯示**早鳥65折**、**早鳥85折**與**早鳥95折**，若有則點選對應的車次，若沒有則選擇與**BOOKING_TIME**最接近的車次為主
      - 如果IS_EARLY_BIRD為False，則選擇沒有顯示**早鳥65折**、**早鳥85折**與**早鳥95折**的車次，若都沒有則選擇與**BOOKING_TIME**最接近的車次為主
   7. 填入訂票人資訊，請參考[Step-04](../html/thsr/Step-04.html)
      - 取票識別碼: **USER_ID**
   8. 填入乘客資訊，請參考[Step-04](../html/thsr/Step-04.html)
      - 如果有IS_EARLY_BIRD為True，則需要填入早鳥票乘客資訊，相關資訊需要透過BOOKING_ID查詢[TB_EARLY_BIRD](../../../../database/tables/TB_EARLY_BIRD.sql)資料表，並且依照**EARLY_BIRD_ID**排序，將乘客資訊依序填入
   9. 填入高鐵會員資訊，請參考[Step-04](../html/thsr/Step-04.html)
      - 如果**IS_MEMBER**為True，則需選擇**高鐵會員 TGo 帳號**，並且輸入**USER_ID**
      - 如果**IS_MEMBER**為False，則不需要進行填寫
   10. 點選**完成訂票**，當訂票送出前會跳出**二次確認視窗**，需要點選送出
   11. 切換畫面前會跳出訂單確認訊息，請點選**關閉**
   12. 抓取**訂票代號**資訊，並且更新回資料表[TB_BOOKING_TICKET](../../../../database/tables/TB_BOOKING_TICKET.sql)的**TICKET_NUMBER**欄位。
4. 應適時使用Sleep()，避免被高鐵網站判定為機器人，導致訂票失敗
5. 如果訂票失敗則需要紀錄至訂票失敗的List，當所有訂票完成後，重新執行訂票流程，若還是失敗，則回填**TICKET_NUMBER**為**Booking Error**.

## IV. 參考程式碼

### 4-1 訂票流程程式碼

訂票流程可以參考以下程式碼，並且應該避免被高鐵網站判定為機器人，導致訂票失敗，請適時使用Sleep()，避免被高鐵網站判定為機器人，導致訂票失敗

```python

def get_edge()-> Edge:
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Edge(options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => false})'
    })
    return driver


def booking_one_way(**kwargs):

    driver = get_edge()
    driver.get(BOOKING_URL)
    driver.find_element(By.ID, 'cookieAccpetBtn').click()
    driver.find_element(By.ID, "BookingS1Form_selectStartStation").send_keys(kwargs.get('START_STATION'))
    driver.find_element(By.ID, "BookingS1Form_selectDestinationStation").send_keys(kwargs.get('DESTINATION_STATION'))

    input_element = driver.find_element(By.ID, "toTimeInputField")
    driver.execute_script(f"arguments[0]._flatpickr.setDate('{kwargs.get('DEPARTURE_DATE')}');", input_element)

    sleep(0.5)
    driver.find_element(By.NAME, "toTimeTable").send_keys(kwargs.get('DEPARTURE_TIME'))

    sleep(0.5)
    img_src = driver.find_element(By.ID, "BookingS1Form_homeCaptcha_passCode")
    img_src.screenshot("my_captcha.png")
    result = SOLVER.normal("my_captcha.png")
    driver.find_element(By.ID, "securityCode").send_keys(result['code'].upper())
    submit_btn = driver.find_element(By.ID, "SubmitButton")
    driver.execute_script("arguments[0].click();", submit_btn)
    os.remove("my_captcha.png")

    sleep(0.5)
    html = driver.page_source
    schedules = search_list(html)

    if not schedules:
        print("No schedules found.")
        driver.close()
        return

    booking_train = find_booking_train(schedules)
    radio_btn = driver.find_element(By.CSS_SELECTOR, f"input[querycode='{booking_train[TRAIN_NO_KEY]}']")

    # 強制執行點擊 (不經過瀏覽器點擊檢查)
    driver.execute_script("arguments[0].click();", radio_btn)

    submit_btn = driver.find_element(By.NAME, "SubmitButton")
    driver.execute_script("arguments[0].click();", submit_btn)

    driver.find_element(By.ID, "idNumber").send_keys(kwargs.get('ID_NUMBER'))
    if booking_train['EARLY_BIRD']:
        driver.find_element(By.ID, "BookingS3Form_TicketPassengerInfoInputPanel_passengerDataView_0_passengerDataView2_passengerDataIdNumber").send_keys(kwargs.get('ID_NUMBER'))

    radio_btn = driver.find_element(By.ID, 'memberSystemRadio1')
    driver.execute_script("arguments[0].click();", radio_btn)
    sleep(0.1)
    radio_btn = driver.find_element(By.ID, 'memberShipCheckBox')
    driver.execute_script("arguments[0].click();", radio_btn)
    sleep(0.1)
    radio_btn = driver.find_element(By.NAME, 'agree')
    driver.execute_script("arguments[0].click();", radio_btn)
    sleep(0.1)
    submit_btn = driver.find_element(By.ID, "isSubmit")
    driver.execute_script("arguments[0].click();", submit_btn)

    # 後續要防止錯誤，id=feedMSG
    sleep(0.5)
    submit_btn = driver.find_element(By.NAME, "SubmitButton")
    driver.execute_script("arguments[0].click();", submit_btn)

    close_btn = driver.find_element(By.CSS_SELECTOR, "input[value='關閉']")
    driver.execute_script("arguments[0].click();", close_btn)

    pnr_element = driver.find_element(By.CSS_SELECTOR, ".pnr-code span").
    driver.close()
    return pnr_element
```

### 4-2 整合車次查詢

```python
def search_list(html: str):

    try:
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find(id="BookingS2Form_TrainQueryDataViewPanel")

        '''
        <div class="result-listing">
            <span>
                <label class="uk-flex uk-flex-middle result-item active" style="font-weight: normal;">
                    <div class="btn-radio" style="height: 6px;">
                        <input queryarrival="07:30" querydeparturedate="07/22" querycode="803" name="TrainQueryDataViewPanel:TrainGroup" querydeparture="06:26" checked="true" queryestimatedtime="1:04" type="radio" class="uk-radio" value="radio22">
                    </div>
                    <div class="mobile-wrapper">
                        <div class="uk-flex uk-flex-middle mobile-top">
                            <div>
                                <p class="departure-time">
                                    <span id="QueryDeparture">06:26</span>
                                    <span style="display: none;" id="QueryDepartureDate">07/22</span>
                                </p>
                            </div>
                            <div class="uk-position-relative uk-flex uk-flex-middle">
                                <span class="icon-direction material-icons">arrow_right_alt</span>
                            </div>
                            <div>
                                <p class="arrival-time"><span id="QueryArrival">07:30</span></p>
                            </div>
                        </div>
                        <div class="uk-flex uk-flex-middle mobile-bottom">
                            <div class="duration">
                                <span class="material-icons">schedule</span><span>1:04</span>
                                <span class="divider">｜</span>
                                <span class="material-icons-outlined">directions_railway</span><span id="QueryCode">803</span>
                            </div>
                            <div class="discount uk-flex">
                            </div>
                        </div>
                    </div>
                </label>
            </span>
        </div>
        '''
        schedules = table.find('div', class_="result-listing")

        train_schedules = []
        for s in schedules:
            if type(s) != bs4.element.Tag:
                continue

            train_radios_data = s.find('input', class_='uk-radio')
            early_bird = s.find('p', class_='type early-bird').getText() if s.find('p', class_='type early-bird') else ''
            dict_data = {
                DEPARTURE_DATE_KEY: train_radios_data.get(DEPARTURE_DATE_KEY),
                DEPARTURE_TIME_KEY: train_radios_data.get(DEPARTURE_TIME_KEY),
                ARRIVAL_TIME_KEY: train_radios_data.get(ARRIVAL_TIME_KEY),
                TRAIN_NO_KEY: train_radios_data.get(TRAIN_NO_KEY),
                ESTIMATED_TIME_KEY: train_radios_data.get(ESTIMATED_TIME_KEY),
                'EARLY_BIRD': early_bird
            }

            train_schedules.append(dict_data)
        return train_schedules
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []

```

### 4-3 優先訂票等級

```python

def find_booking_train(schedules:list) -> str:

    priority = {'早鳥65折': 1, '早鳥8折': 2, '早鳥9折': 3}

    def get_sort_key(s):
        bird_weight = priority.get(s['EARLY_BIRD'], 4)

        # 2. 取得車程分鐘數
        time_minutes = transfer_estimated_time_to_minutes(s[ESTIMATED_TIME_KEY])

        # 回傳一個 Tuple：(優惠優先級, 車程時間)
        return (bird_weight, time_minutes)

    # 直接找出最佳車次
    best_train = min(schedules, key=get_sort_key)

    return best_train

```
