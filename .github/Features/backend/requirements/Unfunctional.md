# 非功能性需求

此文件屬於非功能性需求

1. Request和Response固定格式

```JSON
{
    "headers":{
        // 非功能性需求須保證每一個Request都據以headers
        // status_code, user_agent
        // message放在此處，若無相關訊息則回傳空值
    },
    "info":{
        ... // key固定使用info，但內容根據需求有所調整
    }
}
```
2. 須避免被爬蟲攻擊
3. 與前端的Request和Response需要進行加密
