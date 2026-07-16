# Communication

此文件包含三個情境，讓AI Agent與使用者進行互動，避免需求不明確或需求不完整時，AI自行進行開發，造成錯誤情境。

### New Requirement 1

- 需求說明: 開發預約訂票功能
- 需求參考資料: [預約訂票](./requirements/Booking_Ticket.md)
- 完成開發: 2026-07-16
- PM確認:

### New Requirement 2

- 需求說明:
  - 將TestBookingTicketService與TestDateCalculator區分成不同檔案進行開發
  - 根據情境檔案減少測試程式碼，通過使用@pytest.mark.parametrize進行多種情境模擬
- 需求參考資料: [測試檔案](./requirements/Test_Booking_Ticket.md)
- 完成開發: 2026-07-16
- PM確認:

### Requirement - 實作BookingTicketRepository

- 分支名稱: feature_booking_ticket_repository
- 需求說明:
  - 將create_booking和create_early_bird方法進行實作，確保資料可以正確insert至資料庫中
  - 確認Unit Test可以Mock資料庫，並且測試可以通過
- 需求參考資料: [TB_BOOKING_TICKET](../../../database/tables/TB_BOOKING_TICKET.sql)、[TB_EARLY_BIRD](../../../database/tables/TB_EARLY_BIRD.sql)
- 完成開發: 2026-07-16
- PM確認:
