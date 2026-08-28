# Communication

此文件包含三個情境，讓AI Agent與使用者進行互動，避免需求不明確或需求不完整時，AI自行進行開發，造成錯誤情境。

### Requirement - 高鐵訂票爬蟲實作

- 分支名稱: feature_crawler_thsr
- 需求說明: 請根據**需求文件**說明完成實作該爬蟲功能
- 需求參考資料: [需求文件](./requirements/booking_thsr.md)
- 完成開發: 2026-08-24
- PM確認:


### Requirement - Driver卡住處理
- 分支名稱: feature_crawler_driver
- 需求說明: 目前整體流程已經確認無誤，但有點小問題需要處理，主要是有時候Driver會卡住，需要進行相應的處理
    - 如果卡住超過一定時間，則自動重啟Driver，並且該次操作資料加入Retry列表
    - 如果已經在Retry階段，則自動重啟，但該次操作仍然視為失敗，不再加入Retry列表，直接回填至Tabel
- 完成開發:
- PM確認:

### Requirement - Crawler Docker Compose 撰寫
- 分支名稱: feature_crawler_docker_compose
- 需求說明: 撰寫Crawler所需的Docker Compose配置，確保使用單一的Docker Compose文件即可啟動所有相關服務
    - 將DOCKER資訊填寫至[docker-compose.yaml](../../../docker-compose.yaml)
        - Service name: crawler-agent
        - image: crawler-agent:{APP_VERSION:latest}
        - container_name: crawler-agent-container
        - volumes:
            - /etc/localtime:/etc/localtime:ro
            - /etc/timezone:/etc/timezone:ro
        - environment: 請確認程式內所需要的環境變數
    - 相關環境變數直接回填至[env folder](../../../env)所有的環境變數文件
- 完成開發:
- PM確認:
