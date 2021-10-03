from fastapi.routing import APIRouter
from .bekpackuser import router as bekpackuser
from .bekpacktrip import router as bekpacktrip
from .bekpacktripitemlist import router as bekpackitemlist
from .bekpackitemlistitem import router as bekpackitemlistitem

router = APIRouter()
router.include_router(bekpackuser, prefix="/bekpackusers", tags=["bekpackusers"])
router.include_router(bekpacktrip, prefix="/bekpacktrips", tags=["bekpacktrips"])
router.include_router(
    bekpackitemlist, prefix="/bekpackitemlists", tags=["bekpackitemlists"]
)
router.include_router(
    bekpackitemlistitem, prefix="/bekpackitemlistitems", tags=["bekpackitemlistitems"]
)
