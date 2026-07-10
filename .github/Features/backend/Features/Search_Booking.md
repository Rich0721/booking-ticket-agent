# 查詢與刪除訂票功能

## I. 需求簡介

前端傳入使用者查詢訂票資訊，例如使用者想要查詢完成訂票的取票號碼，輸入訂票者ID，會查詢最新的訂購資訊；如果前端查詢完成後點選刪除，會協助刪除尚未預約的資訊

## II. 流程圖

請參考[查詢訂票流程圖](../workflow/Search_Booking.mmd)

## III. Request與Response說明

- 共用定義定義由[非功能性需求](./Unfunctional.md)
- Method: Post
- Request body

  ```JSON
      {
          "info": {
              "user_id": "A123456789",
              "ticket_type": "THSR",
          }
      }
  ```

- Response body
  1. staus code根據一般定義
  2. JSON Format
  ```JSON
      {
          "info": {
              "ticket_type": "THSR",
              "booking_info": [
                {
                    "id": 1,
                    "booking_date": "2026-07-05",
                    "booking_time": "10:30",
                    "start_station": "台北",
                    "end_station": "左營",
                    "ticket_number": "A12345"
                },
                {
                    "id": 2,
                    "booking_date": "2026-08-30",
                    "booking_time": "10:30",
                    "start_station": "台北",
                    "end_station": "左營",
                    "ticket_number": ""
                }
              ]
          }
      }
  ```

## IV. 需求說明

- 訂票人ID以台灣身份證編碼方法進行檢查
- 查詢T+1開始的預約資訊，如果沒有預約資訊回傳空陣列
- 查詢訂票資訊來源[TB_BOOKING_TICKET](../../../../database/tables/TB_BOOKING_TICKET.sql)
