import sys
sys.path.insert(0, '.')
from src.utils.id_validator import validate_taiwan_id, generate_valid_test_id

# 測試一些ID
print("Testing ID validation:")
print(f"A123456785: {validate_taiwan_id('A123456785')}")
print(f"B987654325: {validate_taiwan_id('B987654325')}")
print(f"INVALID123: {validate_taiwan_id('INVALID123')}")

# 生成有效的ID (8位數字，第一位是性別碼)
print("\nGenerating valid IDs:")
id1 = generate_valid_test_id('A', '12345678')  # 8位
id2 = generate_valid_test_id('B', '98765432')  # 8位
print(f"Generated ID 1: {id1} (len={len(id1)}) (valid: {validate_taiwan_id(id1)})")
print(f"Generated ID 2: {id2} (len={len(id2)}) (valid: {validate_taiwan_id(id2)})")

