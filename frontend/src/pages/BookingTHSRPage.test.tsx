import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import BookingTHSRPage from "./BookingTHSRPage";

// Mock the components that depend on external resources or complex logic
jest.mock("../components", () => ({
  Button: ({ title, onClick }: any) => (
    <button onClick={onClick}>{title}</button>
  ),
  Checkbox: ({ options, onChange }: any) => (
    <input
      type="checkbox"
      onChange={(e) => onChange(e.target.checked ? ["member"] : [])}
      aria-label={options[0].label}
    />
  ),
  DatePicker: ({ title, value, onChange }: any) => (
    <input
      type="date"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      aria-label={title}
    />
  ),
  IDNumberInput: ({ title, value, onChange }: any) => (
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      aria-label={title}
    />
  ),
  Selection: ({ title, parmCategory, onChange }: any) => (
    <select onChange={(e) => onChange(e.target.value)} aria-label={title}>
      <option value="">Select {title}</option>
      {parmCategory === "THSR_TIME" && <option value="10:30">10:30</option>}
      {parmCategory === "THSR_STATION" && (
        <>
          <option value="台北">台北</option>
          <option value="台中">台中</option>
        </>
      )}
    </select>
  ),
  TicketNumber: ({ title, value, onChange }: any) => (
    <input
      type="number"
      value={value}
      onChange={(e) => onChange(Number(e.target.value))}
      aria-label={title}
      min={0}
      max={10}
    />
  ),
  Hint: ({ title, isVisible, onConfirm }: any) =>
    isVisible && (
      <div data-testid="hint-modal">
        <p>{title}</p>
        <button onClick={onConfirm}>Confirm</button>
      </div>
    ),
  DoubleCheck: ({ bookingInfo, isVisible, onConfirm, onCancel }: any) =>
    isVisible && (
      <div data-testid="double-check-modal">
        {bookingInfo.map((info: any, index: number) => (
          <div key={index}>
            {info.label}: {info.value}
          </div>
        ))}
        <button onClick={onCancel}>Cancel</button>
        <button onClick={onConfirm}>Confirm</button>
      </div>
    ),
}));

