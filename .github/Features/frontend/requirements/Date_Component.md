# 日期選擇器

## I. 需求簡介

提供使用者可以選擇日期，並期已'YYYY-MM-DD'格式回傳，而使用者無法選擇系統日與過去日。

## II. 需求說明

- CSS需要有RWD功能
- icon固定使用**public/icons/time-planning.png**
- Title: 預設為搭乘日期，可提供開發者當作參數
- Input Textbox:
  - 預設為空值
  - 選擇後顯示格式為**YYYY-MM-DD**
  - 不可選擇系統日以前(包含系統日)的日期
- ErrorMessage: '日期不可為空，請重新選擇'
- ErrorMessage顯示條件: 當Textbox失去焦點，且輸入值為空時，顯示ErrorMessage

### III. 前端顯示畫面

![UI設計圖](../UI/Commons/components/Date.png)

### IV. React範例說明

```jsx
// DatePicker.jsx
import React, { useState } from "react";
import "./DatePicker.css";

function DatePicker() {
  const [date, setDate] = useState("");

  return (
    <div className="date-picker">
      <img
        className="date-picker__icon"
        src="/icons/time-planning.png"
        alt="日曆"
      />
      <span className="date-picker__label">搭乘日期</span>
      <input
        type="date"
        className="date-picker__input"
        value={date}
        onChange={(e) => setDate(e.target.value)}
      />
    </div>
  );
}

export default DatePicker;
```

### V. CSS範例說明

```css
/* DatePicker.css */
.date-picker {
  position: relative;
  width: 400px;
  height: 50px;
  background: #ffffff;
  display: flex;
  align-items: center;
}

.date-picker__icon {
  width: 28px;
  height: 28px;
  margin-left: 10px;
}

.date-picker__label {
  font-family: "Kalam", cursive;
  font-weight: 700;
  font-size: 16px;
  color: #000000;
  margin-left: 23px;
}

.date-picker__input {
  width: 220px;
  height: 33px;
  margin-left: 42px;
  background: #d9d9d9;
  border: none;
  border-radius: 30px;
  padding: 0 16px;
  font-size: 14px;
  outline: none;
  appearance: none;
  -webkit-appearance: none;
}

.date-picker__input::-webkit-calendar-picker-indicator {
  cursor: pointer;
}
```
