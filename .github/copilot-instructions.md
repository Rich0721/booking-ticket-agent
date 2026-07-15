# Booking-Ticket-Agent開發共同指令

## 專案說明

請根據不同skill與Agnet閱讀不同的需求說明文件，並依照需求進行程式碼撰寫，請遵循程式碼風格與專案架構

## 需求文件閱讀

需求文件會根據前後端與爬蟲的不同需求進行拆分，相關文件都會放在.github/Features資料夾下，以下架構著重說明Features資料夾結構，並非完整資料夾結構，完整資料夾結構請參考-**專案資料夾結構**
.github
└── Features
| ├── backend # 後端需求文件
| | ├── requirements # 功能需求說明文件
| | ├── scenarios # 功能情境說明文件，須根據requirements引用參考
| | ├── workflows # 功能工作流程說明文件，須根據requirements引用參考
| | └── communication.md # 與AI Agent溝通的情境說明文件
| ├── frontend # 前端需求文件
| | ├── requirements # 功能需求說明文件
| | ├── scenarios # 功能情境說明文件，須根據requirements引用參考
| | ├── designs # 前端設計文件，須根據requirements引用參考
| | └── communication.md # 與AI Agent溝通的情境說明文件
| ├── crawler # 爬蟲需求文件
| | ├── requirements # 功能需求說明文件
| | ├── scenarios # 功能情境說明文件，須根據requirements引用參考
| | ├── workflows # 功能工作流程說明文件，須根據requirements引用參考
| | └── communication.md # 與AI Agent溝通的情境說明文件

### Requirements文件導讀

需求文件總共會分成四個部分，分別為需求簡介、流程圖、需求說明與其它說明，以下針對每個部分進行說明:

1. 需求簡介: 主要說明此功能的主要目的與功能，並不會針對細節進行說明
2. 流程圖: 流程圖參考[Mermaid](https://mermaid.js.org/)語法撰寫，並且會依照需求說明文件進行流程圖撰寫，請依照流程圖進行程式碼撰寫
3. 需求說明: 主要針對此功能的細節進行說明，相關情境與使用到的資料表都會在此說明，請依照需求說明進行程式碼撰寫
4. 其它說明: 主要針對此功能的其他說明，例如共用定義、Method、Request與Response說明，請依照需求說明進行程式碼撰寫
5. 非功能性需求: 都會參考各自的端點的非功能性需求定義

### Unit Test

無論前後端或爬蟲都需要撰寫單元測試，相關情境皆根據scenarios文件進行撰寫對應的單元測試
每個單元測試都需要註解來源，以利追蹤需求來源與維護

### 與PM溝通

communication.md文件是由PM與AI Agent進行溝通的文件，AI請保留前面的溝通紀錄，請勿自行刪除，並依照以下規則進行回覆:

- AI Agent: 在開發過程中遇到需求不明瞭或不完整情境時，根據**需求模糊**格式進行回覆，等待PM完成回覆再進行會影響的開發
- PM: 在後續開發完成後，PM會透過**新提出需求**格式進行回覆，AI Agent在收到回覆後，依照需求進行開發

#### 需求模糊

若需求有模糊或不清楚的地方，請勿自行補足，而是根據開發端點寫入對應的communication.md文件，後續透過參考communication.md進行後續開發，相關回應如下格式如下:

```Markdown
### Alignment
- 需求模糊或不清楚的地方: [請描述需求模糊或不清楚的地方]
- 需求確認: [由PM進行填寫]
- 完成開發: [空白代表未完成開發，若完成開發請填寫完成開發日期]
- PM確認: [由PM進行填寫]
```

### 新提出需求

由PM提出新需求或bug修復，開發完成僅會填寫完成開發欄位，請依照以下格式進行回覆:

```Markdown
### New Requirement
- 需求說明: [請描述新需求或bug修復]
- 需求參考資料: [請提供新需求或bug修復的參考資料]
- 完成開發: [空白代表未完成開發，若完成開發請填寫完成開發日期]
- PM確認: [由PM進行填寫]
```

## Docker撰寫

- 各功能的Dockerfile撰寫需要依照專案需求撰寫，不需要額外撰寫到最外層的docker-compose.yml
- 各功能的.dockerignore撰寫需要依照專案需求撰寫
- 再未提出需要撰寫docker-compose.yml的需求前提下，請勿撰寫docker-compose.yml

## Git分支

根據專案需求先從main pull最新的版本後，開出對應功能分支

- 需求分支: feature*[需求端點(backend/frontend/crawler/other)]*[功能名稱]
- Bug修復分支: bug*[需求端點(backend/frontend/crawler/other)]*[功能名稱]
  完成對應功能後，提出MR需求回到main分支，並依照專案需求進行程式碼審查與合併

## 專案資料夾結構

Booking-Ticket-Agent/
├── .github/ # GitHub Copilot與需求設定
| ├── agnets/ # GitHub Agents設定
| ├── Features # 專案需求功能說明
| ├── instructions/ # 專案開發指令
| ├── skills/ # 專案開發技能說明
| └── copilot-instructions.md # Copilot共用指令
|
├── database/
| ├── tables/ # 資料表 SQL 定義
| └── ddl/ # 資料表初始化 SQL 定義
|
├── backend/ # 後端程式碼
| ├── requirements.txt # 套件需求檔
| ├── Dockerfile # Docker設定檔
| ├── .dockerignore # Docker忽略檔
| |
| ├── src/ # 後端程式碼
| │ ├── api/ # API 相關程式碼
| │ ├── utils/ # 工具函式
| │ ├── objects/
| │ │ ├── classes/
| │ │ │ └── UserInfo.py # 使用者資訊類別
| │ │ └── enums/
| │ │ └── EUserPermission.py # 使用者權限列舉
| │ └── main.py # 專案進入點
| ├── tests/ # 單元測試程式碼
|
├── frontend/ # 前端程式碼
| ├── package.json # 套件需求檔
| ├── Dockerfile # Docker設定檔
| ├── .dockerignore # Docker忽略檔
| ├── src/ # 前端程式碼
| │ ├── components/ # React元件
| │ ├── pages/ # React頁面
| │ └── App.tsx # React專案進入點
| │ └── tests/ # 單元測試程式碼
|
├── crawler/ # 爬蟲程式碼
| ├── requirements.txt # 套件需求檔
| ├── Dockerfile # Docker設定檔
| ├── .dockerignore # Docker忽略檔
| ├── src/ # 爬蟲程式碼
| | ├── utils/ # 工具函式
| | ├── objects/
| | │ ├── classes/
| | │ │ └── CWebDriver.py # 爬蟲WebDriver類別
| | │ └── enums/
| | │ └── EWebDriverType.py # 爬蟲WebDriver類型列舉
| | └── main.py # 爬蟲專案進入點
|
├── env/ # 環境變數設定
| | ├── .env.dev # 開發環境變數設定
| | └── .env.prod # 產品環境變數設定
|
├── docker-compose.yml # Docker Compose設定檔
├── .gitignore # Git忽略檔
└── README.md # 專案說明文件

## Copilot指令

- 請根據專案架構與需求檔案進行程式碼撰寫，並遵循程式碼風格與專案架構
- 不需要額外生成已完成開發事項的markdown file
- 除非有特別的要求解釋，否則不需要生成無意義的說明，例如:我現在正在撰寫程式碼等回復，專心生成程式碼即可
