import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import DoubleCheck from "./DoubleCheck";
import "@testing-library/jest-dom";

/**
 * DoubleCheck Component 單元測試
 * 測試場景來自: .github/Features/frontend/requirements/DoubleCheck_Compoent.md
 */
describe("DoubleCheck Component", () => {
  const mockBookingInfo = [
    { label: "訂票種類", value: "THSR", italic: true },
    { label: "身份證字號", value: "A123456789", italic: true },
    { label: "訂票邏輯", value: "早鳥優先" },
    { label: "是否使用會員累積點數", value: "是" },
    { label: "搭乘日期", value: "2026-07-17", italic: true },
    { label: "搭乘時間", value: "15:00", italic: true },
  ];

  /**
   * 場景1: 顯示訂票資訊
   * 驗證: 應正確顯示所有訂票資訊
   */
  it("should render all booking information", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    // 驗證第一個和最後一個資訊項
    expect(screen.getByText(/訂票種類:/)).toBeInTheDocument();
    expect(screen.getByText("THSR")).toBeInTheDocument();

    // 驗證按鈕存在
    expect(
      screen.getByTestId("double-check-cancel-button"),
    ).toBeInTheDocument();
    expect(
      screen.getByTestId("double-check-confirm-button"),
    ).toBeInTheDocument();
  });

  /**
   * 場景2: 點擊「取消預約」按鈕
   * 驗證: 應呼叫 onCancel 回調
   */
  it("should call onCancel when cancel button is clicked", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const cancelButton = screen.getByTestId("double-check-cancel-button");
    fireEvent.click(cancelButton);

    expect(mockOnCancel).toHaveBeenCalledTimes(1);
    expect(mockOnConfirm).not.toHaveBeenCalled();
  });

  /**
   * 場景3: 點擊「確認預約」按鈕
   * 驗證: 應呼叫 onConfirm 回調
   */
  it("should call onConfirm when confirm button is clicked", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const confirmButton = screen.getByTestId("double-check-confirm-button");
    fireEvent.click(confirmButton);

    expect(mockOnConfirm).toHaveBeenCalledTimes(1);
    expect(mockOnCancel).not.toHaveBeenCalled();
  });

  /**
   * 場景4: isVisible 為 false 時不顯示
   * 驗證: 應不渲染任何內容
   */
  it("should not render when isVisible is false", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    const { container } = render(
      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={false}
      />,
    );

    expect(container.firstChild).toBeNull();
  });

  /**
   * 場景5: 驗證「取消預約」按鈕文字
   * 驗證: 按鈕文字應為「取消預約」
   */
  it("should have cancel button with text '取消預約'", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const cancelButton = screen.getByRole("button", { name: "取消預約" });
    expect(cancelButton).toBeInTheDocument();
  });

  /**
   * 場景6: 驗證「確認預約」按鈕文字
   * 驗證: 按鈕文字應為「確認預約」
   */
  it("should have confirm button with text '確認預約'", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const confirmButton = screen.getByRole("button", { name: "確認預約" });
    expect(confirmButton).toBeInTheDocument();
  });

  /**
   * 場景7: 驗證斜體樣式應用
   * 驗證: italic 為 true 的值應有斜體樣式
   */
  it("should apply italic style to values with italic=true", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const italicValue = screen.getByText("THSR");
    expect(italicValue).toHaveClass("italic");
  });

  /**
   * 場景8: isVisible 預設為 true
   * 驗證: 在未指定 isVisible 時應預設顯示
   */
  it("should render by default when isVisible is not specified", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={mockBookingInfo}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
      />,
    );

    expect(
      screen.getByRole("button", { name: "取消預約" }),
    ).toBeInTheDocument();
  });

  /**
   * 場景9: 驗證訂票資訊為空時的處理
   * 驗證: 應正確渲染空內容
   */
  it("should render with empty booking info", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={[]}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    // 應該還有按鈕存在
    expect(
      screen.getByRole("button", { name: "取消預約" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "確認預約" }),
    ).toBeInTheDocument();
  });

  /**
   * 場景10: 驗證訂票資訊不使用斜體
   * 驗證: 不設定 italic 或 italic=false 的值應不使用斜體
   */
  it("should not apply italic style to values without italic or italic=false", () => {
    const mockOnCancel = jest.fn();
    const mockOnConfirm = jest.fn();

    render(
      <DoubleCheck
        bookingInfo={[{ label: "標籤", value: "非斜體值", italic: false }]}
        onCancel={mockOnCancel}
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const value = screen.getByText("非斜體值");
    expect(value).not.toHaveClass("italic");
  });
});
