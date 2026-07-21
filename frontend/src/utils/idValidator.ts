/**
 * 驗證台灣身份證字號格式
 * 台灣身份證編碼方式：
 * - 第1碼：英文字母（代表出生地）
 * - 第2碼：數字（1代表男性，2代表女性）
 * - 第3-10碼：共8位數字
 *
 * @param idNumber - 身份證字號
 * @returns 是否符合台灣身份證格式
 */
export const isValidTaiwanID = (idNumber: string): boolean => {
  if (!idNumber) {
    return false;
  }

  // 移除空白
  const cleanedID = idNumber.trim().toUpperCase();

  // 檢查長度
  if (cleanedID.length !== 10) {
    return false;
  }

  // 檢查格式：第一個字是英文，第二個字是1或2，其餘8位是數字
  const taiwanIDPattern = /^[A-Z][1-2][0-9]{8}$/;
  if (!taiwanIDPattern.test(cleanedID)) {
    return false;
  }

  // 驗證檢驗碼（基於台灣身份證號碼檢驗演算法）
  const idLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const firstCharValue = idLetters.indexOf(cleanedID[0]) + 10;

  let sum = Math.floor(firstCharValue / 10) + (firstCharValue % 10) * 9;

  for (let i = 1; i < 9; i++) {
    sum += parseInt(cleanedID[i]) * (9 - i);
  }

  sum += parseInt(cleanedID[9]);

  return sum % 10 === 0;
};
