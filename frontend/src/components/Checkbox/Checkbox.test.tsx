import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import Checkbox from "./Checkbox";

describe("Checkbox Component", () => {
  // Scenario: 基本勾選互動與回傳格式
  // Reference: Checkbox_Component.md - OnChange事件
  it("should return comma-separated selected values on change", () => {
    const onChange = jest.fn();
    render(
      <Checkbox
        options={
          [
            { label: "早鳥", value: "EARLY", icon: "/icons/bird.png" },
            { label: "學生", value: "STUDENT", icon: "/icons/students.png" },
          ] as const
        }
        onChange={onChange}
      />,
    );

    fireEvent.click(screen.getByTestId("checkbox-input-EARLY"));
    expect(onChange).toHaveBeenLastCalledWith("EARLY");

    fireEvent.click(screen.getByTestId("checkbox-input-STUDENT"));
    expect(onChange).toHaveBeenLastCalledWith("EARLY,STUDENT");

    fireEvent.click(screen.getByTestId("checkbox-input-EARLY"));
    expect(onChange).toHaveBeenLastCalledWith("STUDENT");
  });

  // Scenario: 必填且取消所有勾選時顯示錯誤訊息
  // Reference: Checkbox_Component.md - 必填錯誤訊息
  it("should show error and return empty string when required and nothing selected", () => {
    const onChange = jest.fn();
    render(
      <Checkbox
        options={
          [
            {
              label: "早鳥",
              value: "EARLY",
              defaultChecked: true,
              icon: "/icons/bird.png",
            },
            { label: "學生", value: "STUDENT", icon: "/icons/students.png" },
          ] as const
        }
        required
        onChange={onChange}
      />,
    );

    fireEvent.click(screen.getByTestId("checkbox-input-EARLY"));

    expect(screen.getByTestId("checkbox-error")).toBeInTheDocument();
    expect(onChange).toHaveBeenLastCalledWith("");
    expect(screen.getByText("早鳥").closest("label")).toHaveClass(
      "checkbox-group__option--error",
    );
  });

  // Scenario: 非必填且取消所有勾選時不顯示錯誤
  // Reference: Checkbox_Component.md - 非必填回傳規則
  it("should return empty string without showing error when not required", () => {
    const onChange = jest.fn();
    render(
      <Checkbox
        options={
          [
            {
              label: "早鳥",
              value: "EARLY",
              defaultChecked: true,
            },
            { label: "學生", value: "STUDENT" },
          ] as const
        }
        onChange={onChange}
      />,
    );

    fireEvent.click(screen.getByTestId("checkbox-input-EARLY"));

    expect(screen.queryByTestId("checkbox-error")).not.toBeInTheDocument();
    expect(onChange).toHaveBeenLastCalledWith("");
  });

  // Scenario: Icon 使用規則一致性檢查
  // Reference: Checkbox_Component.md - 開發錯誤檢測
  it("should throw error when icon usage is inconsistent", () => {
    expect(() =>
      render(
        <Checkbox
          // @ts-expect-error 故意測試錯誤資料: Icon 使用不一致，應在型別層被攔截
          options={
            [
              { label: "早鳥", value: "EARLY", icon: "/icons/bird.png" },
              { label: "學生", value: "STUDENT" },
            ] as const
          }
        />,
      ),
    ).toThrow("所有選項的Icon需要一致性");
  });

  // Scenario: value 唯一性檢查
  // Reference: Checkbox_Component.md - 開發錯誤檢測
  it("should throw error when values are duplicated", () => {
    expect(() =>
      render(
        <Checkbox
          // @ts-expect-error 故意測試錯誤資料: value 重複，應在型別層被攔截
          options={
            [
              { label: "早鳥", value: "EARLY" },
              { label: "一般", value: "EARLY" },
            ] as const
          }
        />,
      ),
    ).toThrow("所有選項的value值需要唯一");
  });
});
