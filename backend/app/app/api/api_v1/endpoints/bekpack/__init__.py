from fastapi.routing import APIRouter
from .bekpackuser import router as bekpackuser
from .bekpacktrip import router as bekpacktrip

router = APIRouter()
router.include_router(bekpackuser, prefix="/bekpackusers", tags=["bekpackusers"])
router.include_router(bekpacktrip, prefix="/bekpacktrips", tags=["bekpacktrips"])
