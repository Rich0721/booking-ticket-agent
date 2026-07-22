import React, { useEffect, useState } from "react";
import { ITicketNumberProps } from "../../interfaces/ITicketNumber";
import "./ticket-number.css";

const TicketNumber: React.FC<ITicketNumberProps> = ({
  title,
  iconSrc,
  min = 0,
  max = 10,
  value,
  onChange,
}) => {
  if (title.trim() === "" || iconSrc.trim() === "") {
    throw new Error("icon與Title為必填，請確認設定後再使用TicketNumber元件");
  }

  if (min > max) {
    throw new Error("min不可大於max，請確認TicketNumber元件參數設定");
  }

  const [inputValue, setInputValue] = useState<string>(String(value ?? min));
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    if (value === undefined) {
      return;
    }

    setInputValue(String(value));
  }, [value]);

  const validateValue = (nextValue: string): number | null => {
    if (!/^-?\d+$/.test(nextValue)) {
      return null;
    }

    const parsed = Number(nextValue);
    if (!Number.isInteger(parsed)) {
      return null;
    }

    return parsed;
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const nextRawValue = event.target.value;
    setInputValue(nextRawValue);

    const parsedValue = validateValue(nextRawValue);
    if (parsedValue === null) {
      setErrorMessage(`票數需為${min}到${max}之間的整數`);
      return;
    }

    if (parsedValue < min || parsedValue > max) {
      setErrorMessage(`票數需為${min}到${max}之間的整數`);
      return;
    }

    setErrorMessage("");
    if (onChange) {
      onChange(parsedValue);
    }
  };

  const handleBlur = () => {
    const parsedValue = validateValue(inputValue);

    if (parsedValue === null || parsedValue < min || parsedValue > max) {
      setErrorMessage(`票數需為${min}到${max}之間的整數`);
      return;
    }

    setErrorMessage("");
  };

  return (
    <div className="ticket-number-container">
      <div className="ticket-number__header">
        <label className="ticket-number__title" htmlFor="ticket-number-input">
          {title}
        </label>
        <div className="ticket-number__icon-wrapper">
          <img
            className="ticket-number__icon"
            src={iconSrc}
            alt={`${title} icon`}
          />
        </div>
      </div>

      <input
        id="ticket-number-input"
        type="number"
        min={min}
        max={max}
        value={inputValue}
        onChange={handleChange}
        onBlur={handleBlur}
        className={`ticket-number__input ${errorMessage ? "ticket-number__input--error" : ""}`}
        data-testid="ticket-number-input"
      />

      {errorMessage && (
        <div className="ticket-number__error" data-testid="ticket-number-error">
          {errorMessage}
        </div>
      )}
    </div>
  );
};

export default TicketNumber;
