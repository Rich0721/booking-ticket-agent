---
description: "這個檔案是專案的爬蟲開發指令，請依照指令進行開發"
applyTo: "crawler/**/*.py"
---

# 爬蟲開發指令

爬蟲程式開發除了根據需求文件與共通指令進行開發外，還需要依照以下指令進行開發，請依照指令進行開發。

## 1. 技術說明

- Programming Language: Python3.14
- Database: PostgreSQL(Version 17)

## 2. 爬蟲資料夾結構

```text
booking-ticket-agent/
├── crawler/
│ ├── main.py
│ ├── src/
| | ├── utils/ # 工具函式
| | ├── objects/
| | | ├── classes/
| | | | └── CUserInfo.py # 使用者資訊類別
| | | ├── enums/
| | | | └── EUserPermission.py
| | | └── abstracts/
| ├── tests/ # 單元測試程式碼
| | ├── scenarios/ # 測試情境檔案
| | ├── utils/
| | | └── test_connection_db.py # 測試連線資料庫功能
| ├── requirements.txt # 套件需求檔
| ├── Dockerfile # Docker設定檔
| └── .dockerignore # Docker忽略檔
```

## 3. 程式碼開發規範

- 類別(Class)使用大寫駝峰，檔案第一個字與命名方式固定為C，並分別放在objects/classes，例如:CUserInfo.py
- 枚舉(Enum)，檔案第一個字與命名方式固定為E，並且在資料放在objects/enums，例如EUserPermission.py
- 抽象類別使用大寫駝峰，檔案第一個字與命名方式固定為A，並放在objects/classes/abstracts，例如AUserInfo.py
- **類別**、**Enum**與**抽象類別**檔案不可以有其他類別或函式，若有其他類別或函式，請另外建立檔案
- 功能說明請簡單敘述在功能最上層即可，不需要撰寫過多的註解
- 類別變數或方法屬性是私有使用[__<variable_name>]表示，保護屬性使用[_<variable_name>]
- 變數命名須使用Snake Case，例如: user_info
- 常數命名使用Screaming Case，例如: TURN_OFF = 0
- 功能撰寫需要定義放入的型態與回傳型態，除非回傳為none，例如:def test(string:str, numbers:int)-> class:
- 未詳盡說明請根據**Google Python Style Guide**撰寫

## 4. Unit Test說明

- 單元測試檔案需放在tests資料夾中，並以test\_開頭命名，例如:test_connection_db.py
- 測試功能命名根據測試屬性定義
  - test[_<function_name>_<情境名稱>]
- 測試情境需透過scenarios資料夾中的檔案定義，並且在測試程式碼中註解來源，以利追蹤需求來源與維護
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
