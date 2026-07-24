import React, { useState } from "react";
import Checkbox from "../components/Checkbox/Checkbox";
import TicketNumber from "../components/TicketNumber/TicketNumber";
import Selection from "../components/Selection/Selection";
import Button from "../components/Button/Button";
import "./home-page.css";

type NavKey = "home" | "thsr" | "tra" | "search";

const HomePage: React.FC = () => {
  const [activeSection, setActiveSection] = useState<NavKey>("home");
  const [selectedTicketTags, setSelectedTicketTags] = useState<string>("");
  const [ticketCount, setTicketCount] = useState<number>(0);
  const [selectedStation, setSelectedStation] = useState<string>("");
  const [buttonClickCount, setButtonClickCount] = useState<number>(0);

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

    if (activeSection === "search") {
      return (
        <div className="home-page__component-showcase">
          <div className="home-page__checkbox-demo">
            <h2 className="home-page__checkbox-demo-title">
              Checkbox Component 展示
            </h2>
            <p className="home-page__checkbox-demo-description">
              請勾選適用的票種，元件會回傳逗號分隔字串。
            </p>

            <Checkbox
              required
              options={
                [
                  {
                    label: "早鳥優惠",
                    value: "EARLY_BIRD",
                    icon: "/icons/bird.png",
                  },
                  {
                    label: "學生票",
                    value: "STUDENT",
                    icon: "/icons/students.png",
                  },
                  {
                    label: "敬老票",
                    value: "ELDERLY",
                    icon: "/icons/elderly.png",
                  },
                ] as const
              }
              onChange={setSelectedTicketTags}
            />

            <p
              className="home-page__checkbox-demo-result"
              data-testid="checkbox-result"
            >
              目前回傳值: {selectedTicketTags || ""}
            </p>
          </div>

          <div className="home-page__ticket-number-demo">
            <h2 className="home-page__ticket-number-title">
              Ticket Number Component 展示
            </h2>
            <p className="home-page__ticket-number-description">
              請輸入購買票數，元件會以 number 型別回傳。
            </p>

            <TicketNumber
              title="成人票"
              iconSrc="/icons/people.png"
              min={0}
              max={10}
              value={ticketCount}
              onChange={setTicketCount}
            />

            <p
              className="home-page__ticket-number-result"
              data-testid="ticket-number-result"
            >
              目前回傳值: {ticketCount}
            </p>
          </div>

          <div className="home-page__selection-demo">
            <h2 className="home-page__selection-demo-title">
              Selection Component 展示
            </h2>
            <p className="home-page__selection-demo-description">
              請選擇搭乘起站，元件會回傳選擇的value值。
            </p>

            <Selection
              iconSrc="/icons/time-planning.png"
              title="搭乘起站"
              parmCategory="THSR_STATION"
              required
              onChange={setSelectedStation}
            />

            <p
              className="home-page__selection-demo-result"
              data-testid="selection-result"
            >
              目前回傳值: {selectedStation}
            </p>
          </div>

          <div className="home-page__button-demo">
            <h2 className="home-page__button-demo-title">
              Button Component 展示
            </h2>
            <p className="home-page__button-demo-description">
              點選按鈕會觸發OnClick事件並累加點選次數。
            </p>

            <Button
              title="送出"
              icon="/icons/checked.png"
              onClick={() => setButtonClickCount((count) => count + 1)}
            />

            <p
              className="home-page__button-demo-result"
              data-testid="button-result"
            >
              目前點選次數: {buttonClickCount}
            </p>
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
