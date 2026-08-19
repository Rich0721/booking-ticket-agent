# Communication

此文件包含三個情境，讓AI Agent與使用者進行互動，避免需求不明確或需求不完整時，AI自行進行開發，造成錯誤情境。

### Requirement - 實作共通元件

- 分支名稱: feature_ID_component
- 需求說明: 請根據**需求文件**說明完成實作該Component即可，其餘請不要實作，並且通過Pages顯示實作結果
- 需求參考資料: [需求文件](./requirements/ID_Number_Component.md)
- 完成開發: 2026-07-21
- PM確認:

### Requirement - 日期選擇器實作

- 分支名稱: feature_date_component
- 需求說明: 請根據**需求文件**說明完成實作該Component即可，其餘請不要實作，並且通過Pages顯示實作結果
- 需求參考資料: [需求文件](./requirements/Date_Component.md)
- 完成開發: 2026-07-21
- PM確認:

### Requirement - Checkbox實作

- 分支名稱: feature_checkbox_component
- 需求說明:
  - 請根據**需求文件**說明完成實作該Component即可，其餘請不要實作，並且通過Pages顯示實作結果
  - 調整: 點選Check box會有閃爍的情況，而且需要點兩次才會顯示打勾情況，請修正此問題
- 需求參考資料: [需求文件](./requirements/Checkbox_Component.md)
- 完成開發: 2026-07-22
- PM確認:

### Requirement - Ticket Number Component實作

- 分支名稱: feature_ticket_number_component
- 需求說明: 請根據**需求文件**說明完成實作該Component即可，其餘請不要實作，並且通過Pages顯示實作結果
- 需求參考資料: [需求文件](./requirements/Ticket_Number_Component.md)
- 完成開發: 2026-07-22
- PM確認:

### Requirement - Selection Compoenent實作

- 分支名稱: feature_selection_component
- 需求說明: 請根據**需求文件**說明完成實作該Component即可，其餘請不要實作，並且通過Pages顯示實作結果
- 需求參考資料: [需求文件](./requirements/Selection_Component.md)
- 完成開發: 2026-07-23
- PM確認:

### Requirement - Home Page 實作

- 分支名稱: feature_home_page
- 需求說明:
  - 請根據**需求文件**說明完成實作即可。
  - 確認後須調整: Header的**Auto Booking**需要置中在兩個顏色交界處，而非完全放在橘色區域
- 需求參考資料: [需求文件](./requirements/Home_Page.md)
- 完成開發: 2026-07-22
- PM確認:

### Requirement - Button Component 實作

- 分支名稱: feature_button_component
- 需求說明: 請根據**需求文件**說明完成實作該Component即可，其餘請不要實作，並且通過Pages顯示實作結果
- 需求參考資料: [需求文件](./requirements/Button_Component.md)
- 完成開發: 2026-07-24
- PM確認:

### Requirement - Hint Component 實作

- 分支名稱: feature_hint_component
- 需求說明: 請根據**需求文件**說明完成實作該Component即可，其餘請不要實作，於Pages測試方法**透過使用Button Component點擊後，顯示提示視窗進行測試確認**
- 需求參考資料: [需求文件](./requirements/Hint_Component.md)
- 完成開發: 2026-08-06
- PM確認:

### Requirement - Double Check Component 實作

- 分支名稱: feature_double_check_component
- 需求說明: 請根據**需求文件**說明完成實作該Component即可，其餘請不要實作，於Pages測試方法**透過使用Button Component點擊後，顯示提示視窗進行測試確認**
- 需求參考資料: [需求文件](./requirements/DoubleCheck_Compoent.md)
- 完成開發: 2026-08-06
- PM確認:

### Requirement - Booking THSR Page 實作

- 分支名稱: feature_booking_thsr_page
- 需求說明: 請根據**需求文件**說明完成實作，並讓使用者切換至"THSR"可以正常進行預約訂票
  - 請參考**HTML排版結構**重新完成高鐵預約訂票介面的設計
  - **Header**不須實作，請參考**Home Page**的Header，可透過Header切換至"THSR"頁面
  - 台灣圖片使用public/images/taiwan.png
  - **訂票者身份證字號**、**會員**與**早鳥**相關比例需統一，不能有大小不一的情況
  - **搭乘日期**、**搭乘時間**、**搭乘起站**與**搭乘迄站**相關Component大小需統一，不能有大小不一的情況
  - Button Component之間距離需置中顯示
- 需求參考資料: [需求文件](./requirements/Booking_THSR.md)
- 完成開發: 2026-08-14
- PM確認:

### Requirement - Refactor Component CSS

- 分支名稱: feature_refactor_booking_thsr_page
- 需求說明: 請根據下列說明完成Booking THSR Page的重構
  - 請先參考**Booking THSR Page**所使用的Component，確認跑版原因
  - 確認相關Component的字體大小、間距，需進行統一規格，不能有大小不一或間距不一的情況
  - 請調整對應至統一個CSS檔案內，除非有特殊要求，否則請不要在Component內自行調整CSS樣式
  - 僅可以調整CSS樣式，React架構、Typescript程式碼不可進行調整
- 需求文件: 請參考[Booking THSR Page](./requirements/Booking_THSR.md)所使用到的Component
- 完成開發: 2026-08-17
- PM確認:

### Bug - Selection Component多重載入及後端uri指定

- 分支名稱: bug_selection_component_multiple_load
- 需求說明: Selection Component於THSR頁面中，理論上只需要打三次後端API即可，但目前會出現6次，請確認原因並回填至**錯誤原因**
- 錯誤原因: **React 18 Strict Mode 的正常行為**。應用程式在 `index.tsx` 中啟用了 `React.StrictMode`，在開發環境會雙重執行 `useEffect` 來幫助檢測副作用問題。THSR頁面中有3個Selection Component（搭乘時間、搭乘起站、搭乘迄站），每個都在掛載時發起API調用。在Strict Mode下，每個Component的useEffect會被執行2次，導致 3 × 2 = 6次API調用。在生產環境中（沒有Strict Mode）會只有3次調用。此為預期行為，不是真正的bug。
- 完成開發: 2026-08-17
- PM確認:

### Bug - Selection Component後端uri指定

- 分支名稱: bug_selection_component_backend_uri
- 需求說明: Selection Component使用的uri目前是呼叫**http://localhost:3000**，須調整成**http://localhost:8000**，並且後續可以透過env檔案進行設定
- 錯誤原因:
- 完成開發: 2026-08-18
- PM確認:

### Bug - Button Component API URI指定

- 分支名稱: bug_button_component_backend_uri
- 需求說明: Button Component使用的uri目前是呼叫**http://localhost:3000**，須調整成**http://localhost:8000**，並且後續可以透過env檔案進行設定
- 錯誤原因:
- 完成開發: 2026-08-19
- PM確認:

### Bug - 未勾選早鳥時，會跳出早鳥輸入框

- 分支名稱: bug_early_bird_input_box
- 需求說明:
  - is_early_bird預設為False，當**早鳥**Checkbox勾選時，才能設定成True，並且跳出早鳥輸入框
  - 如果將**早鳥**Checkbox取消勾選，則is_early_bird需設定成False，並且清空早鳥輸入框
- 錯誤原因:
- 完成開發: 2026-08-19
- PM確認:

### Bug - 部位欄位未清空

- 分支名稱: bug_clear_input_fields
- 需求說明:
  - 點擊**清空填寫**後，所有欄位都需要清空
  - 點擊**確認預約**後，所有欄位都需要清空
- 錯誤原因:
- 完成開發: 2026-08-19
- PM確認:

### Bug - 二次確認視窗顯示有誤

- 分支名稱: bug_double_check_window
- 需求說明:
  - 起訖站別不能顯示Selection的value，而是要顯示Selection的label
  - 搭乘時間不能顯示Selection的value，而是要顯示Selection的label
- 錯誤原因:
- 完成開發:
- PM確認:
