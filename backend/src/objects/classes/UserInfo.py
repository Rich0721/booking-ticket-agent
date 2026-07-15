class UserInfo:
    """使用者資訊類別"""
    
    def __init__(self, user_id: str, ticket_type: str = None, is_member: bool = False):
        """
        初始化使用者資訊
        
        Args:
            user_id: 使用者ID（身份證字號）
            ticket_type: 票券類型 (THSR, TRA等)
            is_member: 是否為會員
        """
        self.user_id = user_id
        self.ticket_type = ticket_type
        self.is_member = is_member
    
    def __repr__(self):
        return f"UserInfo(user_id={self.user_id}, ticket_type={self.ticket_type}, is_member={self.is_member})"
