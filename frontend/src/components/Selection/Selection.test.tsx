import React from "react";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import Selection from "./Selection";

describe("Selection Component", () => {
  const mockMenu = [
    { id: 1, parm_name: "台北", parm_value: "TAIPEI" },
    { id: 2, parm_name: "台中", parm_value: "TAICHUNG" },
  ];

  beforeEach(() => {
    global.fetch = jest.fn().mockResolvedValue({
      json: () =>
        Promise.resolve({
          info: {
            menu: mockMenu,
          },
        }),
    }) as jest.Mock;
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  // Scenario: 元件需顯示Icon與Title
  // Reference: Selection_Component.md - 排版格式: [Icon] [Title] [下拉選單]
  it("should render icon and title", async () => {
    render(
      <Selection
        iconSrc="/icons/station.png"
        title="搭乘起站"
        parmCategory="THSR_STATION"
      />,
    );

    expect(screen.getByAltText("搭乘起站 icon")).toHaveAttribute(
      "src",
      "/icons/station.png",
    );
    expect(screen.getByText("搭乘起站")).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText("台北")).toBeInTheDocument();
    });
  });

  // Scenario: 依照parm_category呼叫API並加上請選擇預設值
  // Reference: Selection_Component.md - parm_category Props說明
  it("should fetch options using parm_category and prepend 請選擇 placeholder", async () => {
    render(
      <Selection
        iconSrc="/icons/station.png"
        title="搭乘起站"
        parmCategory="THSR_STATION"
      />,
    );

    expect(global.fetch).toHaveBeenCalledWith(
      "/loading-selected?parm_category=THSR_STATION",
    );

    await waitFor(() => {
      expect(screen.getByText("台北")).toBeInTheDocument();
    });

    const select = screen.getByTestId("selection-select") as HTMLSelectElement;
    const optionLabels = Array.from(select.options).map((opt) => opt.text);
    expect(optionLabels).toEqual(["請選擇", "台北", "台中"]);
  });

  // Scenario: 使用者選擇選項時觸發onChange並回傳value
  // Reference: Selection_Component.md - OnChange事件
  it("should call onChange with selected value", async () => {
    const onChange = jest.fn();
    render(
      <Selection
        iconSrc="/icons/station.png"
        title="搭乘起站"
        parmCategory="THSR_STATION"
        onChange={onChange}
      />,
    );

    await waitFor(() => {
      expect(screen.getByText("台北")).toBeInTheDocument();
    });

    const select = screen.getByTestId("selection-select") as HTMLSelectElement;
    fireEvent.change(select, { target: { value: "TAIPEI" } });

    expect(onChange).toHaveBeenCalledWith("TAIPEI");
    expect(screen.queryByTestId("selection-error")).not.toBeInTheDocument();
  });

  // Scenario: 必填且使用者沒有選擇任何選項
  // Reference: Selection_Component.md - 必填錯誤訊息
  it("should show error, mark select red and return empty string when required and nothing selected", async () => {
    const onChange = jest.fn();
    render(
      <Selection
        iconSrc="/icons/station.png"
        title="搭乘起站"
        parmCategory="THSR_STATION"
        required
        onChange={onChange}
      />,
    );

    await waitFor(() => {
      expect(screen.getByText("台北")).toBeInTheDocument();
    });

    const select = screen.getByTestId("selection-select") as HTMLSelectElement;
    fireEvent.change(select, { target: { value: "" } });

    expect(screen.getByTestId("selection-error")).toHaveTextContent(
      "請至少選擇一個選項",
    );
    expect(select).toHaveClass("selection__select--error");
    expect(onChange).toHaveBeenCalledWith("");
  });

  // Scenario: 非必填且使用者沒有選擇任何選項
  // Reference: Selection_Component.md - 非必填回傳規則
  it("should return empty string without error when not required and nothing selected", async () => {
    const onChange = jest.fn();
    render(
      <Selection
        iconSrc="/icons/station.png"
        title="搭乘起站"
        parmCategory="THSR_STATION"
        required={false}
        onChange={onChange}
      />,
    );

    await waitFor(() => {
      expect(screen.getByText("台北")).toBeInTheDocument();
    });

    const select = screen.getByTestId("selection-select") as HTMLSelectElement;
    fireEvent.change(select, { target: { value: "TAIPEI" } });
    fireEvent.change(select, { target: { value: "" } });

    expect(screen.queryByTestId("selection-error")).not.toBeInTheDocument();
    expect(select).not.toHaveClass("selection__select--error");
    expect(onChange).toHaveBeenLastCalledWith("");
  });
});
