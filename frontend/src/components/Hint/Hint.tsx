import React from "react";
import { IHintProps } from "../../interfaces/IHint";
import "./hint.css";

const Hint: React.FC<IHintProps> = ({
  title,
  type,
  onConfirm,
  isVisible = true,
}) => {
  if (!isVisible) {
    return null;
  }

  const iconSrc =
    type === "info" ? "/icons/information.png" : "/icons/warning.png";

  return (
    <div className="hint-overlay">
      <div className={`hint hint--${type}`}>
        <div className="hint__content">
          <img className="hint__icon" src={iconSrc} alt={type} />
          <h2 className="hint__title">{title}</h2>
        </div>
        <button
          className="hint__button"
          onClick={onConfirm}
          type="button"
          data-testid="hint-confirm-button"
        >
          確認
        </button>
      </div>
    </div>
  );
};

export default Hint;
