Feature 使用者訂票

    Rule 搭乘日為當日或過去
        Example 搭乘日為系統日
          Given 使用者在主頁面
            And 系統日為"2026/07/01"
           When 使用者輸入"2026/07/01"
           Then 系統顯示'請選擇未來日期進行預約'
    
        Example 搭乘日為過去日期
          Given 使用者在主頁面
            And 系統日為"2026/07/01"
           When 使用者輸入"2026/06/30"
           Then 系統顯示'請選擇未來日期進行預約'
    
    Rule 搭乘日為未來日

        Scenario Outline 搭乘日在系統日起29天內
          Given 使用者在主頁面
            And 系統日為"2026/07/01"
           When 使用者選擇"<Departure>"
           Then 系統顯示"2026/07/02"將完成訂票"
        
        Examples:
            | Departure  |
            | 2026/07/03 |
            | 2026/07/21 |
            | 2026/07/29 |

        Scenario Outline 搭乘日在系統日超過29天後，但搭乘日是星期一至星期五
          Given 使用者在主頁面
            And 系統日為"2026/07/01"
           When 使用者選擇"<Departure>"
           Then 系統顯示"<Booking>將完成訂票"
        
        Examples:
            | Departure      | Booking    |
            | 2026/08/03(一) | 2026/07/05 |
            | 2026/08/04(二) | 2026/07/06 |
            | 2026/08/05(三) | 2026/07/07 |
            | 2026/08/06(四) | 2026/07/08 |
            | 2026/08/07(五) | 2026/07/09 |
        
        Scenario Outline 搭乘日在系統日起29天後，但搭乘日是星期六或星期日
          Given 使用者在主頁面
            And 系統日為"2026/07/01"
           When 使用者選擇"<Departure>"
           Then 系統顯示"<Booking>將完成訂票"
        
        Examples:
            | Departure      | Booking    |
            | 2026/08/01(六) | 2026/07/03 |
            | 2026/08/09(日) | 2026/07/10 |