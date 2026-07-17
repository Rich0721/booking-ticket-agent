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

### Requirement - 修復Controller檔名錯誤以及資料庫連接設定

- 分支名稱: bug_fix_controller_and_db_connection
- 需求說明:
  - 修正Controller檔名錯誤，除了Unit test檔案，其餘檔案皆須以大寫駝峰定義檔名
  - Resporitory目前的DB_Session都是使用None，請進行實作
  - DB連線方法請使用os.getenv("KEY", default)，並且在../env/.env.dev和../env/.env.prod中設定對應的KEY
  - 確認所有Unit test可以Mock資料庫，並且測試可以通過
  - **升級需求**: 使用PostgreSQL為主，設計可擴展的資料庫架構，方便未來切換其他DB
- 需求參考: N/A
- 完成開發: 2026-07-16
- 實作細節:
  - 📊 **抽象層設計**
    - `DatabaseProvider` 抽象基類：定義統一的資料庫提供者接口
    - `PostgreSQLProvider`：PostgreSQL實現（主要）
    - `MySQLProvider`：MySQL實現（備用）
    - `DatabaseFactory`：工廠模式支持動態選擇和擴展
  - 🔄 **擴展機制**
    - 支持 `DatabaseFactory.register_provider('oracle', OracleProvider)` 輕鬆添加新資料庫
    - 無需修改現有代碼，只需通過環境變數 `DB_TYPE` 切換
    - 範例：`DB_TYPE=postgresql` 或 `DB_TYPE=mysql`
  - 🔧 **環境配置**
    - `.env.dev`：PostgreSQL本地開發配置（localhost:5432, postgres用戶）
    - `.env.prod`：PostgreSQL生產配置（db:5432, booking_user用戶）
    - 支持完整配置參數：DB_TYPE, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
  - ✅ **測試驗證**
    - 所有47個單元測試通過（無功能破壞）
    - 依賴注入模式正常工作
    - Mock數據庫層正常運作

- PM確認:
