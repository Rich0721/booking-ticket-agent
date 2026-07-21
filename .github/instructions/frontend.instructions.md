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

## 5. 需求文件說明

前端需求文件統一放在 `.github/Features/frontend/requirements` 資料夾下，請依照需求文件進行開發，並且撰寫對應的單元測試。
需求文件內容大綱:

- 需求簡介: 簡單介紹該需求所需要內容
- 需求說明: 詳細說明需求所需的功能與限制，可能包含使用情境，如果有撰寫使用情境，需要根據使用情境進行開發，並且撰寫對應的單元測試。
- 前端顯示畫面: 提供顯示畫面樣板，有可能有多種情境需要顯示不同的情境，請根據需求參考畫面進行開發。
- React範例說明: 根據**前端顯示畫面**由Figma設計時產生的簡單React範例程式，並沒有參考架構設計，因此需要根據整體前端架構進行調整。
- CSS範例說明: 根據**前端顯示畫面**由Figma設計時產生的簡單CSS範例程式，並沒有參考整體架構設計出共用的CSS，因此需要根據開發階段進行對應的CSS調整，減少重複性的CSS，提高可維護性，但若進行CSS調整時，除了Class引用的調整外，請勿調整其它React或Typescript的功能程式。

## 6. 後端資料夾結構

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
