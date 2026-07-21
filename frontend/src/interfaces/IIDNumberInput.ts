export interface IIDNumberInputProps {
  /**
   * 輸入框標題，預設為'身份證字號'
   */
  title?: string;

  /**
   * 輸入框的最大長度，預設為10
   */
  maxLength?: number;

  /**
   * 輸入框值變更時的回呼函式
   */
  onChange?: (value: string) => void;

  /**
   * 輸入框失去焦點時的回呼函式
   */
  onBlur?: () => void;

  /**
   * 輸入框的初始值
   */
  value?: string;

  /**
   * Icon的來源路徑
   */
  iconSrc?: string;
}
