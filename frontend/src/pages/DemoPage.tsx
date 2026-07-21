import React, { useState } from "react";
import IDNumberInput from "../components/IDNumberInput/IDNumberInput";
import "./demo-page.css";

/**
 * DemoPage - 展示 IDNumberInput Component 的頁面
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
      alert(`提交的身份證字號: ${inputValue}`);
    } else {
      alert("請輸入身份證字號");
    }
  };

  return (
    <div className="demo-page">
      <div className="demo-page__container">
        <h1 className="demo-page__title">身份證字號輸入 Component 展示</h1>

        <div className="demo-page__section">
          <h2 className="demo-page__subtitle">基本使用</h2>
          <div className="demo-page__component-wrapper">
            <IDNumberInput
              title="訂票者身份證字號"
              value={inputValue}
              onChange={handleChange}
              iconSrc="/icons/user.png"
            />
          </div>

          <button className="demo-page__button" onClick={handleSubmit}>
            提交
          </button>

          {submittedValue && (
            <div className="demo-page__result">
              <p>
                ✓ 已提交: <strong>{submittedValue}</strong>
              </p>
            </div>
          )}
        </div>

        <div className="demo-page__section">
          <h2 className="demo-page__subtitle">測試案例</h2>
          <div className="demo-page__test-cases">
            <div className="demo-page__test-case">
              <p>
                <strong>有效的身份證字號：</strong>
              </p>
              <ul>
                <li>Z123456788</li>
                <li>A123456789</li>
                <li>B234567890</li>
              </ul>
            </div>
            <div className="demo-page__test-case">
              <p>
                <strong>無效的身份證字號：</strong>
              </p>
              <ul>
                <li>Z123456789 (驗證碼錯誤)</li>
                <li>1234567890 (無英文字首)</li>
                <li>Z1234567 (長度不足)</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="demo-page__section">
          <h2 className="demo-page__subtitle">功能說明</h2>
          <div className="demo-page__features">
            <ul>
              <li>✓ 支援 RWD (響應式設計)</li>
              <li>✓ 自動轉換為大寫</li>
              <li>✓ 即時驗證身份證字號格式</li>
              <li>✓ 失去焦點時顯示錯誤訊息</li>
              <li>✓ 支援自訂標題和最大長度</li>
              <li>✓ 支援 Icon 自訂</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DemoPage;
