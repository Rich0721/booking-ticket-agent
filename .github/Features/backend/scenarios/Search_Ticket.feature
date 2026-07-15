Feature: 使用者查詢訂票
    Rule: 系統應依查詢條件顯示使用者的訂票資料
        Scenario: 使用者有多筆預約資訊
          Given 使用者在查詢頁面
            And 系統日為"2026/07/01"
            And 系統存在以下訂票資料
            | Date             | Start Station | Departure Station | Booking Number |
            | 2026/07/04 22:00 | 左營          | 南港               | AD1321         | 
            | 2026/08/10 22:00 | 左營          | 南港               |                | 
           When 使用者選擇查詢"THSR"
            And 輸入身份證字號"A123456789"
           Then 系統應顯示以下訂票資料
            | Date             | Start Station | Departure Station  | Booking Number  | Can Delete |
            | 2026/07/04 22:00 | 左營          | 南港                | AD1321         | false       |
            | 2026/08/10 22:00 | 左營          | 南港                |                | true        |
        
        Example:使用者未有預約資訊
          Given 使用者在查詢頁面
            And 系統日為"2026/07/01"
            And 系統不存在身份證字號 "A123456789" 的訂票資料
           When 使用者選擇查詢"THSR"
            And 輸入身份證字號"A123456789"
           Then 系統不應顯示訂票資料列表
