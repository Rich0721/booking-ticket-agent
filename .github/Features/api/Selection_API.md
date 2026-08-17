# Selection API

此文件主要是讓前端開發者可以透過此API拿取選單資料

## 電文基本定義

- API-Name: /loading-selected?parm_category={parm_category}
- Method: Get
- Request Header與Response Header請參考[HTTP Header](./HTTP_Header.md)

## Request Body

無

## Response Body

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
