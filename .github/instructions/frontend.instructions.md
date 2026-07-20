---
description: "這個檔案是專案的前端開發指令，請依照指令進行開發"
applyTo: "frontend/**/*.ts, frontend/**/*.tsx"
---

# 前端該發指令

前端程式開發除了根據需求文件與共通指令進行開發外，還需要依照以下指令進行開發，請依照指令進行開發。

## 1. 技術說明

- Web Framework: React 18.2.0
- Programming Language: TypeScript 5.2.2

## 2. 前端資料夾結構

請根據此架構進行前端程式碼撰寫，且請依照此架構撰寫對應的單元測試。

## 3. 程式碼開發風格

- 使用 PascalCase 命名 React 元件檔案，如 `Dropdown.tsx`。
- 使用 camelCase 命名函式與變數。
- 使用 kebab-case 命名 CSS 檔案，如 `dropdown-menu.css`。
- components 資料夾下的元件應該是可重用的 UI 元件，並且應該有對應的測試檔案。
- layouts 資料夾下的元件應該是頁面佈局相關的元件，並且應該有對應的測試檔案。
- 所有元件都需要有Interface定義，並且應該放在 `interfaces` 資料夾中。
- function定義需要有明確的型別定義，並且應該使用 TypeScript 的型別系統來確保程式碼的正確性。

## 4. Unit Test說明

- 單元測試檔案應該與對應的元件檔案放在同一資料夾，並且命名為 `元件名稱.test.tsx`。

## 5. 後端資料夾結構

booking-ticket-agent/
├── frontend/ # 前端程式碼
| ├── node_modules/ # npm套件
| ├── public/ # 靜態資源
| ├── src/ # 前端程式碼
| | ├── assets/ # 靜態資源
| | | ├── images/ # 圖片資源
| | | ├── icons/ # 圖示資源
| | | └── styles/ # CSS資源
| | ├── components/ # 共用元件
| | | ├── Dropdown-menu/
| | | | ├── Dropdown.tsx
| | | | ├── Dropdown.css
| | | | └── Dropdown.test.tsx
| | ├── layouts/ # 版面配置
| | | ├── ThsrLayout.tsx
| | | └── ThsrLayout.test.tsx
| | ├── pages/ # 頁面元件
| | | ├── HomePage.tsx
| | | └── HomePage.test.tsx
| | ├── interfaces/ # TypeScript介面定義
| | ├── services/ # API服務
| | ├── utils/ # 工具函式
| | ├── App.tsx # 主程式
| | └── index.tsx # 入口程式
