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
- 錯誤原因:
- 完成開發:
- PM確認:

### Bug - Selection Component後端uri指定

- 分支名稱: bug_selection_component_backend_uri
- 需求說明: Selection Component使用的uri目前是呼叫**http://localhost:3000**，須調整成**http://localhost:8000**，並且後續可以透過env檔案進行設定
- 錯誤原因:
- 完成開發:
- PM確認:
