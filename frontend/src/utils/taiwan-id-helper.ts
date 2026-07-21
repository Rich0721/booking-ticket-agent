/**
 * 生成和驗證台灣身份證號碼的工具
 */

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

  // 檢查驗證碼（基於台灣身份證號碼檢驗算法）
  // 將字母轉換為數字（A=10, B=11, ..., Z=35）
  const idLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const firstCharValue = idLetters.indexOf(cleanedID[0]) + 10;

  // 計算第一碼的權重
  let sum = Math.floor(firstCharValue / 10) + (firstCharValue % 10) * 9;

  // 計算第2-9碼的權重
  for (let i = 1; i < 9; i++) {
    sum += parseInt(cleanedID[i]) * (9 - i);
  }

  // 加上檢驗碼
  sum += parseInt(cleanedID[9]);

  // 驗證和模10是否為0
  return sum % 10 === 0;
};

/**
 * 根據開頭和性別生成有效的台灣身份證號碼
 * 用於測試用途
 *
 * @param prefix - 身份證開頭字母（如 'A', 'B'等）
 * @param gender - 性別（1為男性，2為女性）
 * @returns 生成的有效身份證號碼
 */
export const generateValidTaiwanID = (
  prefix: string = "A",
  gender: number = 1,
): string => {
  // 基礎序號
  let idNumber = prefix + gender + "12345678";

  // 計算檢驗碼
  const idLetters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const firstCharValue = idLetters.indexOf(idNumber[0]) + 10;

  let sum = Math.floor(firstCharValue / 10) + (firstCharValue % 10) * 9;

  for (let i = 1; i < 9; i++) {
    sum += parseInt(idNumber[i]) * (9 - i);
  }

  // 計算檢驗碼（使得 (sum + checksum) % 10 === 0）
  const checksum = (10 - (sum % 10)) % 10;

  return idNumber + checksum;
};
