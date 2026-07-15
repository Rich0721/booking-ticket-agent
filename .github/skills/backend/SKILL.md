# Backend Skills

---

name: Backend Skills
description: 模擬後端工程師根據需求檔案進行對應的功能開發，並完成對應的Unit Test，最後將程式碼提交至GitHub。

---

## Backend Skills

- 需求來源: [Backend Skills](../../Features/backend/requirements/)

### Step 1: 需求分析

閱讀需求分析文件的「需求簡介」與「需求說明」部分，了解需求的功能與限制。

#### 細項說明

- 請勿自行腦補需求，若有不清楚的地方請根據**需求模糊**格式進行回覆，等待PM完成回覆再進行會影響的開發。
- PM尚未回覆前，若不影響其他需求的開發，請先進行其他需求的開發。

### Step 2: Create Git Branch

1. Pull main分支最新版本，並建立對應的需求分支或Bug修復分支

### Step 3: 撰寫Unit Test

根據需求文件先行撰寫對應的Unit Test，確保程式碼符合需求。

#### 細項說明

- 撰寫Unit Test時，根據需求文件對應的[情境文件](../../Features//backend/scenarios/)撰寫Unit Test，確保程式碼符合需求。
- 若情境文件透過Scenario Outline撰寫時，僅能撰寫單一的測試程式碼通過所有的情境，減少重複撰寫測試程式碼，範例說明如下:
  - TextFormatScenario和text_format_scenarios會放在backend/tests/scenarios/test_get_text_format.py中，並且透過pytest.mark.parametrize進行多個情境的測試，範例如下:

```python
@dataclass
class TextFormatScenario:
    """Test scenario for get_text_format function"""
    name: str
    data: List[list]
    header: List[str]
    should_contain: List[str]

# Define multiple test scenarios
text_format_scenarios = [
    TextFormatScenario(
        name="Basic text format",
        data=[['Alice', '100', 'Pass'], ['Bob', '85', 'Fail']],
        header=['Name', 'Score', 'Status'],
        should_contain=[
            '| Name | Score | Status |',
            '| :---: | :---: | :---: |',
            '| Alice | 100 | Pass |',
            '| Bob | 85 | Fail |'
        ]
    ),
    TextFormatScenario(
        name="Single row data",
        data=[['John', '95', 'Pass']],
        header=['Name', 'Score', 'Status'],
        should_contain=[
            '| Name | Score | Status |',
            '| :---: | :---: | :---: |',
            '| John | 95 | Pass |'
        ]
    ),
    TextFormatScenario(
        name="Numeric data",
        data=[[1, 2, 3], [4, 5, 6]],
        header=['A', 'B', 'C'],
        should_contain=[
            '| A | B | C |',
            '| :---: | :---: | :---: |',
            '| 1 | 2 | 3 |',
            '| 4 | 5 | 6 |'
        ]
    ),
]
@pytest.mark.parametrize("scenario", text_format_scenarios)
@patch('src.utils.write_log_file')
def test_get_text_format(mock_write_log, scenario):
   """Test get_text_format with multiple scenarios"""
   result = get_text_format(scenario.data, scenario.header)

   # Check all required content is present
   for expected_text in scenario.should_contain:
      assert expected_text in result, f"Scenario '{scenario.name}': Expected '{expected_text}' not found in result"

   # Check unwanted content is not present
   if scenario.should_not_contain:
      for unwanted_text in scenario.should_not_contain:
         assert unwanted_text not in result, f"Scenario '{scenario.name}': Unwanted '{unwanted_text}' found in result"
```

- 若情境文件透過Scenario或Example撰寫時，則以每個情境撰寫對應的測試程式碼

```python
def test_email_info_with_custom_body_html(self):
   """Test creating email with custom HTML body"""
   sender = "sender@example.com"
   to = "recipient@example.com"
   custom_html = "<html><body>Custom HTML</body></html>"

   msg = email_info(sender, to, body_html=custom_html)

   payloads = msg.get_payload()
   assert any(
      custom_html in (payload.decode('utf-8') if isinstance(payload := p.get_payload(decode=True), bytes) else payload)
      for p in payloads
   )

```

### Step 4: 撰寫程式碼

根據需求文件與Unit Test撰寫對應的程式碼，確保程式碼符合需求並通過Unit Test，不可透過Unit Test作弊

#### 細項說明

- 撰寫程式碼時，需確保程式碼符合需求文件的規範，並且能夠通過所有的Unit Test。
- 完成後，不調整程式碼，除非需求文件有更新或發現程式碼本身有錯誤。
-

### Step 5: 確認所有需求都有通過Unit Test

每次撰寫完對應需求後，確認所有需求都有通過Unit Test，確保程式碼符合需求

#### 細項說明

- 若有需求未通過Unit Test，請先檢查程式碼是否符合需求，若不符合需求請先修正程式碼，並重新執行Unit Test，直到所有需求都通過Unit Test。
- 若調整三次程式碼仍無法通過Unit Test，請根據**需求模糊**格式進行回覆，等待PM回覆。

### Step 6: 提交程式碼

1. 將程式碼提交至GitHub。
2. 提出MR分支回到main分支。
