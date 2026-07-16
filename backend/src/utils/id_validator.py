def validate_taiwan_id(id_string: str) -> bool:
    """
    驗證台灣身份證編號是否符合編碼方式
    
    Args:
        id_string: 台灣身份證編號
        
    Returns:
        True if valid, False otherwise
    """
    if not id_string or len(id_string) != 10:
        return False
    
    if not (id_string[0].isalpha() and id_string[1:].isdigit()):
        return False
    
    # 首字母對應的數字
    id_letter_dict = {
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16,
        'H': 17, 'I': 34, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22,
        'O': 35, 'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28,
        'V': 29, 'W': 32, 'X': 30, 'Y': 31, 'Z': 33
    }
    
    if id_string[0] not in id_letter_dict:
        return False
    
    # 驗證性別碼（第二位應該是1或2）
    if id_string[1] not in ['1', '2']:
        return False
    
    # 計算檢查碼
    total = id_letter_dict[id_string[0]] // 10 + (id_letter_dict[id_string[0]] % 10) * 9
    
    for i in range(1, 10):
        total += int(id_string[i]) * (10 - i)
    
    check_digit = (10 - (total % 10)) % 10
    
    return check_digit == int(id_string[9])


# 生成有效的測試身份證號
def generate_valid_test_id(letter: str, sex_and_numbers: str) -> str:
    """
    為測試生成有效的台灣身份證號
    
    Args:
        letter: 首字母 (A-Z)
        sex_and_numbers: 8位數字 (第一位為性別碼1=男/2=女，後7位為編號)
        
    Returns:
        10位有效身份證號
    """
    if len(sex_and_numbers) != 8:
        raise ValueError("sex_and_numbers must be 8 digits")
    
    id_letter_dict = {
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16,
        'H': 17, 'I': 34, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22,
        'O': 35, 'P': 23, 'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28,
        'V': 29, 'W': 32, 'X': 30, 'Y': 31, 'Z': 33
    }
    
    total = id_letter_dict[letter] // 10 + (id_letter_dict[letter] % 10) * 9
    
    for i in range(8):
        total += int(sex_and_numbers[i]) * (8 - i)
    
    check_digit = (10 - (total % 10)) % 10
    
    return letter + sex_and_numbers + str(check_digit)
