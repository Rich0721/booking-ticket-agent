# 資料庫架構設計文檔

## 概述

本項目採用**可擴展的資料庫架構設計**，支持多種資料庫，當前以 **PostgreSQL** 為主。透過抽象層和工廠模式，未來無需修改應用代碼就能切換到其他資料庫。

---

## 架構設計

### 核心組件

```
┌─────────────────────────────────────────────┐
│         FastAPI應用層                        │
│  (BookingTicketController等)                │
└──────────────────┬──────────────────────────┘
                   │ 依賴注入
                   ▼
┌─────────────────────────────────────────────┐
│      get_db_session() 便利函數               │
│  (保持FastAPI Depends()兼容)                 │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│         DatabaseProvider 抽象基類            │
│  定義統一的資料庫操作接口                    │
└──────────────────┬──────────────────────────┘
         ┌─────────┴─────────┐
         ▼                   ▼
    ┌──────────┐      ┌──────────┐
    │PostgreSQL│      │  MySQL   │
    │Provider  │      │Provider  │
    └──────────┘      └──────────┘
         │                   │
         ▼                   ▼
    PostgreSQL           MySQL
    (主要)              (備用)
```

### 類層次結構

#### 1. `DatabaseConfig` - 配置類

```python
# 自動從環境變數讀取
config = DatabaseConfig()
# config.host, config.port, config.user, config.password, config.database, config.db_type
```

**環境變數**：

- `DB_TYPE`：資料庫類型（postgresql, mysql）
- `DB_HOST`：資料庫主機
- `DB_PORT`：資料庫埠
- `DB_USER`：用戶名
- `DB_PASSWORD`：密碼
- `DB_NAME`：資料庫名稱
- `DEBUG`：調試模式（True/False）

#### 2. `DatabaseProvider` - 抽象基類

定義所有資料庫提供者必須實現的接口：

```python
class DatabaseProvider(ABC):
    @abstractmethod
    def get_connection_string(self) -> str:
        """取得資料庫連接字符串"""
        pass

    @abstractmethod
    def get_engine(self) -> Engine:
        """取得SQLAlchemy Engine"""
        pass

    @abstractmethod
    def get_session_factory(self) -> sessionmaker:
        """取得Session工廠"""
        pass

    def get_db_session(self) -> Session:
        """取得資料庫Session"""
        # 通用實現

    def init_db(self):
        """初始化資料庫"""
        # 通用實現
```

#### 3. `PostgreSQLProvider` - PostgreSQL實現

```python
class PostgreSQLProvider(DatabaseProvider):
    def get_connection_string(self) -> str:
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    def get_engine(self) -> Engine:
        return create_engine(
            url,
            echo=debug,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
```

#### 4. `MySQLProvider` - MySQL實現

```python
class MySQLProvider(DatabaseProvider):
    def get_connection_string(self) -> str:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    def get_engine(self) -> Engine:
        return create_engine(
            url,
            echo=debug,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
```

#### 5. `DatabaseFactory` - 工廠模式

```python
class DatabaseFactory:
    @classmethod
    def create_provider(config: DatabaseConfig) -> DatabaseProvider:
        """根據DB_TYPE動態創建對應的Provider"""
        # 自動選擇PostgreSQLProvider或MySQLProvider

    @classmethod
    def register_provider(db_type: str, provider_class: type):
        """註冊新的資料庫提供者（支持擴展）"""
```

---

## 使用指南

### 1. 基本使用 - FastAPI依賴注入

```python
from fastapi import Depends
from src.config.database import get_db_session
from sqlalchemy.orm import Session

@router.post("/booking-ticket")
async def booking_ticket(
    request: BookingTicketRequest,
    db_session: Session = Depends(get_db_session)
):
    # 自動注入資料庫Session
    # 無需修改代碼，根據環境變數自動切換資料庫
    repository = BookingTicketRepository(db_session)
    return repository.create_booking(...)
```

### 2. 環境配置示例

#### 開發環境 (`.env.dev`)

```
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=booking_ticket
DEBUG=True
```

#### 生產環境 (`.env.prod`)

```
DB_TYPE=postgresql
DB_HOST=db
DB_PORT=5432
DB_USER=booking_user
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=booking_ticket
DEBUG=False
```

### 3. 切換資料庫（開發/測試）

直接修改環境變數 `DB_TYPE`，**無需修改任何應用代碼**：

