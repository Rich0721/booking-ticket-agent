export interface ISelectionOption {
  id: number;
  parm_name: string;
  parm_value: string;
}

export interface ISelectionProps {
  /**
   * Icon的來源路徑
   */
  iconSrc: string;

  /**
   * 下拉選單的標題
   */
  title: string;

  /**
   * 下拉選單資料來源分類，會透過API-/loading-selected?parm_category={parmCategory}取得選單資料
   */
  parmCategory: string;

  /**
   * 是否為必填，預設為true
   */
  required?: boolean;

  /**
   * 選擇變更時的回呼函式，回傳目前選擇的value值，若未選擇則回傳空字串
   */
  onChange?: (value: string) => void;
}
