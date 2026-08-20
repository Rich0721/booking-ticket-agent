import React, { useCallback, useState } from "react";
import {
  Button,
  Checkbox,
  DatePicker,
  DoubleCheck,
  Hint,
  IDNumberInput,
  Selection,
  TicketNumber,
} from "../components";
import { ISelectionOption } from "../interfaces/ISelection";
import "./booking-thsr-page.css";

interface BookingFormData {
  user_id: string;
  is_member: boolean;
  is_early_bird: boolean;
  booking_date: string;
  booking_time: string;
  start_station: string;
  end_station: string;
  adults: number;
  childs: number;
  elders: number;
  disables: number;
  students: number;
  early_ids: string[];
}

interface ValidationError {
  field: string;
  message: string;
}

export const BookingTHSRPage: React.FC = () => {
  const [formData, setFormData] = useState<BookingFormData>({
    user_id: "",
    is_member: false,
    is_early_bird: false,
    booking_date: "",
    booking_time: "",
    start_station: "",
    end_station: "",
    adults: 1,
    childs: 0,
    elders: 0,
    disables: 0,
    students: 0,
    early_ids: [],
  });

  const [hintVisible, setHintVisible] = useState(false);
  const [hintMessage, setHintMessage] = useState("");
  const [doubleCheckVisible, setDoubleCheckVisible] = useState(false);
  const [hintType, setHintType] = useState<"info" | "warning">("warning");

  // 用於緩存Selection的選項，以便在generateBookingInfo中查詢label
  const [selectionOptionsCache, setSelectionOptionsCache] = useState<
    Record<string, ISelectionOption[]>
  >({});

  // 處理Selection選項加載，緩存選項供後續lookup使用
  // 使用useCallback來記憶化函數引用，避免在父組件重新渲染時
  // 導致Selection Component的useEffect被重複觸發而發起重複的API調用
  const handleSelectionOptionsLoad = useCallback(
    (parmCategory: string, options: ISelectionOption[]) => {
      setSelectionOptionsCache((prev) => ({
        ...prev,
        [parmCategory]: options,
      }));
    },
    [],
  );

  // 根據parmCategory和value查詢對應的label
  const getLabelByValue = (parmCategory: string, value: string): string => {
    const options = selectionOptionsCache[parmCategory] || [];
    const option = options.find((opt) => opt.parm_value === value);
    return option ? option.parm_name : value;
  };

  // 計算系統日期（模擬）
  const getSystemDate = (): Date => {
    return new Date("2026-07-01");
  };

  // 計算預約日期與系統日期的差值（天數）
  const getDaysDifference = (bookingDate: string): number => {
    const systemDate = getSystemDate();
    const booking = new Date(bookingDate);
    const diffTime = booking.getTime() - systemDate.getTime();
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  // 檢查是否需要顯示早鳥ID輸入框
  const shouldShowEarlyBirdIds = (): boolean => {
    // 必須勾選早鳥checkbox才能顯示早鳥輸入框
    if (!formData.is_early_bird) {
      return false;
    }
    if (!formData.booking_date || formData.adults === 0) {
      return false;
    }
    const dayDiff = getDaysDifference(formData.booking_date);
    return dayDiff >= 6;
  };

  // 獲取應該顯示的早鳥ID輸入框數量
  const getEarlyBirdCount = (): number => {
    if (!shouldShowEarlyBirdIds()) {
      return 0;
    }
    return formData.adults;
  };

  // 驗證身份證字號格式
  const validateIdNumber = (id: string): boolean => {
    if (!id) return false;
    const idRegex = /^[A-Z]\d{9}$/;
    return idRegex.test(id);
  };

  // 驗證表單
  const validateForm = (): ValidationError[] => {
    const errors: ValidationError[] = [];

    // 檢查必填字段
    if (!formData.user_id) {
      errors.push({ field: "user_id", message: "請輸入訂票者身份證字號" });
    } else if (!validateIdNumber(formData.user_id)) {
      errors.push({ field: "user_id", message: "請輸入正確的身份證字號" });
    }

    if (!formData.booking_date) {
      errors.push({ field: "booking_date", message: "請選擇搭乘日期" });
    }

    if (!formData.booking_time) {
      errors.push({ field: "booking_time", message: "請選擇搭乘時間" });
    }

    if (!formData.start_station) {
      errors.push({ field: "start_station", message: "請選擇搭乘起站" });
    }

    if (!formData.end_station) {
      errors.push({ field: "end_station", message: "請選擇搭乘迄站" });
    }

    // 檢查起迄站是否相同
    if (
      formData.start_station &&
      formData.end_station &&
      formData.start_station === formData.end_station
    ) {
      errors.push({ field: "stations", message: "請選擇不同的起迄站" });
    }

    // 檢查票券總數
    const totalTickets =
      formData.adults +
      formData.childs +
      formData.elders +
      formData.disables +
      formData.students;
    if (totalTickets > 10) {
      errors.push({ field: "tickets", message: "單一訂單最多可訂購10張" });
    }

    // 檢查是否有任何訂票資訊
    if (totalTickets === 0) {
      errors.push({ field: "tickets", message: "請輸入訂票資訊" });
    }

    // 檢查早鳥ID
    if (shouldShowEarlyBirdIds()) {
      // 檢查早鳥ID是否填寫完整
      const earlyBirdCount = getEarlyBirdCount();
      if (formData.early_ids.length < earlyBirdCount) {
        errors.push({ field: "early_ids", message: "請填寫所有早鳥ID" });
      }

      // 檢查早鳥ID格式
      for (let i = 0; i < formData.early_ids.length; i++) {
        const earlyId = formData.early_ids[i];
        if (!validateIdNumber(earlyId)) {
          errors.push({
            field: `early_id_${i}`,
            message: "請輸入正確的身份證字號",
          });
        }
      }

      // 檢查早鳥ID是否重複
      const uniqueEarlyIds = new Set(formData.early_ids);
      if (uniqueEarlyIds.size !== formData.early_ids.length) {
        errors.push({ field: "early_ids", message: "早鳥ID不可重複" });
      }
    }

    return errors;
  };

  // 處理字段變更
  const handleFieldChange = <K extends keyof BookingFormData>(
    field: K,
    value: BookingFormData[K],
  ) => {
    setFormData((prev) => {
      const updated = { ...prev, [field]: value };

      // 當is_early_bird被取消勾選時，清空早鳥ID
      if (field === "is_early_bird" && !value) {
        updated.early_ids = [];
      }

      // 當成人票數變更時，調整早鳥ID數組
      if (field === "adults") {
        const newAdultCount = value as number;
        const currentEarlyIds = updated.early_ids;
        if (newAdultCount > currentEarlyIds.length) {
          // 增加空的早鳥ID
          updated.early_ids = [
            ...currentEarlyIds,
            ...Array(newAdultCount - currentEarlyIds.length).fill(""),
          ];
        } else if (newAdultCount < currentEarlyIds.length) {
          // 刪除多餘的早鳥ID
          updated.early_ids = currentEarlyIds.slice(0, newAdultCount);
        }
      }

      return updated;
    });
  };

  // 處理早鳥ID變更
  const handleEarlyIdChange = (index: number, value: string) => {
    const newEarlyIds = [...formData.early_ids];
    newEarlyIds[index] = value;
    handleFieldChange("early_ids", newEarlyIds);
  };

  // 清空所有字段
  const handleClearForm = () => {
    setFormData({
      user_id: "",
      is_member: false,
      is_early_bird: false,
      booking_date: "",
      booking_time: "",
      start_station: "",
      end_station: "",
      adults: 1,
      childs: 0,
      elders: 0,
      disables: 0,
      students: 0,
      early_ids: [],
    });
    setHintVisible(false);
    setHintMessage("");
    setHintType("warning");
    setDoubleCheckVisible(false);
  };

  // 處理預約訂票按鈕點擊
  const handleBooking = () => {
    const errors = validateForm();
    if (errors.length > 0) {
      const errorMessage = errors[0].message;
      setHintMessage(errorMessage);
      setHintType("warning");
      setHintVisible(true);
    } else {
      // 顯示Double Check確認視窗
      setDoubleCheckVisible(true);
    }
  };

  // 處理提交預約
  const handleConfirmBooking = async () => {
    // 準備API請求資料
    const requestData = {
      user_id: formData.user_id,
      ticket_type: "THSR",
      booking_date: formData.booking_date,
      booking_time: formData.booking_time,
      start_station: formData.start_station,
      end_station: formData.end_station,
      adults: formData.adults,
      childs: formData.childs,
      students: formData.students,
      elders: formData.elders,
      disables: formData.disables,
      is_early_bird: formData.is_early_bird,
      is_member: formData.is_member,
      early_ids: formData.early_ids,
    };

    try {
      // 呼叫API
      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL || "http://localhost:8000"}/booking-ticket`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        },
      );

      if (response.ok) {
        // 成功提交
        setHintMessage("預約訂票成功！");
        setHintType("info");
        setHintVisible(true);
        setDoubleCheckVisible(false);
        // 延遲後清空表單
        setTimeout(() => {
          handleClearForm();
        }, 2000);
      } else {
        // 提交失敗
        setHintMessage("預約訂票失敗，請稍後重試");
        setHintType("warning");
        setHintVisible(true);
        setDoubleCheckVisible(false);
      }
    } catch (error) {
      setHintMessage("預約訂票出現錯誤，請稍後重試");
      setHintType("warning");
      setHintVisible(true);
      setDoubleCheckVisible(false);
    }
  };

  // 產生Double Check資訊
  const generateBookingInfo = () => {
    const bookingInfo = [
      { label: "訂票者身份證字號", value: formData.user_id },
      { label: "搭乘日期", value: formData.booking_date },
      {
        label: "搭乘時間",
        value: getLabelByValue("THSR_TIME", formData.booking_time),
      },
      {
        label: "搭乘起站",
        value: getLabelByValue("THSR_STATION", formData.start_station),
      },
      {
        label: "搭乘迄站",
        value: getLabelByValue("THSR_STATION", formData.end_station),
      },
      { label: "成人票", value: `${formData.adults}張` },
      { label: "兒童票", value: `${formData.childs}張` },
      { label: "敬老票", value: `${formData.elders}張` },
      { label: "愛心票", value: `${formData.disables}張` },
      { label: "學生票", value: `${formData.students}張` },
    ];

    if (formData.is_member) {
      bookingInfo.push({ label: "會員資格", value: "使用高鐵會員" });
    }

    if (formData.is_early_bird) {
      bookingInfo.push({ label: "早鳥資格", value: "使用早鳥優惠" });
      formData.early_ids.forEach((id, index) => {
        if (id) {
          bookingInfo.push({ label: `早鳥${index + 1}`, value: id });
        }
      });
    }

    return bookingInfo;
  };

  return (
    <div className="page">
      {/* 主區：左側地圖 + 右側表單 */}
      <div className="main">
        {/* 左側：台灣地圖 */}
        <div className="sidebar">
          <img src="/images/taiwan.png" alt="Taiwan map" />
        </div>

        {/* 右側：訂票表單 */}
        <div className="form-area">
          {/* 第一列：身份證字號 ＋ 會員/早鳥 */}
          <div className="row">
            <div className="field" style={{ flex: "1" }}>
              <IDNumberInput
                title="訂票者身份證字號"
                value={formData.user_id}
                onChange={(value) => handleFieldChange("user_id", value)}
                onBlur={() => {}}
              />
            </div>
            <div className="member-group" style={{ flex: "1" }}>
              <Checkbox
                options={[
                  {
                    label: "會員",
                    value: "member",
                    defaultChecked: formData.is_member,
                    icon: "/icons/membership.png",
                  },
                ]}
                onChange={(selected) =>
                  handleFieldChange("is_member", selected.includes("member"))
                }
              />
              <Checkbox
                options={[
                  {
                    label: "早鳥",
                    value: "early",
                    defaultChecked: formData.is_early_bird,
                  },
                ]}
                onChange={(selected) =>
                  handleFieldChange("is_early_bird", selected.includes("early"))
                }
              />
            </div>
          </div>

          {/* 第二列：搭乘日期 ＋ 搭乘時間 */}
          <div className="row">
            <div className="field">
              <DatePicker
                title="搭乘日期"
                value={formData.booking_date}
                onChange={(value) => handleFieldChange("booking_date", value)}
              />
            </div>
            <div className="field">
              <Selection
                title="搭乘時間"
                iconSrc="/icons/clock.png"
                parmCategory="THSR_TIME"
                value={formData.booking_time}
                onChange={(value) => handleFieldChange("booking_time", value)}
                onOptionsLoad={(options) =>
                  handleSelectionOptionsLoad("THSR_TIME", options)
                }
              />
            </div>
          </div>

          {/* 第三列：搭乘起站 ＋ 搭乘迄站 */}
          <div className="row">
            <div className="field">
              <Selection
                title="搭乘起站"
                iconSrc="/icons/transport.png"
                parmCategory="THSR_STATION"
                value={formData.start_station}
                onChange={(value) => handleFieldChange("start_station", value)}
                onOptionsLoad={(options) =>
                  handleSelectionOptionsLoad("THSR_STATION", options)
                }
              />
            </div>
            <div className="field">
              <Selection
                title="搭乘迄站"
                iconSrc="/icons/transport.png"
                parmCategory="THSR_STATION"
                value={formData.end_station}
                onChange={(value) => handleFieldChange("end_station", value)}
                onOptionsLoad={(options) =>
                  handleSelectionOptionsLoad("THSR_STATION", options)
                }
              />
            </div>
          </div>

          {/* 票種選擇（5 種票） */}
          <div className="tickets">
            <div className="ticket">
              <span>成人票</span>
              <TicketNumber
                title="成人票"
                iconSrc="/icons/people.png"
                min={0}
                max={10}
                value={formData.adults}
                onChange={(value) => handleFieldChange("adults", value)}
              />
            </div>
            <div className="ticket">
              <span>兒童票</span>
              <TicketNumber
                title="兒童票"
                iconSrc="/icons/children.png"
                min={0}
                max={10}
                value={formData.childs}
                onChange={(value) => handleFieldChange("childs", value)}
              />
            </div>
            <div className="ticket">
              <span>敬老票</span>
              <TicketNumber
                title="敬老票"
                iconSrc="/icons/elderly.png"
                min={0}
                max={10}
                value={formData.elders}
                onChange={(value) => handleFieldChange("elders", value)}
              />
            </div>
            <div className="ticket">
              <span>愛心票</span>
              <TicketNumber
                title="愛心票"
                iconSrc="/icons/disabled.png"
                min={0}
                max={10}
                value={formData.disables}
                onChange={(value) => handleFieldChange("disables", value)}
              />
            </div>
            <div className="ticket">
              <span>學生票</span>
              <TicketNumber
                title="學生票"
                iconSrc="/icons/students.png"
                min={0}
                max={10}
                value={formData.students}
                onChange={(value) => handleFieldChange("students", value)}
              />
            </div>
          </div>

          {/* 早鳥區（2 欄 × n 列） */}
          {shouldShowEarlyBirdIds() && (
            <div className="early-bird">
              {Array.from({ length: getEarlyBirdCount() }).map((_, index) => (
                <div key={`early_id_${index}`} className="eb-row">
                  <IDNumberInput
                    title={`早鳥${index + 1}`}
                    value={formData.early_ids[index] || ""}
                    onChange={(value) => handleEarlyIdChange(index, value)}
                    onBlur={() => {}}
                  />
                </div>
              ))}
            </div>
          )}

          {/* 底部按鈕 */}
          <div className="actions">
            <Button
              title="清空填寫"
              icon="/icons/school.png"
              buttonColor="#FFCCCC"
              selectedColor="#f73f3f"
              buttonSize="medium"
              onClick={handleClearForm}
            />
            <Button
              title="預約訂票"
              icon="/icons/checked.png"
              buttonColor="#a7fdb9"
              selectedColor="#59fa59"
              buttonSize="medium"
              onClick={handleBooking}
            />
          </div>
        </div>
      </div>

      <Hint
        title={hintMessage}
        type={hintType}
        isVisible={hintVisible}
        onConfirm={() => setHintVisible(false)}
      />

      <DoubleCheck
        bookingInfo={generateBookingInfo()}
        isVisible={doubleCheckVisible}
        onCancel={() => setDoubleCheckVisible(false)}
        onConfirm={handleConfirmBooking}
      />
    </div>
  );
};

export default BookingTHSRPage;
