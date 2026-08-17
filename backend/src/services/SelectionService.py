from typing import Any, Dict, List


class SelectionService:
    """選單載入服務"""

    def __init__(self, selection_repository=None):
        self.selection_repository = selection_repository

    def get_selection_options(self, parm_category: str) -> List[Dict[str, Any]]:
        """依類別取得選單內容"""
        if not parm_category or not parm_category.strip():
            raise ValueError("parm_category is required")

        if self.selection_repository is None:
            return []

        data = self.selection_repository.get_by_category(parm_category.strip())
        return [
            {
                "id": item.parm_id,
                "parm_name": item.parm_name,
                "parm_value": item.parm_value,
            }
            for item in data
        ]
