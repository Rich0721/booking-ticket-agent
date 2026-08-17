from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.config.database import get_db_session
from src.repositories.SelectionRepository import SelectionRepository
from src.services.SelectionService import SelectionService

router = APIRouter()


def get_selection_repository(db_session: Session = Depends(get_db_session)) -> SelectionRepository:
    """建立 SelectionRepository 依賴"""
    return SelectionRepository(db_session)


@router.get("/loading-selected")
async def loading_selected(
    parm_category: str = Query(..., description="選單類別"),
    repository: SelectionRepository = Depends(get_selection_repository),
):
    """依 parm_category 讀取 TB_SYS_PARM 中的選單資料"""
    try:
        service = SelectionService(repository)
        menu = service.get_selection_options(parm_category)
        return {"info": {"menu": menu}}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - unexpected runtime safeguard
        raise HTTPException(status_code=500, detail=str(exc)) from exc
