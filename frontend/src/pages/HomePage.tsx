import React, { useState } from "react";
import "./home-page.css";

type NavKey = "home" | "thsr" | "tra" | "search";

const HomePage: React.FC = () => {
  const [activeSection, setActiveSection] = useState<NavKey>("home");

  const renderContent = () => {
    if (activeSection === "home") {
      return (
        <div className="home-page__hero">
          <div className="home-page__image-panel">
            <img src="/images/taiwan.png" alt="Taiwan map" />
          </div>

          <div className="home-page__text-panel">
            <h1 className="home-page__title">Welcome To Auto Booking</h1>
            <p className="home-page__description">
              這是一個練習使用Github Copilot的專案，主要透過需求文件和Custom
              Agent的方式完成高鐵與台鐵自動訂票的功能，並且可以透過查詢功能查詢訂票結果。
            </p>

            <div
              className="home-page__tech-stack"
              aria-label="tech stack icons"
            >
              <img src="/images/tech-icons.png" alt="Tech stack icon" />
            </div>
          </div>
        </div>
      );
    }

    return (
      <div className="home-page__placeholder">
        <p>作業中..</p>
      </div>
    );
  };

  return (
    <div className="home-page">
      <header className="home-page__header">
        <div className="home-page__header-band home-page__header-band--tra" />
        <div className="home-page__header-band home-page__header-band--thsr" />

        <div className="home-page__header-content">
          <button
            className="home-page__logo"
            type="button"
            onClick={() => setActiveSection("home")}
          >
            Auto Booking
          </button>

          <nav className="home-page__nav" aria-label="primary navigation">
            <button
              className={`home-page__nav-button ${activeSection === "thsr" ? "home-page__nav-button--active" : ""}`}
              type="button"
              onClick={() => setActiveSection("thsr")}
              disabled={activeSection === "thsr"}
            >
              THSR
            </button>
            <button
              className={`home-page__nav-button ${activeSection === "tra" ? "home-page__nav-button--active" : ""}`}
              type="button"
              onClick={() => setActiveSection("tra")}
              disabled={activeSection === "tra"}
            >
              TRA
            </button>
            <button
              className={`home-page__nav-button ${activeSection === "search" ? "home-page__nav-button--active" : ""}`}
              type="button"
              onClick={() => setActiveSection("search")}
              disabled={activeSection === "search"}
            >
              Search
            </button>
          </nav>
        </div>
      </header>

      <main className="home-page__content">{renderContent()}</main>
    </div>
  );
};

export default HomePage;
