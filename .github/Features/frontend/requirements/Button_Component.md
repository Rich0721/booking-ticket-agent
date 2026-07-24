# 按鈕Componet

## I. 需求簡介
提供給開發者可以進行按鈕的操作，包含文字、icon、按鈕顏色、選取顏色、按鈕大小、點選之後要觸發的事件

## II. 需求說明
- CSS需要有RWD功能
- Props設定:
  - Title: 可提供開發者設定按鈕的Title文字
  - Icon: 可提供開發者放入不同的icon顯示
  - ButtonColor: 可提供開發者設定按鈕的顏色，預設為**#007bff**
  - SelectedColor: 可提供開發者設定按鈕被選取時的顏色，預設為**#0056b3**
  - ButtonSize: 可提供開發者設定按鈕的大小，預設為**medium**
    - small: 高度30px，字體大小12px
    - medium: 高度40px，字體大小14px
    - large: 高度50px，字體大小16px
  - OnClick事件:由外部放入需要的Function，當使用者點選按鈕時，會觸發OnClick事件
- 排版格式: [Icon] [Title]


## III. 前端顯示畫面

![Button Component](../UI/Commons/components/Button.png)

### IV. React範例說明

```jsx
import React from 'react';
import './Button.css';

function Button({ onClick }) {
  return (
    <button className="clear-button" onClick={onClick}>
      <img
        className="clear-button__icon"
        src="/eraser-icon.png"
        alt=""
      />
      <span className="clear-button__text">清空填寫</span>
    </button>
  );
}

export default Button;

```

### V. CSS範例說明

```css
.clear-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 13px;
  min-width: 217px;
  height: 61px;
  padding: 0 46px;
  background-color: #ffcccc;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}

.clear-button:hover {
  opacity: 0.85;
}

.clear-button:active {
  opacity: 0.7;
}

.clear-button__icon {
  width: 31px;
  height: 31px;
  flex-shrink: 0;
}

.clear-button__text {
  font-family: 'Kalam', cursive;
  font-size: 20px;
  font-weight: 400;
  color: #000000;
  line-height: normal;
  white-space: nowrap;
}
```