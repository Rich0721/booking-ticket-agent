# THSR訂票上下行電文

此文件是用來說明高鐵訂票上下行電文的格式與內容，並提供給前端與後端開發人員參考。

## 電文基本定義

- API-Name: /booking-ticket
- Method: Post
- Request Header與Response Header請參考[HTTP Header](./HTTP_Header.md)

## Request Body

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

## Response Body

```JSON
      {
          "headers": {
              "message": "請根據需求回傳"
          }
      }
```
