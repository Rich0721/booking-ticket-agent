Feature: 使用者在主頁面進行操作

  Rule: 使用者切換分頁
    Example: 使用者切換到THSR分頁
       Given 使用者在主頁面
         And 系統日為"2026/07/01"
        When 使用者移至"THSR"分頁
         And "THSR"字體顯示底線
        Then 系統顯示THSR訂票頁面
         And THSR字體為粗體
    
    Example: 使用者無法切換到THSR分頁
       Given 使用者在THSR頁面
         And 系統日為"2026/07/01"
        When 使用者移至"THSR"分頁
        Then "THSR"字體不顯示底線
    
    Example: 使用者回到主頁面
       Given 使用者在THSR頁面
         And 系統日為"2026/07/01"
        When 使用者點擊Header的"Auto Booking"字體
        Then 系統顯示主頁面