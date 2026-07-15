# 載入選單

## I. 需求簡介

使用者在前端選擇特定選單項目時，系統需要載入對應的選單資料，並回傳給前端顯示。

## II. 流程圖

N/A

## III. 需求說明

- 根據前端需求至單資料來源[TB_SYS_PARM](../../../../database/tables/TB_SYS_PARM.sql)進行查詢後，塞選條件為**PARM_CATEGORY**，將選單資料回傳給前端渲染

## IV. 其它說明

- API-Name: /loading-selected?parm_category={parm_category}
- 共用定義由[非功能性需求](./Unfunctional.md)
- Method: Get
- Request body: 無
- Response body
  1. status code 根據一般定義
  2. JSON Format
  ```JSON
      {
          "info": {
              "menu": [
                {
                    "id": 1,
                    "parm_name": "首頁",
                    "parm_value": "home"
                },
                {
                    "id": 2,
                    "parm_name": "訂票",
                    "parm_value": "booking"
                }
              ]
          }
      }
  ```
