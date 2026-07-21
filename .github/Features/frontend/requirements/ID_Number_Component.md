# 身份證字號輸入Component

## I. 需求簡介

實作一個可以提供使用者輸入台灣身份證的Component，並且提供ErrorMessage提示使用者輸入格式錯誤的訊息。

## II. 需求說明

- CSS需要有RWD功能
- 排版說明: [Icon] [Title] [Textbox]
- Icon:需置中放置，固定來源都是assert/images/icons
- Title: 預設為身份證字號，可提供開發者當作參數進行調整，並且固定置中
- Textbox
- Type: text
- Pattern: 台灣身份證編碼方式
- MaxLength: 10(提供調整)
- ErrorMessage: '身份證字號格式錯誤，請重新輸入'
- ErrorMessage顯示位置: Textbox下方
- ErrorMessage顯示條件: 當Textbox失去焦點，且輸入值不符合台灣身份證編碼方式時，顯示ErrorMessage
