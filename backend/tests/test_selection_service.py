"""
選單載入服務單元測試

來源: .github/Features/backend/requirements/Loading_Selected.md
"""

from types import SimpleNamespace

import pytest

from src.services.SelectionService import SelectionService


class TestSelectionService:
    """選單載入服務測試"""

    @pytest.fixture
    def service(self):
        """建立服務實例"""
        return SelectionService()

    @pytest.mark.parametrize(
        "parm_category,expected",
        [
            (
                "THSR_TIME",
                [
                    {"id": 1, "parm_name": "00:00", "parm_value": "1201A"},
                    {"id": 2, "parm_name": "00:30", "parm_value": "1230A"},
                ],
            ),
            (
                "THSR_STATION",
                [
                    {"id": 3, "parm_name": "台北", "parm_value": "TPE"},
                    {"id": 4, "parm_name": "台中", "parm_value": "TXG"},
                ],
            ),
        ],
    )
    def test_get_selection_options_success(self, service, parm_category, expected, monkeypatch):
        """測試依 parm_category 取得對應選項 - Scenario: 載入選單資料成功"""
        repo = SimpleNamespace(
            get_by_category=lambda category: [
                SimpleNamespace(parm_id=1, parm_name="00:00", parm_value="1201A"),
                SimpleNamespace(parm_id=2, parm_name="00:30", parm_value="1230A"),
            ]
            if category == "THSR_TIME"
            else [
                SimpleNamespace(parm_id=3, parm_name="台北", parm_value="TPE"),
                SimpleNamespace(parm_id=4, parm_name="台中", parm_value="TXG"),
            ]
        )

        monkeypatch.setattr(service, "selection_repository", repo)

        result = service.get_selection_options(parm_category)

        assert result == expected

    @pytest.mark.parametrize("parm_category", ["", "   "])
    def test_get_selection_options_empty_category_rejected(self, service, parm_category):
        """測試空白 parm_category 不接受 - Scenario: 參數缺失或空值"""
        with pytest.raises(ValueError, match="parm_category"):
            service.get_selection_options(parm_category)

    def test_get_selection_options_returns_empty_list_when_not_found(self, service, monkeypatch):
        """測試查無資料時回傳空選單 - Scenario: 無符合類別的選項"""
        repo = SimpleNamespace(get_by_category=lambda category: [])
        monkeypatch.setattr(service, "selection_repository", repo)

        result = service.get_selection_options("UNKNOWN_CATEGORY")

        assert result == []
