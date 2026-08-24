FROM python:3.14-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 複製requirements.txt並安裝Python依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製爬蟲程式碼
COPY . .

# 設置環境變數
ENV PYTHONUNBUFFERED=1

# 運行爬蟲
CMD ["python", "main.py"]
