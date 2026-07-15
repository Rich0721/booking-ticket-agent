---
description: "這個檔案是專案的後端開發指令，請依照指令進行開發"
applyTo: "backend/**/*.py"
---

# 後端開發指令

後端程式開發除了根據需求文件與共通指令進行開發外，還需要依照以下指令進行開發，請依照指令進行開發。

## 1. 技術說明

- Programming Language: Python3.14
- Framework: FastApi
- Database: PostgreSQL(Version 17)

## 2. 後端資料夾結構

請根據此架構進行後端程式碼撰寫，且請依照此架構撰寫對應的單元測試。

## 3. 程式碼開發風格

- 類別(Class)使用大寫駝峰，檔案第一個字與命名方式固定為C，並分別放在objects/classes，例如:CUserInfo.py
- 枚舉(Enum)，檔案第一個字與命名方式固定為E，並且在資料放在objects/enums，例如EUserPermission.py
- 抽象類別使用大寫駝峰，檔案第一個字與命名方式固定為A，並放在objects/classes/abstracts，例如AUserInfo.py
- 功能說明請簡單敘述在功能最上層即可，不需要撰寫過多的註解
- 類別變數或方法屬性是私有使用__表示，保護屬性使用_
- 變數命名須使用Snake Case，例如:use_info
- 常數命名使用Screaming Case，例如: TURN_OFF = 0
- 功能撰寫需要定義放入的型態與回傳型態，除非回傳為none，例如:def test(string:str, numbers:int)-> class:
- 未詳盡說明請根據**Google Python Style Guide**

## 4. 後端資料夾結構

booking-ticket-agent/
├── backend/ # 後端程式碼
| ├── requirements.txt # 套件需求檔
| ├── Dockerfile # Docker設定檔
| ├── .dockerignore # Docker忽略檔
| ├── src/ # 後端程式碼
| | ├── api/ # API 相關程式碼
| | ├── utils/ # 工具函式
| | ├── objects/
| | | ├── classes/
| | | | └── CUserInfo.py # 使用者資訊類別
| | | └── enums/
| | | └── EUserPermission.py # 使用者權限列舉
| | └── main.py # FastApi啟動程式碼
| └── tests/ # 單元測試程式碼
|    └── scenarios # 單元測試單一情境，不同的測資
