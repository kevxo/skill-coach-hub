from fastapi import APIRouter, Depends
from app.models.user import User, UserRole
from app.core.dependencies import require_role

router = APIRouter(
    prefix="/coach",
    tags=["coach"],
)

@router.get("/dashboard")
def coach_dashboard(coach: User = Depends(require_role(UserRole.coach))):
    return {
        "message": f"Welcome Coach {coach.first_name}",
        "role": coach.role
    }