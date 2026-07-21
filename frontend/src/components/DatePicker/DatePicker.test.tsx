import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import DatePicker from "./DatePicker";

const getTodayISODate = (): string => {
  return new Date().toISOString().split("T")[0];
};

const getTomorrowISODate = (): string => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  return tomorrow.toISOString().split("T")[0];
};

describe("DatePicker Component", () => {
  // Scenario: 使用者選擇當天進行預約訂票
  // Reference: Booking_THSR.feature - Rule: 使用者選擇搭乘日期
  it("should set minimum selectable date to tomorrow", () => {
    render(<DatePicker />);

    const input = screen.getByTestId("date-picker-input") as HTMLInputElement;
    expect(input.min).toBe(getTomorrowISODate());
  });

  // Scenario: 使用者選擇過去進行預約訂票
  // Reference: Booking_THSR.feature - Rule: 使用者選擇搭乘日期
  it("should not allow selecting today or a past date", () => {
    render(<DatePicker />);

    const input = screen.getByTestId("date-picker-input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: getTodayISODate() } });

    expect(input.value).toBe("");
  });

  // Scenario: 使用者選擇未來進行預約訂票
  // Reference: Booking_THSR.feature - Rule: 使用者選擇搭乘日期
  it("should allow selecting a future date in YYYY-MM-DD format", () => {
    render(<DatePicker />);

    const input = screen.getByTestId("date-picker-input") as HTMLInputElement;
    const futureDate = "2026-07-30";

    fireEvent.change(input, { target: { value: futureDate } });

    expect(input.value).toBe(futureDate);
  });

  // Scenario: Textbox 失去焦點且輸入值為空
  // Reference: Date_Component.md - ErrorMessage 顯示條件
  it("should display error message when input loses focus and value is empty", () => {
    render(<DatePicker />);

    const input = screen.getByTestId("date-picker-input") as HTMLInputElement;
    fireEvent.blur(input);

    const errorMessage = screen.getByTestId("error-message");
    expect(errorMessage).toBeInTheDocument();
    expect(errorMessage.textContent).toBe("日期不可為空，請重新選擇");
    expect(input).toHaveClass("date-picker__textbox--error");
  });

  // Scenario: Textbox 失去焦點且輸入值不為空
  // Reference: Date_Component.md - ErrorMessage 顯示條件
  it("should not display error message when input has value", () => {
    render(<DatePicker />);

    const input = screen.getByTestId("date-picker-input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: getTomorrowISODate() } });
    fireEvent.blur(input);

    const errorMessage = screen.queryByTestId("error-message");
    expect(errorMessage).not.toBeInTheDocument();
  });

  it("should show default title", () => {
    render(<DatePicker />);
    expect(screen.getByText("搭乘日期")).toBeInTheDocument();
  });

  it("should show custom title", () => {
    render(<DatePicker title="去程日期" />);
    expect(screen.getByText("去程日期")).toBeInTheDocument();
  });

  it("should call onChange with selected value", () => {
    const onChange = jest.fn();
    render(<DatePicker onChange={onChange} />);

    const input = screen.getByTestId("date-picker-input") as HTMLInputElement;
    const futureDate = getTomorrowISODate();

    fireEvent.change(input, { target: { value: futureDate } });
    expect(onChange).toHaveBeenCalledWith(futureDate);
  });

  it("should call onBlur callback", () => {
    const onBlur = jest.fn();
    render(<DatePicker onBlur={onBlur} />);

    const input = screen.getByTestId("date-picker-input") as HTMLInputElement;
    fireEvent.blur(input);

    expect(onBlur).toHaveBeenCalled();
  });
});
