# 預約訂票功能

## I. 需求簡介

前端傳入使用者預約訂票資訊，例如使用者想要預約尚未開放線上訂票的高鐵票，透過預約機制會在開放第一天由另外一個功能協助自動訂票

## II. 流程圖

請參考[預約訂票流程圖](../workflow/Booking_Tickets.mmd)

## III. 需求說明

- 訂票人ID與早鳥票ID共用同一個檢查方式，以台灣身份證編碼方法進行檢查
- 早鳥票ID數量須與全票(Adults)相同
- 預約訂票規則如下:
  1. 不接受當天的預約訂票，當天會回傳'當天不接受預約訂票'
  2. 預約日期如果在29天以內，系統日+1就可以開放使用者查詢，例如系統日為2026/7/1(三)，如果搭乘日2026/7/21(三)，則會回傳，'2026/07/02將完成訂票，請記得查詢取票號碼'
  3. 預約日期如果在29天以後且為週一到週六，請用搭乘時間往前算29天為完成訂票日期，例如系統日為2026/7/1(三)，訂票日期為2026/8/3(一)，則回傳'2026/07/05將完成訂票，請記得查詢取票號碼'
  4. 預約日期如果在29天以後且為週日，可提早至離29日最近的週五，例如系統日為2026/7/1(三)，訂票日期為2026/8/2(日)，則回傳'2026/07/03將完成訂票，請記得查詢取票號碼'
- 將預約訂票資訊新增至[TB_BOOKING_TICKET](../../../../database/tables/TB_BOOKING_TICKET.sql)
- 早鳥票乘坐者新增至[TB_EARLY_BIRD](../../../../database/tables/TB_EARLY_BIRD.sql)
- Gherkin情境說明請至[Feature](./Scenarios/Booking_Ticket.feature)

## IV. 其它說明

- 共用定義定義由[非功能性需求](./Unfunctional.md)
- Method: Post
- Request body

  ```JSON
      {
          "info": {
              "user_id": "A123456789",
              "ticket_type": "THSR",
              "booking_date": "2026-07-03",
              "booking_time": "10:30",
              "start_station": "台北",
              "end_station": "左營",
              "adults": 1,
              "childs": 0,
              "students": 0,
              "elders": 0,
              "disables": 0,
              "is_early_bird": true,
              "is_member": true,
              "early_ids": ["A123456789", "B123456789"]
          }

      }
  ```

- Response body
  1. staus code根據一般定義
  2. JSON Format
  ```JSON
      {
          "headers": {
              "message": "請根據需求回傳"
          }
      }
  ```
