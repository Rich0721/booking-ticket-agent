# BOOKING-TICKET-AGENT

這是練習透過設定Github Copilot的功能，包含共通與個別指令(Instruction)、Skill和Agent執行開發的預約訂票專案，主要目的是練習自己可以透過多個Agent、指令與技能達到自動化開發的目的。

- 0 -> 1: 透過Copilot指令與技能，讓Agent可以自動化開發專案
- 1 -> n: 透過Copilot指令與技能，讓Agent可以根據新需求進行自動化開發與維護

練習使用下列Agent完成預約訂票功能，預計完成目標如下:

- 設計共用Github Copilot指令、個別功能使用的指令，並設計對應的Agent，減少Token使用量
- 前端功能: 使用者可以選擇進行預約訂票類別(EX:台鐵或高鐵)、查詢預約與刪除預約的訂票功能
- 後端功能: 根據前端功能進行對應API設計
- 爬蟲功能：根據資料庫資料進行對應行為，透過排程自動化執行
- 資料庫：儲存站別資訊、預約資訊

### Github Copilot設計

- [x] 共用指令<br>
- [x] 前端相關指令、Agent與Skill<br>
- [x] 後端相關指令、Agent與Skill<br>
- [x] 爬蟲相關指令、Agent與Skill<br>
- [x] 前端需求設計<br>
- [x] 後端需求設計<br>
- [x] 爬蟲需求設計<br>


### 資料夾架構
```text
booking-ticket-agent/
├── .github/
|   ├── agents                       # Agent相關設定
|   ├── Feature        
|   |   ├── api                      # API需求，前後端共用
|   |   ├── backend                  # 後端需求
|   |   ├── crawler                  # 爬蟲需求
|   |   └── frontend                 # 前端需求
|   ├── instructions                 # 指令相關設定
|   ├── skills                       # 技能相關設定
|   └── copilot-instructions.md      # 專案說明
├── frontend/                        # 前端程式碼
├── backend/                         # 後端程式碼
├── crawler/                         # 爬蟲程式碼
├── database/                        # 資料庫相關
├── env/                             # 環境設定檔版本控制
└── README.md                        # 專案說明
```

### Github Copilot使用方式
1. 在**Feature**撰寫對應的需求
2. 將相關資訊於Feature中的communication.md中進行記錄需要開發的需求與分支名稱
3. 根據需求請不同的**Agent**進行開發
4. Agent協助開發與Push至對應分支
5. 開發完成後，進行Code Review與合併至主分支


### Docker

- Docker Build
    ```bash 
        docker compose build <service_name>
    ```

- Docker Up
    ```bash
        docker compose --env-file <env_file> up -d <service_name>
    ```

### 免責說明

此專案僅為研究 AI Agent 的 side project，若自行拿去<strong>營利或違反用途，請自行負法律責任</strong>。
