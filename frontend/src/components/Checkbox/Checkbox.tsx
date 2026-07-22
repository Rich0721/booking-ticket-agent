import React, { useEffect, useMemo, useState } from "react";
import {
  CheckboxOption,
  ICheckboxOptionWithIcon,
  ICheckboxProps,
} from "../../interfaces/ICheckbox";
import "./checkbox.css";

const getInitialSelectedValues = (
  options: readonly CheckboxOption[],
): string[] => {
  return options
    .filter((option) => option.defaultChecked)
    .map((option) => option.value);
};

const hasIconInAllOptions = (options: readonly CheckboxOption[]): boolean => {
  return options.every((option) => "icon" in option);
};

const validateOptions = (options: readonly CheckboxOption[]): void => {
  if (options.length === 0) {
    return;
  }

  const useIcon = hasIconInAllOptions(options);
  const hasSomeIcon = options.some((option) => "icon" in option);

  if (useIcon !== hasSomeIcon) {
    throw new Error("所有選項的Icon需要一致性，請確認選項全有Icon或全無Icon");
  }

  const uniqueValues = new Set(options.map((option) => option.value));
  if (uniqueValues.size !== options.length) {
    throw new Error("所有選項的value值需要唯一，請確認沒有重複的value");
  }
};

const Checkbox = <T extends readonly CheckboxOption[]>({
  options,
  required = false,
  onChange,
}: ICheckboxProps<T>) => {
  validateOptions(options);

  const [selectedValues, setSelectedValues] = useState<string[]>(() =>
    getInitialSelectedValues(options),
  );
  const [hasInteracted, setHasInteracted] = useState<boolean>(false);

  useEffect(() => {
    setSelectedValues(getInitialSelectedValues(options));
    setHasInteracted(false);
  }, [options]);

  const hasIcon = useMemo(() => hasIconInAllOptions(options), [options]);

  const showError = required && hasInteracted && selectedValues.length === 0;

  const handleToggle = (value: string, checked: boolean): void => {
    const nextValues = checked
      ? [...selectedValues, value]
      : selectedValues.filter((item) => item !== value);

    setSelectedValues(nextValues);
    setHasInteracted(true);

    const output = nextValues.join(",");
    if (onChange) {
      onChange(output);
    }
  };

  return (
    <div className="checkbox-group" data-testid="checkbox-group">
      {options.map((option) => {
        const isChecked = selectedValues.includes(option.value);

        return (
          <label
            key={option.value}
            className={`checkbox-group__option ${showError ? "checkbox-group__option--error" : ""}`}
          >
            <input
              type="checkbox"
              className="checkbox-group__input"
              checked={isChecked}
              onChange={(event) =>
                handleToggle(option.value, event.target.checked)
              }
              data-testid={`checkbox-input-${option.value}`}
            />
            <span className="checkbox-group__label">{option.label}</span>
            {hasIcon && (
              <img
                src={(option as ICheckboxOptionWithIcon).icon}
                alt={`${option.label} icon`}
                className="checkbox-group__icon"
              />
            )}
          </label>
        );
      })}

      {showError && (
        <div
          className="checkbox-group__error-message"
          data-testid="checkbox-error"
        >
          請至少勾選一個選項
        </div>
      )}
    </div>
  );
};

export default Checkbox;
