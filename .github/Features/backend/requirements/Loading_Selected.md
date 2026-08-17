# 載入選單內容

## I. 需求簡介

前端開發者會呼叫此API，並且透過**parm_category**參數傳遞需要查詢選內的條件，此API需至[Table](../../../../database/tables/TB_SYS_PARM.sql)進行查詢並回傳相關選項給前端。

## II. 流程圖

N/A

## III. 需求說明

- 前端會透過GET方式呼叫此API，並且透過**parm_category**參數傳遞需要查詢選內的條件
- 固定查詢[Table](../../../../database/tables/TB_SYS_PARM.sql)內的**parm_category**欄位，並且回傳相關選項給前端

## IV. 其它說明

- API定義請參考[Selection API](../../api/Selection_API.md)
- 共用定義由[非功能性需求](./Unfunctional.md)
