import React, { useState } from "react";
import DatePicker from "../components/DatePicker/DatePicker";
import "./demo-page.css";

/**
 * DemoPage - 展示 DatePicker Component 的頁面
 */
const DemoPage: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [submittedValue, setSubmittedValue] = useState<string>("");

  const handleChange = (value: string) => {
    setInputValue(value);
  };

  const handleSubmit = () => {
    if (inputValue.trim() !== "") {
      setSubmittedValue(inputValue);
      alert(`提交的搭乘日期: ${inputValue}`);
    } else {
      alert("請選擇搭乘日期");
    }
  };

  return (
    <div className="demo-page">
      <div className="demo-page__container">
        <h1 className="demo-page__title">日期選擇器 Component 展示</h1>

        <div className="demo-page__section">
          <h2 className="demo-page__subtitle">基本使用</h2>
          <div className="demo-page__component-wrapper">
            <DatePicker
              title="搭乘日期"
              value={inputValue}
              onChange={handleChange}
            />
          </div>

          <button className="demo-page__button" onClick={handleSubmit}>
            提交
          </button>

          {submittedValue && (
            <div className="demo-page__result">
              <p>
                ✓ 已提交搭乘日期: <strong>{submittedValue}</strong>
              </p>
            </div>
          )}
        </div>

        <div className="demo-page__section">
          <h2 className="demo-page__subtitle">功能說明</h2>
          <div className="demo-page__features">
            <ul>
              <li>✓ 支援 RWD (響應式設計)</li>
              <li>✓ 顯示格式為 YYYY-MM-DD</li>
              <li>✓ 無法選擇系統日與過去日</li>
              <li>✓ 失去焦點且空值時顯示錯誤訊息</li>
              <li>✓ 標題可透過參數客製化</li>
              <li>✓ 使用固定 Icon: /icons/time-planning.png</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DemoPage;
