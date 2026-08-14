import React, { useState } from "react";
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
import "./booking-thsr-page.css";

interface BookingFormData {
  user_id: string;
  is_member: boolean;
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

interface FieldErrors {
  [key: string]: boolean;
}

export const BookingTHSRPage: React.FC = () => {
  const [formData, setFormData] = useState<BookingFormData>({
    user_id: "",
    is_member: false,
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

  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [hintVisible, setHintVisible] = useState(false);
  const [hintMessage, setHintMessage] = useState("");
  const [doubleCheckVisible, setDoubleCheckVisible] = useState(false);
  const [hintType, setHintType] = useState<"info" | "warning">("warning");

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
    const errorFields: FieldErrors = {};

    // 檢查必填字段
    if (!formData.user_id) {
      errors.push({ field: "user_id", message: "請輸入訂票者身份證字號" });
      errorFields.user_id = true;
    } else if (!validateIdNumber(formData.user_id)) {
      errors.push({ field: "user_id", message: "請輸入正確的身份證字號" });
      errorFields.user_id = true;
    }

    if (!formData.booking_date) {
      errors.push({ field: "booking_date", message: "請選擇搭乘日期" });
      errorFields.booking_date = true;
    }

    if (!formData.booking_time) {
      errors.push({ field: "booking_time", message: "請選擇搭乘時間" });
      errorFields.booking_time = true;
    }

    if (!formData.start_station) {
      errors.push({ field: "start_station", message: "請選擇搭乘起站" });
      errorFields.start_station = true;
    }

    if (!formData.end_station) {
      errors.push({ field: "end_station", message: "請選擇搭乘迄站" });
      errorFields.end_station = true;
    }

    // 檢查起迄站是否相同
    if (
      formData.start_station &&
      formData.end_station &&
      formData.start_station === formData.end_station
    ) {
      errors.push({ field: "stations", message: "請選擇不同的起迄站" });
      errorFields.start_station = true;
      errorFields.end_station = true;
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
      errorFields.adults = true;
      errorFields.childs = true;
      errorFields.elders = true;
      errorFields.disables = true;
      errorFields.students = true;
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
        for (let i = 0; i < earlyBirdCount; i++) {
          errorFields[`early_id_${i}`] = true;
        }
      }

      // 檢查早鳥ID格式
      for (let i = 0; i < formData.early_ids.length; i++) {
        const earlyId = formData.early_ids[i];
        if (!validateIdNumber(earlyId)) {
          errors.push({
            field: `early_id_${i}`,
            message: "請輸入正確的身份證字號",
          });
          errorFields[`early_id_${i}`] = true;
        }
      }

      // 檢查早鳥ID是否重複
      const uniqueEarlyIds = new Set(formData.early_ids);
      if (uniqueEarlyIds.size !== formData.early_ids.length) {
        errors.push({ field: "early_ids", message: "早鳥ID不可重複" });
        formData.early_ids.forEach((_, i) => {
          errorFields[`early_id_${i}`] = true;
        });
      }
    }

    setFieldErrors(errorFields);
    return errors;
  };

  // 處理字段變更
  const handleFieldChange = <K extends keyof BookingFormData>(
    field: K,
    value: BookingFormData[K],
  ) => {
    setFormData((prev) => {
      const updated = { ...prev, [field]: value };

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

      // 清除該字段的錯誤標記
      setFieldErrors((prev) => {
        const updated = { ...prev };
        delete updated[field as string];
        return updated;
      });

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
    setFieldErrors({});
    setHintVisible(false);
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
      info: {
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
        is_early_bird: shouldShowEarlyBirdIds(),
        is_member: formData.is_member,
        early_ids: formData.early_ids,
      },
    };

    try {
      // 呼叫API
      const response = await fetch("/booking-ticket", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

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
      { label: "搭乘時間", value: formData.booking_time },
      { label: "搭乘起站", value: formData.start_station },
      { label: "搭乘迄站", value: formData.end_station },
      { label: "成人票", value: `${formData.adults}張` },
      { label: "兒童票", value: `${formData.childs}張` },
      { label: "敬老票", value: `${formData.elders}張` },
      { label: "愛心票", value: `${formData.disables}張` },
      { label: "學生票", value: `${formData.students}張` },
    ];

    if (formData.is_member) {
      bookingInfo.push({ label: "會員資格", value: "使用高鐵會員" });
    }

    if (shouldShowEarlyBirdIds() && formData.early_ids.length > 0) {
      formData.early_ids.forEach((id, index) => {
        if (id) {
          bookingInfo.push({ label: `早鳥${index + 1}`, value: id });
        }
      });
    }

    return bookingInfo;
  };

  return (
    <div className="booking-thsr-page">
      <div className="booking-form-container">
        <h1>高鐵預約訂票</h1>

        <div className="form-section">
          <IDNumberInput
            title="訂票者身份證字號"
            value={formData.user_id}
            onChange={(value) => handleFieldChange("user_id", value)}
            onBlur={() => {}}
          />
          {fieldErrors.user_id && <div className="error-indicator" />}
        </div>

        <div className="form-section">
          <Checkbox
            options={[
              {
                label: "使用高鐵會員",
                value: "member",
                defaultChecked: false,
                icon: "/icons/membership.png",
              },
            ]}
            onChange={(selected) =>
              handleFieldChange("is_member", selected.includes("member"))
            }
          />
        </div>

        <div className="form-section">
          <DatePicker
            title="搭乘日期"
            value={formData.booking_date}
            onChange={(value) => handleFieldChange("booking_date", value)}
          />
          {fieldErrors.booking_date && <div className="error-indicator" />}
        </div>

        <div className="form-section">
          <Selection
            title="搭乘時間"
            iconSrc="/icons/clock.png"
            parmCategory="THSR_TIME"
            onChange={(value) => handleFieldChange("booking_time", value)}
          />
          {fieldErrors.booking_time && <div className="error-indicator" />}
        </div>

        <div className="form-row">
          <div className="form-section">
            <Selection
              title="搭乘起站"
              iconSrc="/icons/transport.png"
              parmCategory="THSR_STATION"
              onChange={(value) => handleFieldChange("start_station", value)}
            />
            {fieldErrors.start_station && <div className="error-indicator" />}
          </div>
          <div className="form-section">
            <Selection
              title="搭乘迄站"
              iconSrc="/icons/transport.png"
              parmCategory="THSR_STATION"
              onChange={(value) => handleFieldChange("end_station", value)}
            />
            {fieldErrors.end_station && <div className="error-indicator" />}
          </div>
        </div>

        <div className="ticket-section">
          <h3>購買票券數量</h3>
          <div className="ticket-grid">
            <div className="ticket-item">
              <TicketNumber
                title="成人票"
                iconSrc="/icons/people.png"
                min={0}
                max={10}
                value={formData.adults}
                onChange={(value) => handleFieldChange("adults", value)}
              />
              {fieldErrors.adults && <div className="error-indicator" />}
            </div>
            <div className="ticket-item">
              <TicketNumber
                title="兒童票"
                iconSrc="/icons/children.png"
                min={0}
                max={10}
                value={formData.childs}
                onChange={(value) => handleFieldChange("childs", value)}
              />
              {fieldErrors.childs && <div className="error-indicator" />}
            </div>
            <div className="ticket-item">
              <TicketNumber
                title="敬老票"
                iconSrc="/icons/elderly.png"
                min={0}
                max={10}
                value={formData.elders}
                onChange={(value) => handleFieldChange("elders", value)}
              />
              {fieldErrors.elders && <div className="error-indicator" />}
            </div>
            <div className="ticket-item">
              <TicketNumber
                title="愛心票"
                iconSrc="/icons/disabled.png"
                min={0}
                max={10}
                value={formData.disables}
                onChange={(value) => handleFieldChange("disables", value)}
              />
              {fieldErrors.disables && <div className="error-indicator" />}
            </div>
            <div className="ticket-item">
              <TicketNumber
                title="學生票"
                iconSrc="/icons/students.png"
                min={0}
                max={10}
                value={formData.students}
                onChange={(value) => handleFieldChange("students", value)}
              />
              {fieldErrors.students && <div className="error-indicator" />}
            </div>
          </div>
        </div>

        {shouldShowEarlyBirdIds() && (
          <div className="early-bird-section">
            <h3>購買早鳥票</h3>
            <div className="early-bird-grid">
              {Array.from({ length: getEarlyBirdCount() }).map((_, index) => (
                <div key={`early_id_${index}`} className="early-bird-item">
                  <IDNumberInput
                    title={`早鳥${index + 1}`}
                    value={formData.early_ids[index] || ""}
                    onChange={(value) => handleEarlyIdChange(index, value)}
                  />
                  {fieldErrors[`early_id_${index}`] && (
                    <div className="error-indicator" />
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="button-section">
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
            icon="/icons/booking.png"
            buttonColor="#a7fdb9"
            selectedColor="#59fa59"
            buttonSize="medium"
            onClick={handleBooking}
          />
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
