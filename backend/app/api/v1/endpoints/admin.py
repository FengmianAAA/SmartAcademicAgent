from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user, get_db
from app.models.user import User
from app.schemas.admin import (
    AdminOverviewResponse,
    WarningRecordResponse,
    WarningRecordUpdate,
    WarningRuleCreate,
    WarningRuleResponse,
    WarningRuleUpdate,
)
from app.services.admin_service import (
    create_warning_rule,
    delete_warning_rule,
    get_admin_overview,
    list_warning_records,
    list_warning_rules,
    update_warning_record,
    update_warning_rule,
)

router = APIRouter()


@router.get("/overview", response_model=AdminOverviewResponse)
def overview(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> AdminOverviewResponse:
    return get_admin_overview(db)


@router.get("/warning-rules", response_model=list[WarningRuleResponse])
def warning_rules(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> list[WarningRuleResponse]:
    return list_warning_rules(db)


@router.post("/warning-rules", response_model=WarningRuleResponse, status_code=status.HTTP_201_CREATED)
def create_rule(payload: WarningRuleCreate, current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> WarningRuleResponse:
    return create_warning_rule(db, payload)


@router.put("/warning-rules/{rule_id}", response_model=WarningRuleResponse)
def update_rule(rule_id: int, payload: WarningRuleUpdate, current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> WarningRuleResponse:
    result = update_warning_rule(db, rule_id, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Warning rule not found")
    return result


@router.delete("/warning-rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_rule(rule_id: int, current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> None:
    ok = delete_warning_rule(db, rule_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Warning rule not found")


@router.get("/warning-records", response_model=list[WarningRecordResponse])
def warning_records(current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> list[WarningRecordResponse]:
    return list_warning_records(db)


@router.put("/warning-records/{record_id}", response_model=WarningRecordResponse)
def update_record(record_id: int, payload: WarningRecordUpdate, current_user: User = Depends(get_admin_user), db: Session = Depends(get_db)) -> WarningRecordResponse:
    result = update_warning_record(db, record_id, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="Warning record not found")
    return result
