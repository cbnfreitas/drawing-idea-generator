from fastapi import APIRouter

from .auth_router import auth_router
from .dummies_router import dummies_router
from .features_router import features_router
from .users_me_router import router as users_me_router
from .users_router import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["Auth"])
api_router.include_router(users_me_router, tags=["Users/Me"])
api_router.include_router(users_router, tags=["Users"])
api_router.include_router(features_router, tags=["Features"])

api_router.include_router(dummies_router, tags=["Dummies"])
