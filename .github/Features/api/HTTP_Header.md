# Http Header

API進行前後端溝通時，都需要透過HTTP Header來傳遞一些必要的資訊，例如使用者身份驗證、請求格式、回應格式等。
因此為了確保後續可維護性與一致性，將HTTP Header的定義統一管理，並提供給前端與後端開發人員參考。

## Request Header定義

```json
{
  "Authorization": "Bearer <token>",
  "Content-Type": "application/json",
  "Accept": "application/json",
  "User-Agent": "Booking-Ticket-Agent/1.0"
}
```

## Response Header定義

```json
{
  "Content-Type": "application/json",
  "Cache-Control": "no-cache"
}
```
