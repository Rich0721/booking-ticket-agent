export interface ITicketNumberProps {
  title: string;
  iconSrc: string;
  min?: number;
  max?: number;
  value?: number;
  onChange?: (value: number) => void;
}
