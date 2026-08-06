import React, { useState } from "react";
import DatePicker from "../components/DatePicker/DatePicker";
import { Button, Hint, DoubleCheck, BookingInfo } from "../components";
import "./demo-page.css";

/**
 * DemoPage - 展示 DatePicker Component 的頁面
 */
const DemoPage: React.FC = () => {
  const [inputValue, setInputValue] = useState<string>("");
  const [submittedValue, setSubmittedValue] = useState<string>("");
  const [showInfoHint, setShowInfoHint] = useState<boolean>(false);
  const [showWarningHint, setShowWarningHint] = useState<boolean>(false);
  const [showDoubleCheck, setShowDoubleCheck] = useState<boolean>(false);

  const mockBookingInfo: BookingInfo[] = [
    { label: "訂票種類", value: "THSR", italic: true },
    { label: "身份證字號", value: "A123456789", italic: true },
    { label: "訂票邏輯", value: "早鳥優先" },
    { label: "是否使用會員累積點數", value: "是" },
    { label: "搭乘日期", value: "2026-07-17", italic: true },
    { label: "搭乘時間", value: "15:00", italic: true },
    { label: "搭乘起站", value: "南港" },
    { label: "搭乘迄站", value: "左營" },
    { label: "成人", value: "2" },
    { label: "愛心", value: "0" },
    { label: "敬老", value: "0" },
    { label: "孩童", value: "0" },
    { label: "大學生", value: "0" },
    { label: "早鳥", value: "A123456789, B234567890", italic: true },
  ];

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

  const handleShowInfoHint = () => {
    setShowInfoHint(true);
  };

  const handleShowWarningHint = () => {
    setShowWarningHint(true);
  };

  const handleShowDoubleCheck = () => {
    setShowDoubleCheck(true);
  };

  const handleCloseInfoHint = () => {
    setShowInfoHint(false);
  };

  const handleCloseWarningHint = () => {
    setShowWarningHint(false);
  };

  const handleCloseDoubleCheck = () => {
    setShowDoubleCheck(false);
  };

  const handleConfirmBooking = () => {
    alert("確認訂票已提交到後端");
    setShowDoubleCheck(false);
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

        <div className="demo-page__section">
          <h2 className="demo-page__subtitle">Hint Component 展示</h2>
          <div className="demo-page__hint-buttons">
            <Button
              title="顯示提示訊息"
              buttonColor="#007bff"
              selectedColor="#0056b3"
              buttonSize="medium"
              onClick={handleShowInfoHint}
            />
            <Button
              title="顯示警告訊息"
              buttonColor="#ff6b6b"
              selectedColor="#cc5555"
              buttonSize="medium"
              onClick={handleShowWarningHint}
            />
          </div>
        </div>

        <div className="demo-page__section">
          <h2 className="demo-page__subtitle">Double Check Component 展示</h2>
          <div className="demo-page__hint-buttons">
            <Button
              title="顯示確認訂票視窗"
              buttonColor="#00cc88"
              selectedColor="#00aa66"
              buttonSize="medium"
              onClick={handleShowDoubleCheck}
            />
          </div>
        </div>
      </div>

      <Hint
        title="這是一個提示訊息"
        type="info"
        onConfirm={handleCloseInfoHint}
        isVisible={showInfoHint}
      />

      <Hint
        title="相關欄位未填寫或有誤，請確認"
        type="warning"
        onConfirm={handleCloseWarningHint}
        isVisible={showWarningHint}
      />

      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={handleCloseDoubleCheck}
        onConfirm={handleConfirmBooking}
        isVisible={showDoubleCheck}
      />
    </div>
  );
};

export default DemoPage;
