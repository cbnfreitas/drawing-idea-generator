from fastapi import APIRouter

from .auth_route import auth_route
from .dummies_route import dummies_route
from .features_router import features_router
from .users_me_route import router as users_me_route
from .users_route import router as users_route
from .values_route import values_route

api_router = APIRouter()

api_router.include_router(auth_route, tags=["Auth"])
api_router.include_router(users_me_route, tags=["Users/Me"])
api_router.include_router(users_route, tags=["Users"])

api_router.include_router(dummies_route, tags=["Dummies"])


api_router.include_router(features_router, tags=["Features & Values"])
api_router.include_router(values_route, tags=["Features & Values"])