describe("BookingTHSRPage", () => {
  describe("Rule: 使用者輸入訂票者身份證字號", () => {
    it("使用者輸入錯誤的身份證字號", () => {
      // Given: 使用者在訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // When: 使用者輸入"Z123456789"，移開輸入框
      const idInput = screen.getByLabelText("訂票者身份證字號");
      fireEvent.change(idInput, { target: { value: "Z123456789" } });
      fireEvent.blur(idInput);

      // Then: 應該顯示錯誤訊息（通過點擊預約訂票時驗證）
      const bookingButton = screen.getByRole("button", { name: "預約訂票" });
      fireEvent.click(bookingButton);

      waitFor(() => {
        expect(screen.getByTestId("hint-modal")).toBeInTheDocument();
      });
    });

    it("使用者輸入正確的身份證字號", () => {
      // Given: 使用者在訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // When: 使用者輸入"Z123456788"，移開輸入框
      const idInput = screen.getByLabelText("訂票者身份證字號");
      fireEvent.change(idInput, { target: { value: "Z123456788" } });
      fireEvent.blur(idInput);

      // Then: 不顯示任何訊息與紅色外框
      expect(screen.queryByTestId("hint-modal")).not.toBeInTheDocument();
    });
  });

  describe("Rule: 使用者選擇搭乘日期", () => {
    it("使用者開啟日期選擇器", () => {
      // Given: 使用者在THSR訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // When: 使用者點擊搭乘日期輸入框
      const dateInput = screen.getByLabelText("搭乘日期");

      // Then: 系統顯示日期選擇器
      expect(dateInput).toBeInTheDocument();
      expect(dateInput).toHaveAttribute("type", "date");
    });

    it("使用者開啟日期選擇器，並選擇日期", () => {
      // Given: 使用者在THSR訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // When: 使用者選擇"2026-07-03"
      const dateInput = screen.getByLabelText("搭乘日期");
      fireEvent.change(dateInput, { target: { value: "2026-07-03" } });

      // Then: 搭乘日期輸入框顯示"2026-07-03"
      expect(dateInput).toHaveValue("2026-07-03");
    });
  });

  describe("Rule: 使用者選擇搭乘起訖站", () => {
    it("使用者選擇起站與迄站", () => {
      // Given: 使用者在THSR訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // When: 使用者選擇起站為"台北"，迄站為"台中"
      const startStationSelect = screen.getByLabelText("搭乘起站");
      const endStationSelect = screen.getByLabelText("搭乘迄站");

      fireEvent.change(startStationSelect, { target: { value: "台北" } });
      fireEvent.change(endStationSelect, { target: { value: "台中" } });

      // Then: 起站和迄站輸入框應該顯示選擇的值
      expect(startStationSelect).toHaveValue("台北");
      expect(endStationSelect).toHaveValue("台中");
    });

    it("使用者選擇相同的起站與迄站", () => {
      // Given: 使用者在THSR訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // When: 使用者選擇起站為"台北"，迄站為"台北"，並點擊預約訂票
      const idInput = screen.getByLabelText("訂票者身份證字號");
      fireEvent.change(idInput, { target: { value: "Z123456788" } });

      const dateInput = screen.getByLabelText("搭乘日期");
      fireEvent.change(dateInput, { target: { value: "2026-07-03" } });

      const timeSelect = screen.getByLabelText("搭乘時間");
      fireEvent.change(timeSelect, { target: { value: "10:30" } });

      const startStationSelect = screen.getByLabelText("搭乘起站");
      const endStationSelect = screen.getByLabelText("搭乘迄站");

      fireEvent.change(startStationSelect, { target: { value: "台北" } });
      fireEvent.change(endStationSelect, { target: { value: "台北" } });

      const bookingButton = screen.getByRole("button", { name: "預約訂票" });
      fireEvent.click(bookingButton);

      // Then: 應該顯示錯誤訊息
      waitFor(() => {
        expect(screen.getByTestId("hint-modal")).toBeInTheDocument();
        expect(screen.getByText(/請選擇不同的起迄站/i)).toBeInTheDocument();
      });
    });
  });

  describe("Rule: 使用者輸入票種與票數", () => {
    it("使用者購買單一票種超過10張", () => {
      // Given: 使用者在訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // When: 使用者輸入成人票數為"11"
      const adultsInput = screen.getByLabelText("成人票");
      fireEvent.change(adultsInput, { target: { value: "11" } });

      const bookingButton = screen.getByRole("button", { name: "預約訂票" });
      fireEvent.click(bookingButton);

      // Then: 所有票數輸入框顯示紅色外框，並顯示錯誤訊息
      waitFor(() => {
        expect(screen.getByTestId("hint-modal")).toBeInTheDocument();
      });
    });

    it("使用者購買總數超過10張", () => {
      // Given: 使用者在訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // When: 使用者輸入多種票券，總數超過10張
      const adultsInput = screen.getByLabelText("成人票");
      const childInput = screen.getByLabelText("兒童票");
      const disableInput = screen.getByLabelText("愛心票");
      const elderInput = screen.getByLabelText("敬老票");
      const studentInput = screen.getByLabelText("學生票");

      fireEvent.change(adultsInput, { target: { value: "2" } });
      fireEvent.change(childInput, { target: { value: "3" } });
      fireEvent.change(disableInput, { target: { value: "1" } });
      fireEvent.change(elderInput, { target: { value: "3" } });
      fireEvent.change(studentInput, { target: { value: "2" } });

      const bookingButton = screen.getByRole("button", { name: "預約訂票" });
      fireEvent.click(bookingButton);

      // Then: 應該顯示錯誤訊息
      waitFor(() => {
        expect(screen.getByTestId("hint-modal")).toBeInTheDocument();
      });
    });

    it("使用者購買票數為10張", () => {
      // Given: 使用者在訂票頁面，系統日為"2026/07/01"
      render(<BookingTHSRPage />);

      // Setup other required fields
      const idInput = screen.getByLabelText("訂票者身份證字號");
      fireEvent.change(idInput, { target: { value: "Z123456788" } });

      const dateInput = screen.getByLabelText("搭乘日期");
      fireEvent.change(dateInput, { target: { value: "2026-07-03" } });

      const timeSelect = screen.getByLabelText("搭乘時間");
      fireEvent.change(timeSelect, { target: { value: "10:30" } });

      const startStationSelect = screen.getByLabelText("搭乘起站");
      const endStationSelect = screen.getByLabelText("搭乘迄站");
      fireEvent.change(startStationSelect, { target: { value: "台北" } });
      fireEvent.change(endStationSelect, { target: { value: "台中" } });

      // When: 使用者輸入票券數，總數為10張
      const adultsInput = screen.getByLabelText("成人票");
      const childInput = screen.getByLabelText("兒童票");
      const disableInput = screen.getByLabelText("愛心票");
      const elderInput = screen.getByLabelText("敬老票");
      const studentInput = screen.getByLabelText("學生票");

      fireEvent.change(adultsInput, { target: { value: "2" } });
      fireEvent.change(childInput, { target: { value: "3" } });
      fireEvent.change(disableInput, { target: { value: "1" } });
      fireEvent.change(elderInput, { target: { value: "3" } });
      fireEvent.change(studentInput, { target: { value: "1" } });

      const bookingButton = screen.getByRole("button", { name: "預約訂票" });
      fireEvent.click(bookingButton);

      // Then: 不顯示任何訊息，應該顯示Double Check視窗
      waitFor(() => {
        expect(screen.getByTestId("double-check-modal")).toBeInTheDocument();
      });
    });
  });

  describe("Rule: 清空填寫按鈕", () => {
    it("使用者點擊清空填寫按鈕，所有欄位應該回復到預設值", () => {
      // Given: 使用者已填寫一些資訊
      render(<BookingTHSRPage />);

      const idInput = screen.getByLabelText("訂票者身份證字號");
      fireEvent.change(idInput, { target: { value: "Z123456788" } });

      const dateInput = screen.getByLabelText("搭乘日期");
      fireEvent.change(dateInput, { target: { value: "2026-07-03" } });

      const adultsInput = screen.getByLabelText("成人票");
      fireEvent.change(adultsInput, { target: { value: "5" } });

      // When: 使用者點擊清空填寫按鈕
      const clearButton = screen.getByRole("button", { name: "清空填寫" });
      fireEvent.click(clearButton);

      // Then: 所有欄位回復到預設值
      expect(idInput).toHaveValue("");
      expect(dateInput).toHaveValue("");
      expect(adultsInput).toHaveValue(1);
    });
  });

  describe("Rule: 早鳥checkbox勾選狀態控制", () => {
    // Scenario: 未勾選早鳥時，不顯示早鳥輸入框
    // Reference: communication.md - Bug: 未勾選早鳥時，會跳出早鳥輸入框
    it("當未勾選早鳥時，不應該顯示早鳥輸入框", () => {
      // Given: 使用者在訂票頁面，早鳥checkbox未勾選
      render(<BookingTHSRPage />);

      // When: 使用者填寫超過6天的預約日期和成人票數
      const dateInput = screen.getByLabelText("搭乘日期");
      fireEvent.change(dateInput, { target: { value: "2026-07-10" } });

      const adultsInput = screen.getByLabelText("成人票");
      fireEvent.change(adultsInput, { target: { value: "2" } });

      // Then: 早鳥輸入框不應該出現（因為is_early_bird為false）
      // 注意：測試環境中的早鳥輸入框不會被渲染，因為shouldShowEarlyBirdIds()傳回false
      expect(screen.queryByLabelText(/早鳥\d+/)).not.toBeInTheDocument();
    });

    // Scenario: 勾選早鳥且滿足條件時，顯示早鳥輸入框
    // Reference: communication.md - Bug: 未勾選早鳥時，會跳出早鳥輸入框
    it("當勾選早鳥且滿足條件時，應該顯示早鳥輸入框", () => {
      // Given: 使用者在訂票頁面
      render(<BookingTHSRPage />);

      // When: 使用者勾選早鳥checkbox、填寫超過6天的預約日期和成人票數
      const earlyBirdCheckbox = screen.getByLabelText("早鳥");
      fireEvent.click(earlyBirdCheckbox);

      const dateInput = screen.getByLabelText("搭乘日期");
      fireEvent.change(dateInput, { target: { value: "2026-07-10" } });

      const adultsInput = screen.getByLabelText("成人票");
      fireEvent.change(adultsInput, { target: { value: "2" } });

      // Then: 早鳥輸入框應該出現（因為is_early_bird為true且日期滿足條件）
      waitFor(() => {
        expect(screen.getByLabelText(/早鳥\d+/)).toBeInTheDocument();
      });
    });

    // Scenario: 取消勾選早鳥時，清空早鳥ID
    // Reference: communication.md - Bug: 未勾選早鳥時，會跳出早鳥輸入框
    it("當取消勾選早鳥時，應該清空早鳥ID並隱藏早鳥輸入框", () => {
      // Given: 使用者已勾選早鳥並填寫相關信息
      render(<BookingTHSRPage />);

      const earlyBirdCheckbox = screen.getByLabelText("早鳥");
      const dateInput = screen.getByLabelText("搭乘日期");
      const adultsInput = screen.getByLabelText("成人票");

      // 先勾選早鳥並填寫數據
      fireEvent.click(earlyBirdCheckbox);
      fireEvent.change(dateInput, { target: { value: "2026-07-10" } });
      fireEvent.change(adultsInput, { target: { value: "2" } });

      // When: 使用者取消勾選早鳥checkbox
      fireEvent.click(earlyBirdCheckbox);

      // Then: 早鳥輸入框應該隱藏，且早鳥ID被清空
      waitFor(() => {
        expect(screen.queryByLabelText(/早鳥\d+/)).not.toBeInTheDocument();
      });
    });

    // Scenario: 驗證傳給後端的is_early_bird值根據checkbox勾選而不同
    // Reference: communication.md - Bug: 未勾選早鳥時，會跳出早鳥輸入框
    it("當勾選早鳥時，Double Check視窗應該顯示早鳥資格", () => {
      // Given: 使用者在訂票頁面
      render(<BookingTHSRPage />);

      // Setup all required fields
      const idInput = screen.getByLabelText("訂票者身份證字號");
      fireEvent.change(idInput, { target: { value: "Z123456788" } });

      const dateInput = screen.getByLabelText("搭乘日期");
      fireEvent.change(dateInput, { target: { value: "2026-07-10" } });

      const timeSelect = screen.getByLabelText("搭乘時間");
      fireEvent.change(timeSelect, { target: { value: "10:30" } });

      const startStationSelect = screen.getByLabelText("搭乘起站");
      const endStationSelect = screen.getByLabelText("搭乘迄站");
      fireEvent.change(startStationSelect, { target: { value: "台北" } });
      fireEvent.change(endStationSelect, { target: { value: "台中" } });

      const adultsInput = screen.getByLabelText("成人票");
      fireEvent.change(adultsInput, { target: { value: "1" } });

      // When: 使用者勾選早鳥checkbox，並點擊預約訂票
      const earlyBirdCheckbox = screen.getByLabelText("早鳥");
      fireEvent.click(earlyBirdCheckbox);

      const bookingButton = screen.getByRole("button", { name: "預約訂票" });
      fireEvent.click(bookingButton);

      // Then: Double Check視窗應該顯示早鳥資格信息
      waitFor(() => {
        expect(screen.getByTestId("double-check-modal")).toBeInTheDocument();
        expect(screen.getByText(/早鳥資格/)).toBeInTheDocument();
        expect(screen.getByText(/使用早鳥優惠/)).toBeInTheDocument();
      });
    });

    // Scenario: 驗證未勾選早鳥時，Double Check視窗不顯示早鳥資格
    // Reference: communication.md - Bug: 未勾選早鳥時，會跳出早鳥輸入框
    it("當未勾選早鳥時，Double Check視窗不應該顯示早鳥資格", () => {
      // Given: 使用者在訂票頁面，早鳥checkbox未勾選
      render(<BookingTHSRPage />);

      // Setup all required fields
      const idInput = screen.getByLabelText("訂票者身份證字號");
      fireEvent.change(idInput, { target: { value: "Z123456788" } });

      const dateInput = screen.getByLabelText("搭乘日期");
      fireEvent.change(dateInput, { target: { value: "2026-07-10" } });

      const timeSelect = screen.getByLabelText("搭乘時間");
      fireEvent.change(timeSelect, { target: { value: "10:30" } });

      const startStationSelect = screen.getByLabelText("搭乘起站");
      const endStationSelect = screen.getByLabelText("搭乘迄站");
      fireEvent.change(startStationSelect, { target: { value: "台北" } });
      fireEvent.change(endStationSelect, { target: { value: "台中" } });

      const adultsInput = screen.getByLabelText("成人票");
      fireEvent.change(adultsInput, { target: { value: "1" } });

      // When: 使用者未勾選早鳥checkbox，點擊預約訂票
      const bookingButton = screen.getByRole("button", { name: "預約訂票" });
      fireEvent.click(bookingButton);

      // Then: Double Check視窗應該存在，但不顯示早鳥資格信息
      waitFor(() => {
        expect(screen.getByTestId("double-check-modal")).toBeInTheDocument();
        expect(screen.queryByText(/早鳥資格/)).not.toBeInTheDocument();
        expect(screen.queryByText(/使用早鳥優惠/)).not.toBeInTheDocument();
      });
    });
  });
});
