export type ButtonSize = "small" | "medium" | "large";

export interface IButtonProps {
  /**
   * 按鈕顯示文字
   */
  title: string;

  /**
   * 按鈕Icon來源路徑，未提供則不顯示Icon
   */
  icon?: string;

  /**
   * 按鈕顏色，預設為 #007bff
   */
  buttonColor?: string;

  /**
   * 按鈕被選取(按下)時的顏色，預設為 #0056b3
   */
  selectedColor?: string;

  /**
   * 按鈕大小，預設為 medium
   */
  buttonSize?: ButtonSize;

  /**
   * 點選按鈕時觸發的事件
   */
  onClick?: () => void;
}
