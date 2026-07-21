import React, { useMemo, useState } from "react";
import { IDatePickerProps } from "../../interfaces/IDatePicker";
import "./date-picker.css";

const getTodayISODate = (): string => {
  return new Date().toISOString().split("T")[0];
};

const getTomorrowISODate = (): string => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  return tomorrow.toISOString().split("T")[0];
};

const DatePicker: React.FC<IDatePickerProps> = ({
  title = "搭乘日期",
  value = "",
  onChange,
  onBlur,
}) => {
  const [inputValue, setInputValue] = useState<string>(value);
  const [hasBlurred, setHasBlurred] = useState<boolean>(false);

  const minDate = useMemo(() => getTomorrowISODate(), []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const nextValue = e.target.value;
    const today = getTodayISODate();

    if (nextValue !== "" && nextValue <= today) {
      setInputValue("");
      if (onChange) {
        onChange("");
      }
      return;
    }

    setInputValue(nextValue);
    if (onChange) {
      onChange(nextValue);
    }
  };

  const handleBlur = () => {
    setHasBlurred(true);
    if (onBlur) {
      onBlur();
    }
  };

  const showError = hasBlurred && inputValue.trim() === "";

  return (
    <div className="date-picker-container">
      <div className="date-picker__icon">
        <img src="/icons/time-planning.png" alt="日期選擇" />
      </div>

      <div className="date-picker__content">
        <label className="date-picker__title" htmlFor="date-picker-input">
          {title}
        </label>

        <input
          id="date-picker-input"
          type="date"
          className={`date-picker__textbox ${showError ? "date-picker__textbox--error" : ""}`}
          value={inputValue}
          min={minDate}
          onChange={handleChange}
          onBlur={handleBlur}
          data-testid="date-picker-input"
        />

        {showError && (
          <div
            className="date-picker__error-message"
            data-testid="error-message"
          >
            日期不可為空，請重新選擇
          </div>
        )}
      </div>
    </div>
  );
};

export default DatePicker;
