export interface IDatePickerProps {
  title?: string;
  value?: string;
  onChange?: (value: string) => void;
  onBlur?: () => void;
}