```bash
# 使用PostgreSQL
export DB_TYPE=postgresql

# 使用MySQL
export DB_TYPE=mysql

# Python中
os.environ["DB_TYPE"] = "mysql"
```

---

## 擴展新的資料庫

### 步驟 1：創建新Provider類

```python
# backend/src/config/database.py

class OracleProvider(DatabaseProvider):
    """Oracle資料庫提供者"""

    def get_connection_string(self) -> str:
        return f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{database}"

    def get_engine(self) -> Engine:
        return create_engine(
            self.get_connection_string(),
            echo=self.config.debug,
            pool_pre_ping=True
        )

    def get_session_factory(self) -> sessionmaker:
        engine = self.get_engine_instance()
        return sessionmaker(bind=engine, expire_on_commit=False)
```

### 步驟 2：註冊Provider

```python
# backend/src/config/database.py 或其他初始化位置

from src.config.database import DatabaseFactory, OracleProvider

# 註冊新的資料庫提供者
DatabaseFactory.register_provider("oracle", OracleProvider)
```

### 步驟 3：配置環境變數

```
DB_TYPE=oracle
DB_HOST=oracle-server
DB_PORT=1521
DB_USER=oracle_user
DB_PASSWORD=password
DB_NAME=BOOKING_TICKET
```

**完成！無需修改任何應用代碼。**

---

## 架構優勢

### 1. **高度可擴展**

- 新增資料庫只需創建新的Provider類
- 使用工廠模式自動選擇正確的實現
- 支持 `register_provider()` 動態註冊

### 2. **零代碼修改**

- 應用代碼只依賴 `get_db_session()` 便利函數
- 切換資料庫只需修改環境變數
- 完全後向兼容

### 3. **規範化設計**

- 抽象基類定義清晰的接口契約
- 所有實現必須遵循同一模式
- 易於測試和維護

### 4. **生產就緒**

- 連接池管理（pool_size, max_overflow）
- 連接健康檢查（pool_pre_ping）
- SQL調試模式支持

---

## 測試支持

### Mock資料庫測試

```python
# backend/tests/conftest.py

@pytest.fixture
def mock_db_session():
    """Mock資料庫Session用於單元測試"""
    session = MagicMock(spec=Session)
    # 配置mock行為
    return session

# 測試代碼
def test_create_booking(mock_db_session):
    repository = BookingTicketRepository(mock_db_session)
    result = repository.create_booking(...)
    mock_db_session.add.assert_called()
    mock_db_session.flush.assert_called()
```

### 測試驗證

所有47個單元測試通過，驗證：

- ✅ 依賴注入正常工作
- ✅ Mock資料庫層正常運作
- ✅ 無功能破壞

---

## 注意事項

1. **連接字符串格式**
   - PostgreSQL: `postgresql+psycopg2://`
   - MySQL: `mysql+pymysql://`
   - 確保使用正確的驅動

2. **環境變數優先級**
   - 直接設置的環境變數 > .env文件
   - 開發時使用 `.env.dev`，生產使用 `.env.prod`

3. **連接池配置**
   - `pool_size=10`: 持久連接數
   - `max_overflow=20`: 最大突發連接數
   - 可根據負載調整

4. **調試模式**
   - `DEBUG=True` 時顯示所有SQL語句
   - 生產環境應設置為 `False`

---

## 支持的資料庫類型

| 資料庫     | DB_TYPE                   | 驅動      | 狀態      |
| ---------- | ------------------------- | --------- | --------- |
| PostgreSQL | `postgresql` / `postgres` | psycopg2  | ✅ 主要   |
| MySQL      | `mysql`                   | pymysql   | ✅ 備用   |
| Oracle     | `oracle`                  | cx_oracle | 📝 可擴展 |
| SQLite     | `sqlite`                  | sqlite3   | 📝 可擴展 |

---

## 常見問題

**Q: 如何在開發中使用PostgreSQL，生產中使用MySQL？**

A: 分別配置 `.env.dev` 和 `.env.prod`：

```bash
# .env.dev
DB_TYPE=postgresql

# .env.prod
DB_TYPE=mysql
```

**Q: 是否可以同時使用多個資料庫？**

A: 可以創建多個provider實例並管理它們，但當前 `get_db_session()` 只返回一個主資料庫連接。

**Q: 性能如何？**

A: 透過連接池和預ping機制確保最優性能，無額外開銷。

---

## 版本歷史

- **v1.0** (2026-07-16): 初始設計
  - 支持PostgreSQL和MySQL
  - 工廠模式和抽象層
  - 所有47個測試通過
