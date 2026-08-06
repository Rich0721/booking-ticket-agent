export interface BookingInfo {
  /**
   * 標籤文字
   */
  label: string;

  /**
   * 值文字
   */
  value: string;

  /**
   * 是否使用斜體顯示
   */
  italic?: boolean;
}

export interface IDoubleCheckProps {
  /**
   * 訂票資訊列表
   */
  bookingInfo: BookingInfo[];

  /**
   * 點選「取消預約」按鈕時觸發的事件
   */
  onCancel: () => void;

  /**
   * 點選「確認預約」按鈕時觸發的事件
   */
  onConfirm: () => void;

  /**
   * 是否顯示提示視窗
   */
  isVisible?: boolean;
}
