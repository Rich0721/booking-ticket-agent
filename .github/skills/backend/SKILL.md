# Backend Skills
---
name: Backend Skills
description: 模擬後端工程師根據需求檔案進行對應的功能開發，並完成對應的Unit Test，最後將程式碼提交至GitHub。
---

## Backend Skills
- 需求來源: [Backend Skills](../../Features/backend/)
- 需求分析文件: [Requirements](../../Features/backend/Features/)
- 工作流程文件: [Workflow](../../Features/backend/Workflow/)

### Step 1: 需求分析
閱讀需求分析文件的「需求簡介」與「需求說明」部分，了解需求的功能與限制。
#### 細項說明
- 請勿自行腦補需求，若有不清楚的地方請於需求來源路徑下生成"需求檔案_issus.md"(EX: Features/backend/issus/Features/Booking_issus.md)，並將不清楚的地方提出，等待PM回覆後再進行下一步，並生成表格提供給PM回覆，說明如下:
```markdown
   #### 需求不清楚的地方，請PM回覆
   - □ 需求不清楚的地方，請PM回覆
   | 需求段落 | 不清楚的地方 | PM回覆 |
   |  -------- | ------------ | ------- |
   | Request body | 早鳥票ID數量須與全票(Adults)相同，若不相同，請問要回傳什麼訊息? |  |

   #### 需求不清楚的地方，PM已回覆
   - ✅ 需求不清楚的地方，PM已回覆
   | 需求段落 | 不清楚的地方 | PM回覆 |
   | ------- | ------------ | ------- |
   | Response body | status code根據一般定義，請問要回傳什麼訊息? | 200: 成功, 400: 請求錯誤, 404: 查無資料, 500: 伺服器錯誤 |
```
- PM尚未回覆前，若不影響其他需求的開發，請先進行其他需求的開發，並將不清楚的地方記錄於"issus.md"檔案中，等待PM回覆後再進行下一步。
- 若PM回覆後，重新對issus.md與對應的需求檔案進行分析，並且進行開發，完成後將對應的issus.md內容進行調整後，提供給PM查核，若皆已完成，請將issus檔案移至"Features/backend/issus/Done"資料夾中，並將issus檔案重新命名為"需求檔案_issus_Done.md"(EX: Features/backend/issus/Done/Features/Booking_issus_Done.md)，說明如下:
```markdown
   #### 已完成需求撰寫
   - ✅ 需求不清楚的地方，PM已回覆
   | 需求段落 | 不清楚的地方 | PM回覆 | 已完成需求撰寫 |
   | -------- | ------------ | ------- | ---------------- |
   | Response body | status code根據一般定義，請問要回傳什麼訊息? | 200: 成功, 400: 請求錯誤, 404: 查無資料, 500: 伺服器錯誤 | '2026-06-14' |
```

### Step 2: 撰寫Unit Test
根據需求文件先行撰寫對應的Unit Test，確保程式碼符合需求。完成
#### 細項說明
- 撰寫Unit Test時，需模擬多種情境，確保程式碼能夠處理各種可能的輸入與狀況。
- 完成後，不調整Unit Test，除非需求文件有更新或發現Unit Test本身有錯誤。
- 確認該需求有沒有"需求文件_UT_issus.md"，PM回覆後，若有需要調整Unit Test，請先調整Unit Test，並重新執行Unit Test，直到所有需求都通過Unit Test。

### Step 3: 撰寫程式碼
根據需求文件與Unit Test撰寫對應的程式碼，確保程式碼符合需求並通過Unit Test，不可透過Unit Test作弊。
#### 細項說明
- 撰寫程式碼時，需確保程式碼符合需求文件的規範，並且能夠通過所有的Unit Test。
- 完成後，不調整程式碼，除非需求文件有更新或發現程式碼本身有錯誤。
- 確認該需求有沒有"需求文件_UT_issus.md"，PM回覆後，若有需要調整程式碼，請先調整程式碼，並重新執行Unit Test，直到所有需求都通過Unit Test。

### Step 4: 確認所有需求都有通過Unit Test
每次撰寫完對應需求後，確認所有需求都有通過Unit Test，確保程式碼符合需求
#### 細項說明
- 若有需求未通過Unit Test，請先檢查程式碼是否符合需求，若不符合需求請先修正程式碼，並重新執行Unit Test，直到所有需求都通過Unit Test。
- 如果超過三次修正仍無法通過Unit Test，於撰寫"需求文件_UT_issus.md"(EX: Features/backend/issus/UT_issus/Booking_UT_issus.md)請回報給PM，並提供以下資訊:
```markdown
   #### Unit Test無法通過，請PM回覆
   - □ Unit Test無法通過，請PM回覆
   | 程式碼檔名 | Function Name | Unit Test錯誤訊息 |PM回覆 |
   | ------------ | -------- | ----------------- | ----------- |
   | Booking_Ticket.py | booking_ticket | AssertionError: assert '2026/07/02將完成訂票，請記得查詢取票號碼' == '2026/07/03將完成訂票，請記得查詢取票號碼'  |
```

### Step 5: 提交程式碼至GitHub