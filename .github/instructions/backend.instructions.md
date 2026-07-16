---
description: "這個檔案是專案的後端開發指令，請依照指令進行開發"
applyTo: "backend/**/*.py"
---

# 後端開發指令

後端程式開發除了根據需求文件與共通指令進行開發外，還需要依照以下指令進行開發，請依照指令進行開發。

## 1. 技術說明

- Programming Language: Python3.14
- Framework: FastApi
- Database: PostgreSQL(Version 17)

## 2. 後端資料夾結構

請根據此架構進行後端程式碼撰寫，且請依照此架構撰寫對應的單元測試。

## 3. 程式碼開發風格

- API分層架構使用MVC(Model-View-Controller)架構
- 類別(Class)使用大寫駝峰，檔案第一個字與命名方式固定為C，並分別放在objects/classes，例如:CUserInfo.py
- 枚舉(Enum)，檔案第一個字與命名方式固定為E，並且在資料放在objects/enums，例如EUserPermission.py
- 抽象類別使用大寫駝峰，檔案第一個字與命名方式固定為A，並放在objects/classes/abstracts，例如AUserInfo.py
- 功能說明請簡單敘述在功能最上層即可，不需要撰寫過多的註解
- 類別變數或方法屬性是私有使用[__<variable_name>]表示，保護屬性使用[_<variable_name>]
- 變數命名須使用Snake Case，例如: user_info
- 常數命名使用Screaming Case，例如: TURN_OFF = 0
- 功能撰寫需要定義放入的型態與回傳型態，除非回傳為none，例如:def test(string:str, numbers:int)-> class:
- 未詳盡說明請根據**Google Python Style Guide**

## 4. Unit Test說明

- Unit Test測試**services**與**utils**為主
- 檔案命名需要區分，不要把不同功能的測試放在同一個檔案，例如不同serivce或不同util的測試需要分開撰寫，檔案命名方式如下:
  - services: test[_<service_name>].py
  - utils: test[_<util_name>].py
- 測試功能命名根據測試屬性定義
  - test[_<function_name>_<情境名稱>]
- 參考scenarios文件撰寫對應的測試情境，並在測試程式碼中註解來源，以利追蹤需求來源與維護
  - 當scenarios使用 Scenario Outline時，請撰寫單一測試情境，並使用pytest.mark.parametrize進行測試

  ```python
  @pytest.mark.parametrize(
      "booking_date",
      [
          date(2026, 7, 1),   # 當日
          date(2026, 6, 30),  # 過去日期
      ]
  )
  def test_booking_non_future_date_rejection(self, service, booking_date):
      """測試當日及過去日期不可預約"""

      system_date = datetime(2026, 7, 1)

      booking_info = CBookingTicketInfo(
          user_id=VALID_TEST_ID_1,
          ticket_type="THSR",
          booking_date=booking_date,
          booking_time="10:30",
          start_station="台北",
          end_station="左營",
          adults=1,
          childs=0,
          students=0,
          elders=0,
          disables=0,
          is_early_bird=False,
          is_member=False,
          early_ids=[]
      )

      with patch('src.services.BookingTicketService.validate_taiwan_id') as mock_validate:
          mock_validate.return_value = True

          success, message = service.process_booking(booking_info, system_date)

          assert not success
          assert "不接受當天或過去的預約訂票" in message
  ```

## 5. 後端資料夾結構

booking-ticket-agent/
├── backend/ # 後端程式碼
| ├── requirements.txt # 套件需求檔
| ├── Dockerfile # Docker設定檔
| ├── .dockerignore # Docker忽略檔
| ├── src/ # 後端程式碼
| | ├── controllers/ # API 相關程式碼
| | ├── services/ # 服務程式碼
| | ├── repositories/ # 資料庫存取程式碼
| | ├── utils/ # 工具函式
| | ├── objects/
| | | ├── classes/
| | | | └── CUserInfo.py # 使用者資訊類別
| | | └── enums/
| | | └── EUserPermission.py # 使用者權限列舉
| | └── main.py # FastApi啟動程式碼
| └── tests/ # 單元測試程式碼
| └── scenarios # 單元測試單一情境，不同的測資
