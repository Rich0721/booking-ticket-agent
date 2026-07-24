import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import Button from "./Button";

describe("Button Component", () => {
  // Scenario: 元件需顯示Title文字
  // Reference: Button_Component.md - Props設定: Title
  it("should render the title text", () => {
    render(<Button title="送出" />);

    expect(screen.getByText("送出")).toBeInTheDocument();
  });

  // Scenario: 提供Icon時應顯示於Title之前
  // Reference: Button_Component.md - 排版格式: [Icon] [Title]
  it("should render icon before title when icon is provided", () => {
    render(<Button title="送出" icon="/icons/submit.png" />);

    const button = screen.getByTestId("button-component");
    const icon = screen.getByRole("img");

    expect(icon).toHaveAttribute("src", "/icons/submit.png");
    expect(button.firstElementChild).toBe(icon);
  });

  // Scenario: 未提供Icon時不應顯示Icon
  // Reference: Button_Component.md - Props設定: Icon
  it("should not render an icon when icon is not provided", () => {
    render(<Button title="送出" />);

    expect(screen.queryByRole("img")).not.toBeInTheDocument();
  });

  // Scenario: 未提供ButtonColor與SelectedColor時應使用預設顏色
  // Reference: Button_Component.md - ButtonColor/SelectedColor 預設值
  it("should apply default button color when not pressed", () => {
    render(<Button title="送出" />);

    const button = screen.getByTestId("button-component");
    expect(button).toHaveStyle({ backgroundColor: "#007bff" });
  });

  // Scenario: 按下按鈕時應套用SelectedColor，放開後恢復ButtonColor
  // Reference: Button_Component.md - SelectedColor Props說明
  it("should switch to selected color while pressed and revert on release", () => {
    render(
      <Button title="送出" buttonColor="#111111" selectedColor="#222222" />,
    );

    const button = screen.getByTestId("button-component");

    fireEvent.mouseDown(button);
    expect(button).toHaveStyle({ backgroundColor: "#222222" });

    fireEvent.mouseUp(button);
    expect(button).toHaveStyle({ backgroundColor: "#111111" });
  });

  // Scenario: 滑鼠離開按鈕時應恢復ButtonColor
  // Reference: Button_Component.md - SelectedColor Props說明
  it("should revert to button color when mouse leaves while pressed", () => {
    render(
      <Button title="送出" buttonColor="#111111" selectedColor="#222222" />,
    );

    const button = screen.getByTestId("button-component");

    fireEvent.mouseDown(button);
    expect(button).toHaveStyle({ backgroundColor: "#222222" });

    fireEvent.mouseLeave(button);
    expect(button).toHaveStyle({ backgroundColor: "#111111" });
  });

  // Scenario: 未提供ButtonSize時預設為medium
  // Reference: Button_Component.md - ButtonSize 預設值: medium
  it("should default to medium size", () => {
    render(<Button title="送出" />);

    expect(screen.getByTestId("button-component")).toHaveClass(
      "button--medium",
    );
  });

  it.each([
    ["small", "button--small"],
    ["medium", "button--medium"],
    ["large", "button--large"],
  ] as const)(
    "should apply %s size class",
    // Scenario: ButtonSize可設定small/medium/large
    // Reference: Button_Component.md - ButtonSize: small/medium/large
    (size, expectedClass) => {
      render(<Button title="送出" buttonSize={size} />);

      expect(screen.getByTestId("button-component")).toHaveClass(expectedClass);
    },
  );

  // Scenario: 點選按鈕時應觸發OnClick事件
  // Reference: Button_Component.md - OnClick事件
  it("should call onClick when clicked", () => {
    const onClick = jest.fn();
    render(<Button title="送出" onClick={onClick} />);

    fireEvent.click(screen.getByTestId("button-component"));

    expect(onClick).toHaveBeenCalledTimes(1);
  });
});
