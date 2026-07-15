Feature: 使用者刪除訂票
    Rule: 系統應依使用者傳送ID刪除訂票資訊
        Example: 使用者刪除含有取票號碼的訂票資訊
            Given 使用者在查詢頁面
              And 系統日為"2026/07/01"
              And 系統存在以下訂票資料
                | Booking ID | Date             | Start Station | Departure Station | Booking Number |
                | 1          | 2026/07/04 22:00 | 左營          | 南港               | AD1321         |
                | 2          | 2026/08/10 22:00 | 左營          | 南港               |                | 
             When 使用者選擇刪除"THSR"
              And 輸入身份證字號"A123456789"
              And 選擇刪除Booking ID為"1"的訂票資訊
             Then 系統應回傳刪除失敗訊息
              And 系統應回傳以下訂票資料
                | Booking ID | Date             | Start Station | Departure Station | Booking Number | Can Delete |
                | 1          | 2026/07/04 22:00 | 左營          | 南港               | AD1321         | false      |
                | 2          | 2026/08/10 22:00 | 左營          | 南港               |                | true       |

        Example: 使用者刪除未含有取票號碼的訂票資訊
            Given 使用者在查詢頁面
              And 系統日為"2026/07/01"
              And 系統存在以下訂票資料
                | Booking ID | Date             | Start Station | Departure Station | Booking Number |
                | 1          | 2026/07/04 22:00 | 左營          | 南港               | AD1321         |
                | 2          | 2026/08/10 22:00 | 左營          | 南港               |                | 
             When 使用者選擇刪除"THSR"
              And 輸入身份證字號"A123456789"
              And 選擇刪除Booking ID為"2"的訂票資訊
             Then 系統應回傳刪除成功訊息
              And 系統應回傳以下訂票資料
                | Booking ID | Date             | Start Station | Departure Station | Booking Number | Can Delete |
                | 1          | 2026/07/04 22:00 | 左營          | 南港               | AD1321         | false      |