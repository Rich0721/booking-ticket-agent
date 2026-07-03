# 後端開發指令

## 技術
- 前端開發技術: React18 + TypeScript + TailwindCSS
- 後端開發技術: Python3.14 + FastApi
- 爬蟲開發技術: Python3.14 + Selenium
- 資料庫: PostgreSQL(Version 17)

## 程式碼風格
- 類別(Class)使用大寫駝峰，檔案第一個字與命名方式固定為C，並分別放在objects/classes，例如:CUserInfo.py
- 枚舉(Enum)，檔案第一個字與命名方式固定為E，並且在資料放在objects/enums，例如EUserPermission.py
- 抽象類別使用大寫駝峰，檔案第一個字與命名方式固定為A，並放在objects/classes/abstracts，例如AUserInfo.py
- 類別變數或方法屬性是私有使用__表示，保護屬性使用_
- 變數命名須使用Snake Case，例如:use_info
- 常數命名使用Screaming Case，例如: TURN_OFF = 0
- 功能撰寫需要定義放入的型態與回傳型態，除非回傳為none，例如:def test(string:str, numbers:int)-> class:
- 功能說明請簡單敘述在功能最上層即可，不需要撰寫過多的註解

## Docker撰寫
- 各功能的Dockerfile撰寫需要依照專案需求撰寫，不需要額外撰寫到最外層的docker-compose.yml
- 各功能的.dockerignore撰寫需要依照專案需求撰寫
- 再未提出需要撰寫docker-compose.yml的需求前提下，請勿撰寫docker-compose.yml

## Unit test
- 每個功能都需要寫單元測試


## 專案架構
THSR
├── .github/ # GitHub相關設定
|   ├── agnets/ # GitHub Agents設定
|   ├── Features # 專案需求功能說明
|   ├── instructions/ # 專案開發指令
|   ├── skills/ # 專案開發技能說明
|   └── copilot-instructions.md # Copilot共用指令
|
├── database/
|   ├── tables/ # 資料表 SQL 定義
|   └── ddl/ # 資料表初始化 SQL 定義
|
├── backend/ # 後端程式碼
|   ├── requirements.txt # 套件需求檔
|   ├── Dockerfile # Docker設定檔
|   ├── .dockerignore # Docker忽略檔
|   |
|   ├── src/ # 後端程式碼
|   │   ├── api/ # API 相關程式碼
|   │   ├── utils/ # 工具函式
|   │   ├── objects/
|   │   │   ├── classes/
|   │   │   │   └── UserInfo.py # 使用者資訊類別
|   │   │   └── enums/
|   │   │       └── EUserPermission.py # 使用者權限列舉
|   │   └── main.py # 專案進入點
|   ├── tests/ # 單元測試程式碼
|
├── frontend/ # 前端程式碼
|   ├── package.json # 套件需求檔
|   ├── Dockerfile # Docker設定檔
|   ├── .dockerignore # Docker忽略檔
|   ├── src/ # 前端程式碼
|   │   ├── components/ # React元件
|   │   ├── pages/ # React頁面
|   │   └── App.tsx # React專案進入點
|   │   └── tests/ # 單元測試程式碼
|
├── crawler/ # 爬蟲程式碼
|  ├── requirements.txt # 套件需求檔
|  ├── Dockerfile # Docker設定檔
|  ├── .dockerignore # Docker忽略檔
|  ├── src/ # 爬蟲程式碼
|  |  ├── utils/ # 工具函式
|  |  ├── objects/
|  |  │   ├── classes/
|  |  │   │   └── CWebDriver.py # 爬蟲WebDriver類別
|  |  │   └── enums/
|  |  │       └── EWebDriverType.py # 爬蟲WebDriver類型列舉
|  |  └── main.py # 爬蟲專案進入點
|
├── env/ # 環境變數設定
|   |    ├── .env.dev # 開發環境變數設定
|   |    └── .env.prod # 產品環境變數設定
|
├── docker-compose.yml # Docker Compose設定檔
├── .gitignore # Git忽略檔
└── README.md # 專案說明文件


## Copilot指令
- 請根據專案架構與需求檔案進行程式碼撰寫，並遵循程式碼風格與專案架構
- 不需要額外生成已完成開發事項的markdown file
- 除非有特別的要求解釋，否則不需要生成無意義的說明，例如:我現在正在撰寫程式碼等回復，專心生成程式碼即可
