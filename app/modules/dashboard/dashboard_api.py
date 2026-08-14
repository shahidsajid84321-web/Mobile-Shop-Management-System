from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.constants.permissions import PermissionCode
from app.dependencies.db import get_db
from app.modules.dashboard.dashboard_schema import DashboardResponse
from app.modules.dashboard.dashboard_service import DashboardService
from app.modules.permissions.permission_dependencies import require_permission
from app.shared.common_schema import ApiResponse
from app.shared.responses import success_response

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=ApiResponse[DashboardResponse])
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_permission(PermissionCode.DASHBOARD_VIEW)),
):
    return success_response("Dashboard retrieved successfully.", DashboardService.get_dashboard(db))
