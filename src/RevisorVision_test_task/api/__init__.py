from fastapi import APIRouter
from .plate_operations import router as plate_router
from .auth import router as auth_router


router = APIRouter()
router.include_router(plate_router)
router.include_router(auth_router)
