import React from "react";
import { IDoubleCheckProps } from "../../interfaces/IDoubleCheck";
import "./double-check.css";

const DoubleCheck: React.FC<IDoubleCheckProps> = ({
  bookingInfo,
  onCancel,
  onConfirm,
  isVisible = true,
}) => {
  if (!isVisible) {
    return null;
  }

  return (
    <div className="double-check-overlay">
      <div className="double-check">
        <div className="booking-details">
          {bookingInfo.map((item, index) => (
            <p key={index} className="booking-line">
              <span className="booking-label">{item.label}:</span>{" "}
              <span className={`booking-value${item.italic ? " italic" : ""}`}>
                {item.value}
              </span>
            </p>
          ))}
        </div>
        <div className="button-group">
          <button
            className="btn btn-cancel"
            onClick={onCancel}
            type="button"
            data-testid="double-check-cancel-button"
          >
            取消預約
          </button>
          <button
            className="btn btn-confirm"
            onClick={onConfirm}
            type="button"
            data-testid="double-check-confirm-button"
          >
            確認預約
          </button>
        </div>
      </div>
    </div>
  );
};

export default DoubleCheck;
