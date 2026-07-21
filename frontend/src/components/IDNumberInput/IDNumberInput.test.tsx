import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import IDNumberInput from "./IDNumberInput";

describe("IDNumberInput Component", () => {
  // Scenario: 使用者輸入錯誤的身份證字號
  // Reference: Booking_THSR.feature - 使用者輸入錯誤的身份證字號
  it("should display error message when invalid Taiwan ID is entered", async () => {
    const { rerender } = render(
      <IDNumberInput
        value=""
        onChange={(value) => {
          rerender(<IDNumberInput value={value} />);
        }}
      />,
    );

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    // 輸入錯誤的身份證字號
    fireEvent.change(input, { target: { value: "Z123456789" } });
    fireEvent.blur(input);

    // 驗證錯誤訊息是否顯示
    const errorMessage = screen.getByTestId("error-message");
    expect(errorMessage).toBeInTheDocument();
    expect(errorMessage.textContent).toBe("身份證字號格式錯誤，請重新輸入");
    expect(input).toHaveClass("id-number-input__textbox--error");
  });

  // Scenario: 使用者輸入正確的身份證字號
  // Reference: Booking_THSR.feature - 使用者輸入正確的身份證字號
  it("should not display error message when valid Taiwan ID is entered", async () => {
    render(<IDNumberInput />);

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    // 輸入正確的身份證字號
    fireEvent.change(input, { target: { value: "A100000001" } });
    fireEvent.blur(input);

    // 驗證錯誤訊息不顯示
    const errorMessage = screen.queryByTestId(
      "error-message",
    ) as HTMLElement | null;
    expect(errorMessage).not.toBeInTheDocument();
    expect(input).not.toHaveClass("id-number-input__textbox--error");
  });

  // 測試：空值時不顯示錯誤
  it("should not display error message when input is empty", () => {
    render(<IDNumberInput />);

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    // 失去焦點時輸入框為空
    fireEvent.blur(input);

    // 驗證錯誤訊息不顯示
    const errorMessage = screen.queryByTestId(
      "error-message",
    ) as HTMLElement | null;
    expect(errorMessage).not.toBeInTheDocument();
  });

  // 測試：自動轉換為大寫
  it("should convert input to uppercase automatically", () => {
    render(<IDNumberInput />);

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    // 輸入小寫
    fireEvent.change(input, { target: { value: "a100000001" } });

    // 驗證已轉換為大寫
    expect(input.value).toBe("A100000001");
  });

  // 測試：最大長度限制
  it("should respect maxLength property", () => {
    render(<IDNumberInput maxLength={10} />);

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    // 嘗試輸入超過最大長度的值
    fireEvent.change(input, { target: { value: "A1000000011" } });

    // 驗證長度限制為 10
    expect(input.maxLength).toBe(10);
  });

  // 測試：onChange 回呼函式
  it("should call onChange callback when input value changes", () => {
    const mockOnChange = jest.fn();
    render(<IDNumberInput onChange={mockOnChange} />);

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    fireEvent.change(input, { target: { value: "A100000001" } });

    expect(mockOnChange).toHaveBeenCalledWith("A100000001");
  });

  // 測試：onBlur 回呼函式
  it("should call onBlur callback when input loses focus", () => {
    const mockOnBlur = jest.fn();
    render(<IDNumberInput onBlur={mockOnBlur} />);

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    fireEvent.blur(input);

    expect(mockOnBlur).toHaveBeenCalled();
  });

  // 測試：自訂 title
  it("should display custom title", () => {
    const customTitle = "訂票者身份證字號";
    render(<IDNumberInput title={customTitle} />);

    const titleElement = screen.getByText(customTitle);
    expect(titleElement).toBeInTheDocument();
  });

  // 測試：預設 title
  it("should display default title when not provided", () => {
    render(<IDNumberInput />);

    const titleElement = screen.getByText("身份證字號");
    expect(titleElement).toBeInTheDocument();
  });

  // 測試：錯誤狀態和焦點交互
  it("should clear error when input regains focus", () => {
    render(<IDNumberInput />);

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    // 輸入錯誤的身份證字號並失去焦點
    fireEvent.change(input, { target: { value: "Z123456789" } });
    fireEvent.blur(input);

    // 驗證錯誤訊息顯示
    let errorMessage: HTMLElement | null = screen.getByTestId("error-message");
    expect(errorMessage).toBeInTheDocument();

    // 重新獲得焦點
    fireEvent.focus(input);

    // 驗證錯誤訊息暫時隱藏
    errorMessage = screen.queryByTestId("error-message") as HTMLElement | null;
    expect(errorMessage).not.toBeInTheDocument();
  });

  // 測試：僅允許英文字母和數字
  it("should only allow letters and numbers", () => {
    render(<IDNumberInput />);

    const input = screen.getByTestId("id-number-input") as HTMLInputElement;

    // 先輸入有效的身份證格式
    fireEvent.change(input, { target: { value: "A100000001" } });
    expect(input.value).toBe("A100000001");

    // 清空並嘗試輸入特殊字符（應該被過濾）
    fireEvent.change(input, { target: { value: "" } });
    fireEvent.change(input, { target: { value: "A100000001@#" } });

    // 驗證特殊字符被過濾
    expect(input.value).toMatch(/^[A-Z0-9]*$/);
  });

  // 測試：有效的身份證號碼驗證
  it("should validate multiple valid Taiwan IDs correctly", () => {
    const validIDs = ["A100000001", "B100000002", "C100000003"];

    validIDs.forEach((validID) => {
      const { unmount } = render(<IDNumberInput />);

      const input = screen.getByTestId("id-number-input") as HTMLInputElement;

      fireEvent.change(input, { target: { value: validID } });
      fireEvent.blur(input);

      const errorMessage = screen.queryByTestId(
        "error-message",
      ) as HTMLElement | null;
      expect(errorMessage).not.toBeInTheDocument();

      unmount();
    });
  });
});
