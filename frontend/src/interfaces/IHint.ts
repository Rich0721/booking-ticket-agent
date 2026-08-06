export type HintType = "info" | "warning";

export interface IHintProps {
  /**
   * 提示訊息的標題文字
   */
  title: string;

  /**
   * 提示訊息類型: info 或 warning
   * - info: 顯示資訊圖示
   * - warning: 顯示警告圖示
   */
  type: HintType;

  /**
   * 點選確認按鈕時觸發的事件
   */
  onConfirm: () => void;

  /**
   * 是否顯示提示訊息
   */
  isVisible?: boolean;
}
