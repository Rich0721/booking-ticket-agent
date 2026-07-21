import React, { useState } from "react";
import { IIDNumberInputProps } from "../../interfaces/IIDNumberInput";
import { isValidTaiwanID } from "../../utils/idValidator";
import "./id-number-input.css";

/**
 * 身份證字號輸入Component
 * 提供使用者輸入台灣身份證號碼，並即時驗證格式
 *
 * @param props - 元件屬性
 * @returns JSX元素
 *
 * @example
 * <IDNumberInput
 *   title="訂票者身份證字號"
 *   maxLength={10}
 *   onChange={(value) => console.log(value)}
 *   onBlur={() => console.log('blurred')}
 * />
 */
const IDNumberInput: React.FC<IIDNumberInputProps> = ({
  title = "身份證字號",
  maxLength = 10,
  onChange,
  onBlur,
  value = "",
  iconSrc = "/icons/user.png",
}) => {
  const [inputValue, setInputValue] = useState<string>(value);
  const [hasBlurred, setHasBlurred] = useState<boolean>(false);
  const [isValid, setIsValid] = useState<boolean>(true);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value.toUpperCase();

    // 只允許英文字母和數字
    if (/^[A-Z0-9]*$/.test(newValue)) {
      setInputValue(newValue);

      // 呼叫外部onChange回呼
      if (onChange) {
        onChange(newValue);
      }
    }
  };

  const handleBlur = () => {
    setHasBlurred(true);

    // 驗證輸入值
    if (inputValue.trim() !== "") {
      const valid = isValidTaiwanID(inputValue);
      setIsValid(valid);
    } else {
      setIsValid(true); // 空值不顯示錯誤
    }

    // 呼叫外部onBlur回呼
    if (onBlur) {
      onBlur();
    }
  };

  const handleFocus = () => {
    // 取消錯誤顯示，但保持 hasBlurred 狀態以便重新輸入後重新驗證
    if (isValid === false) {
      setIsValid(true);
    }
  };

  const showError = hasBlurred && !isValid && inputValue.trim() !== "";

  return (
    <div className="id-number-input-container">
      {/* Icon */}
      <div className="id-number-input__icon">
        <img src={iconSrc} alt="身份證字號" />
      </div>

      {/* Title & Textbox 容器 */}
      <div className="id-number-input__content">
        {/* Title */}
        <label className="id-number-input__title" htmlFor="id-number-input">
          {title}
        </label>

        {/* Textbox */}
        <input
          id="id-number-input"
          type="text"
          className={`id-number-input__textbox ${showError ? "id-number-input__textbox--error" : ""}`}
          value={inputValue}
          onChange={handleChange}
          onBlur={handleBlur}
          onFocus={handleFocus}
          maxLength={maxLength}
          placeholder="例：Z123456788"
          data-testid="id-number-input"
        />

        {/* Error Message */}
        {showError && (
          <div
            className="id-number-input__error-message"
            data-testid="error-message"
          >
            身份證字號格式錯誤，請重新輸入
          </div>
        )}
      </div>
    </div>
  );
};

export default IDNumberInput;
