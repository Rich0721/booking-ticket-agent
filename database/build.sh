#!/bin/bash
set -e # 若其中有任何一個 SQL 執行失敗，整個腳本會立即終止並報錯

echo "=========================================="
echo "開始執行資料庫初始化腳本..."
echo "=========================================="

# 1. 批次執行 tables 資料夾下的所有 .sql 檔案
if [ -d "/docker-entrypoint-initdb.d/tables" ]; then
    echo "--- 正在建立資料表 (Tables) ---"
    for sql_file in /docker-entrypoint-initdb.d/tables/*.sql; do
        if [ -f "$sql_file" ]; then
            echo "執行中: $(basename "$sql_file")"
            psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$sql_file"
        fi
    done
fi

# 2. 批次執行 dml 資料夾下的所有 .sql 檔案
if [ -d "/docker-entrypoint-initdb.d/dml" ]; then
    echo "--- 正在載入初始資料 (DML) ---"
    for sql_file in /docker-entrypoint-initdb.d/dml/*.sql; do
        if [ -f "$sql_file" ]; then
            echo "執行中: $(basename "$sql_file")"
            psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$sql_file"
        fi
    done
fi

echo "=========================================="
echo "資料庫建置與初始化全部完成！"
echo "=========================================="