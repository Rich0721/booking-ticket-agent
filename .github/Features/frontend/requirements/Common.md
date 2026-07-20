# 共通功能

## I. 需求簡介
前端共同UI功能需求，通過jsx與css實現相同功能，減少重複開發，並且統一UI風格

## II. UI設計

### 2-1 身份證字號輸入Component
- UI設計圖: [身份證字號輸入](../UI/Commons/components/Common_ID.png)
- icon: [身份證字號輸入icon](../UI/Commons/icons/user.png)
- 需求說明:
    - CSS需要有RWD功能
    - icon需置中放置，此Component的icon固定
    - Textbox
        - Type: text
        - Pattern: 台灣身份證編碼方式
        - MaxLength: 10(提供調整)
        - 僅顯示前面5碼，後5碼顯示*，例如: A1234*****
    - ErrorMessage: '身份證字號格式錯誤，請重新輸入
    - ErrorMessage顯示位置: Textbox下方
    - ErrorMessage顯示條件: 當Textbox失去焦點，且輸入值不符合台灣身份證編碼方式時，顯示ErrorMessage

### 2-2 票數輸入Component
- UI設計圖: [票數輸入](../UI/Commons/components/Tickets.png)
- icon: [成人票](../UI/Commons/icons/people.png)、[兒童票](../UI/Commons/icons/children.png)、[敬老票](../UI/Commons/icons/elderly.png)、[愛心票](../UI/Commons/icons/disabled-person.png)、[學生票](../UI/Commons/icons/students.png)
- 需求說明:
    - CSS需要有RWD功能
    - icon需置中放置，可提供開發者放入不同的icon顯示
    - Textbox:
        - Type: number
        - Min: 0
        - Max: 10
    - ErrorMessage: '票數不可為0，且不可超過10張'
    - ErrorMessage顯示位置: Textbox下方
    - ErrorMessage顯示條件: 當Textbox失去焦點，且輸入值為0或大於10時，顯示ErrorMessage

### 2-3 單一選項Checkbox Component
- UI設計圖: [早鳥](../UI/Commons/components/Bird.png)
- icon: [早鳥](../UI/Commons/icons/bird.png)、[會員](../UI/Commons/icons/membership.png)
- 需求說明:
    - CSS需要有RWD功能
    - icon需置中放置，可提供開發者放入不同的icon顯示
    - Checkbox:
        - Type: checkbox
        - 可提供開發者設定checkbox的label文字
        - 可提供開發者設定checkbox的value值
        - defult: true(勾選，可提供開發者調整)


### 2-4 下拉選單Component
- UI設計圖: [搭乘日期](../UI/Commons/components/Time.png)
- icon: [搭乘日期](../UI/Commons/icons/time.png)、[站別](../UI/Commons/icons/transport.png)
- 需求說明:
    - CSS需要有RWD功能
    - icon需置中放置，可提供開發者放入不同的icon顯示
    - 下拉選單:
        - 固定使用API-**/loading-selected?parm_category={parm_category}**，拿回選單資料
        - **{parm_category}**- 提供給開發者設定，對應TB_SYS_PARM資料表的PARM_CATEGORY欄位
        - 回傳資料格式: [{ label: '選項文字', value: '選項值' }]
        - 僅需顯示label文字，value值提供給開發者使用
