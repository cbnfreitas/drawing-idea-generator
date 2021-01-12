from fastapi import APIRouter

from .auth_route import auth_route
from .dummy_route import dummy_route
from .feature_route import feature_route
from .idea_route import idea_route
from .user_me_route import user_me_route
from .user_route import user_route
from .value_route import value_route

api_router = APIRouter()

api_router.include_router(idea_route, tags=["Ideas!"])

api_router.include_router(auth_route, tags=["Auth"])
api_router.include_router(user_me_route, tags=["Users/Me"])
api_router.include_router(user_route, tags=["Users"])

api_router.include_router(dummy_route, tags=["Dummies"])

api_router.include_router(feature_route, tags=["Features & Values"])
api_router.include_router(value_route, tags=["Features & Values"])
