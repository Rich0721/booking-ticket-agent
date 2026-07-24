import React, { useState } from "react";
import { IButtonProps } from "../../interfaces/IButton";
import "./button.css";

const Button: React.FC<IButtonProps> = ({
  title,
  icon,
  buttonColor = "#007bff",
  selectedColor = "#0056b3",
  buttonSize = "medium",
  onClick,
}) => {
  const [isPressed, setIsPressed] = useState<boolean>(false);

  const handlePressStart = () => setIsPressed(true);
  const handlePressEnd = () => setIsPressed(false);

  return (
    <button
      type="button"
      className={`button button--${buttonSize}`}
      style={{ backgroundColor: isPressed ? selectedColor : buttonColor }}
      onClick={onClick}
      onMouseDown={handlePressStart}
      onMouseUp={handlePressEnd}
      onMouseLeave={handlePressEnd}
      data-testid="button-component"
    >
      {icon && <img className="button__icon" src={icon} alt="" />}
      <span className="button__title">{title}</span>
    </button>
  );
};

export default Button;
