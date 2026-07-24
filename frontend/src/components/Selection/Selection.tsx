import React, { useEffect, useState } from "react";
import { ISelectionOption, ISelectionProps } from "../../interfaces/ISelection";
import "./selection.css";

const PLACEHOLDER_OPTION: ISelectionOption = {
  id: 0,
  parm_name: "請選擇",
  parm_value: "",
};

const Selection: React.FC<ISelectionProps> = ({
  iconSrc,
  title,
  parmCategory,
  required = true,
  onChange,
}) => {
  const [options, setOptions] = useState<ISelectionOption[]>([
    PLACEHOLDER_OPTION,
  ]);
  const [selectedValue, setSelectedValue] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    let isMounted = true;

    const fetchOptions = async () => {
      try {
        const response = await fetch(
          `/loading-selected?parm_category=${parmCategory}`,
        );
        const data = await response.json();
        const menu: ISelectionOption[] = data?.info?.menu ?? [];

        if (isMounted) {
          setOptions([PLACEHOLDER_OPTION, ...menu]);
        }
      } catch {
        if (isMounted) {
          setOptions([PLACEHOLDER_OPTION]);
        }
      }
    };

    fetchOptions();

    return () => {
      isMounted = false;
    };
  }, [parmCategory]);

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const nextValue = event.target.value;
    setSelectedValue(nextValue);

    if (nextValue === "") {
      setErrorMessage(required ? "請至少選擇一個選項" : "");
      if (onChange) {
        onChange("");
      }
      return;
    }

    setErrorMessage("");
    if (onChange) {
      onChange(nextValue);
    }
  };

  const showError = errorMessage !== "";

  return (
    <div className="selection-container">
      <img className="selection__icon" src={iconSrc} alt={`${title} icon`} />
      <label className="selection__title" htmlFor="selection-select">
        {title}
      </label>

      <div className="selection__select-wrapper">
        <select
          id="selection-select"
          className={`selection__select ${showError ? "selection__select--error" : ""}`}
          value={selectedValue}
          onChange={handleChange}
          data-testid="selection-select"
        >
          {options.map((option) => (
            <option key={option.parm_value} value={option.parm_value}>
              {option.parm_name}
            </option>
          ))}
        </select>

        {showError && (
          <div
            className="selection__error-message"
            data-testid="selection-error"
          >
            {errorMessage}
          </div>
        )}
      </div>
    </div>
  );
};

export default Selection;
