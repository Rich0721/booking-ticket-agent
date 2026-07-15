# 刪除訂票功能

## I. 需求簡介

使用者會先進行查詢功能，若是尚未完成訂票的預約資訊，使用者在前端可以點擊按鈕移除預約資訊

## II. 流程圖

請參考[刪除預約訂票流程圖](../workflow/Delete_Booking.mmd)

## III. 需求說明

- 先於[TB_BOOKING_TICKET](../../../../database/tables/TB_BOOKING_TICKET.sql)查詢ID資訊
- 若`TICKET_NUMBER`為空則進行刪除，否則回傳錯誤訊息"該資料已完成訂票，無法進行刪除"

## IV. 其它說明

- API-Name: /delete-booking-ticket
- 共用定義定義由[非功能性需求](./Unfunctional.md)
- Method: Delete
- 刪除ID會從URI取得，Request Body僅有基本資訊
- - Response body
  1. staus code根據一般定義
  2. JSON Format
  ```JSON
      {
          "headers": {
            "message": "已成功刪除預約訂票資訊"
          },
          "info": {
              "ticket_type": "THSR",
              "booking_info": [
                {
                    "id": 1,
                    "booking_date": "2026-07-05",
                    "booking_time": "10:30",
                    "start_station": "台北",
                    "end_station": "左營",
                    "ticket_number": "A12345",
                    "canDelete": false
                },
                {
                    "id": 2,
                    "booking_date": "2026-08-30",
                    "booking_time": "10:30",
                    "start_station": "台北",
                    "end_station": "左營",
                    "ticket_number": "",
                    "canDelete": true
                }
              ]
          }
      }
  ```
