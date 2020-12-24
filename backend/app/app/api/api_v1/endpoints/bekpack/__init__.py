from fastapi.routing import APIRouter
from .bekpackuser import router as bekpackuser

router = APIRouter()
router.include_router(bekpackuser, prefix="/bekpackusers", tags=["bekpackusers"])
