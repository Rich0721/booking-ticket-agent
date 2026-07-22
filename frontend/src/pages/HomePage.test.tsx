import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import HomePage from "./HomePage";

describe("HomePage", () => {
  it("renders the hero section and header navigation", () => {
    render(<HomePage />);

    expect(screen.getByText("Auto Booking")).toBeInTheDocument();
    expect(screen.getByText("THSR")).toBeInTheDocument();
    expect(screen.getByText("TRA")).toBeInTheDocument();
    expect(screen.getByText("Search")).toBeInTheDocument();
    expect(screen.getByText("Welcome To Auto Booking")).toBeInTheDocument();
    expect(
      screen.getByText(/這是一個練習使用Github Copilot的專案/i),
    ).toBeInTheDocument();
    expect(screen.getByAltText("Taiwan map")).toBeInTheDocument();
    expect(screen.getByAltText("Tech stack icon")).toBeInTheDocument();
  });

  it("switches the content view and disables the selected nav item", () => {
    render(<HomePage />);

    const thsrButton = screen.getByRole("button", { name: "THSR" });
    fireEvent.click(thsrButton);

    expect(screen.getByText("作業中..")).toBeInTheDocument();
    expect(thsrButton).toBeDisabled();
  });
});
