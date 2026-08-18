const fs = require("fs");
const path = require("path");

// 判斷環境
const nodeEnv = process.env.NODE_ENV || "development";
const envFileName = nodeEnv === "production" ? ".env.prod" : ".env.dev";
const srcPath = path.join(__dirname, "..", "env", envFileName);
const destPath = path.join(__dirname, ".env");

try {
  // 檢查源檔案是否存在
  if (!fs.existsSync(srcPath)) {
    console.error(`❌ Environment file not found: ${srcPath}`);
    process.exit(1);
  }

  // 複製環境檔案
  fs.copyFileSync(srcPath, destPath);
  console.log(`✅ Environment file copied: ${envFileName} -> .env`);
} catch (error) {
  console.error("❌ Error setting up environment:", error.message);
  process.exit(1);
}
