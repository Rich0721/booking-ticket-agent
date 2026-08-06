import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Hint from "./Hint";
import "@testing-library/jest-dom";

/**
 * Hint Component 單元測試
 * 測試場景來自: .github/Features/frontend/requirements/Hint_Component.md
 */
describe("Hint Component", () => {
  /**
   * 場景1: 顯示 Info 類型提示
   * 驗證: 應顯示資訊圖示、標題和確認按鈕
   */
  it("should render info hint with information icon", () => {
    const mockOnConfirm = jest.fn();
    render(
      <Hint
        title="這是一個提示訊息"
        type="info"
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    // 驗證是否渲染了 Hint 元素
    const hintElement = screen
      .getByTestId("hint-confirm-button")
      .closest(".hint");
    expect(hintElement).toBeInTheDocument();

    // 驗證是否有正確的 class
    expect(hintElement).toHaveClass("hint--info");

    // 驗證標題
    expect(screen.getByText("這是一個提示訊息")).toBeInTheDocument();

    // 驗證確認按鈕
    const confirmButton = screen.getByTestId("hint-confirm-button");
    expect(confirmButton).toBeInTheDocument();
    expect(confirmButton).toHaveTextContent("確認");
  });

  /**
   * 場景2: 顯示 Warning 類型提示
   * 驗證: 應顯示警告圖示、標題和確認按鈕
   */
  it("should render warning hint with warning icon", () => {
    const mockOnConfirm = jest.fn();
    render(
      <Hint
        title="相關欄位未填寫或有誤，請確認"
        type="warning"
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    // 驗證是否有正確的 class
    const hintElement = screen
      .getByTestId("hint-confirm-button")
      .closest(".hint");
    expect(hintElement).toHaveClass("hint--warning");

    // 驗證標題
    expect(
      screen.getByText("相關欄位未填寫或有誤，請確認"),
    ).toBeInTheDocument();

    // 驗證確認按鈕
    expect(screen.getByTestId("hint-confirm-button")).toBeInTheDocument();
  });

  /**
   * 場景3: 點擊確認按鈕觸發 onConfirm 回調
   * 驗證: 應呼叫 onConfirm 函式
   */
  it("should call onConfirm when confirm button is clicked", () => {
    const mockOnConfirm = jest.fn();
    render(
      <Hint
        title="測試訊息"
        type="info"
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const confirmButton = screen.getByTestId("hint-confirm-button");
    fireEvent.click(confirmButton);

    expect(mockOnConfirm).toHaveBeenCalledTimes(1);
  });

  /**
   * 場景4: isVisible 為 false 時不顯示提示
   * 驗證: 應不渲染任何內容
   */
  it("should not render when isVisible is false", () => {
    const mockOnConfirm = jest.fn();
    const { container } = render(
      <Hint
        title="測試訊息"
        type="info"
        onConfirm={mockOnConfirm}
        isVisible={false}
      />,
    );

    expect(container.firstChild).toBeNull();
  });

  /**
   * 場景5: 驗證 icon 圖片來源正確
   * 驗證: info 類型使用 information.png，warning 類型使用 warning.png
   */
  it("should render correct icon src for info type", () => {
    const mockOnConfirm = jest.fn();
    render(
      <Hint
        title="測試訊息"
        type="info"
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const icon = screen.getByAltText("info");
    expect(icon).toHaveAttribute("src", "/icons/information.png");
  });

  it("should render correct icon src for warning type", () => {
    const mockOnConfirm = jest.fn();
    render(
      <Hint
        title="測試訊息"
        type="warning"
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const icon = screen.getByAltText("warning");
    expect(icon).toHaveAttribute("src", "/icons/warning.png");
  });

  /**
   * 場景6: 驗證確認按鈕文本固定為"確認"
   * 驗證: 按鈕文本應為"確認"
   */
  it("should have confirm button with text '確認'", () => {
    const mockOnConfirm = jest.fn();
    render(
      <Hint
        title="測試訊息"
        type="info"
        onConfirm={mockOnConfirm}
        isVisible={true}
      />,
    );

    const confirmButton = screen.getByRole("button", { name: "確認" });
    expect(confirmButton).toBeInTheDocument();
  });

  /**
   * 場景7: isVisible 預設為 true
   * 驗證: 在未指定 isVisible 時應預設顯示
   */
  it("should render by default when isVisible is not specified", () => {
    const mockOnConfirm = jest.fn();
    render(<Hint title="預設顯示" type="info" onConfirm={mockOnConfirm} />);

    expect(screen.getByText("預設顯示")).toBeInTheDocument();
  });
});
