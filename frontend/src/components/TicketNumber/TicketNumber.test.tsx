import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import TicketNumber from "./TicketNumber";

describe("TicketNumber Component", () => {
  // Scenario: 開發者需設定 icon 與 title
  // Reference: Ticket_Number_Component.md - 檢查開發者須設定icon與Title
  it("should throw error when title is empty", () => {
    expect(() =>
      render(<TicketNumber title="" iconSrc="/icons/people.png" />),
    ).toThrow("icon與Title為必填");
  });

  // Scenario: 開發者需設定 icon 與 title
  // Reference: Ticket_Number_Component.md - 檢查開發者須設定icon與Title
  it("should throw error when icon is empty", () => {
    expect(() => render(<TicketNumber title="成人票" iconSrc="" />)).toThrow(
      "icon與Title為必填",
    );
  });

  // Scenario: 預設 min 與 max
  // Reference: Ticket_Number_Component.md - Textbox min/max 預設值
  it("should use default min and max values", () => {
    render(<TicketNumber title="成人票" iconSrc="/icons/people.png" />);

    const input = screen.getByTestId("ticket-number-input") as HTMLInputElement;
    expect(input.min).toBe("0");
    expect(input.max).toBe("10");
  });

  // Scenario: 可由開發者指定 min 與 max
  // Reference: Ticket_Number_Component.md - Textbox min/max 設定
  it("should use custom min and max values", () => {
    render(
      <TicketNumber
        title="成人票"
        iconSrc="/icons/people.png"
        min={2}
        max={5}
      />,
    );

    const input = screen.getByTestId("ticket-number-input") as HTMLInputElement;
    expect(input.min).toBe("2");
    expect(input.max).toBe("5");
  });

  // Scenario: 輸入合法票數時透過 onChange 回傳 number
  // Reference: Ticket_Number_Component.md - onChange 回傳數字
  it("should call onChange with number when input is valid", () => {
    const onChange = jest.fn();
    render(
      <TicketNumber
        title="成人票"
        iconSrc="/icons/people.png"
        onChange={onChange}
      />,
    );

    const input = screen.getByTestId("ticket-number-input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "6" } });

    expect(onChange).toHaveBeenCalledWith(6);
  });

  // Scenario: 輸入超出範圍時顯示錯誤訊息
  // Reference: Ticket_Number_Component.md - 輸入不符合預期顯示錯誤
  it("should show error when value is out of range", () => {
    render(
      <TicketNumber
        title="成人票"
        iconSrc="/icons/people.png"
        min={1}
        max={3}
      />,
    );

    const input = screen.getByTestId("ticket-number-input") as HTMLInputElement;
    fireEvent.change(input, { target: { value: "5" } });

    expect(screen.getByTestId("ticket-number-error").textContent).toContain(
      "票數需為1到3之間的整數",
    );
    expect(input).toHaveClass("ticket-number__input--error");
  });
});
