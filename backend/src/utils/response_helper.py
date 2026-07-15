"""Response相關工具函式"""
from typing import Any, Dict, Optional

def create_response(headers: Optional[Dict[str, Any]] = None, info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    建立標準API Response格式
    
    Args:
        headers: 標頭訊息字典
        info: 資訊字典
        
    Returns:
        dict: 標準格式的Response
    """
    response = {}
    
    if headers is not None:
        response['headers'] = headers
    else:
        response['headers'] = {}
    
    if info is not None:
        response['info'] = info
    
    return response


def create_error_response(message: str) -> Dict[str, Any]:
    """
    建立錯誤Response
    
    Args:
        message: 錯誤訊息
        
    Returns:
        dict: 錯誤Response
    """
    return create_response(
        headers={'message': message}
    )


def create_success_response(message: str = '', info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    建立成功Response
    
    Args:
        message: 成功訊息
        info: 資訊字典
        
    Returns:
        dict: 成功Response
    """
    return create_response(
        headers={'message': message},
        info=info
    )
