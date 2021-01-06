from fastapi import APIRouter

from .auth_router import router as auth_router
from .rank_router import rank_router
# from .domain_router import domain_router
# from .keyword_router import keyword_router
# from .rank_router import rank_router
from .users_me_router import router as users_me_router
from .users_router import router as user_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["Auth"])
api_router.include_router(users_me_router, tags=["Users/Me"])
api_router.include_router(user_router, tags=["Users"])

# api_router.include_router(domain_router, tags=["Domains & Keywords"])
# api_router.include_router(keyword_router, tags=["Domains & Keywords"])
api_router.include_router(rank_router, tags=["Ranks - only for testing!"])

# api_router.include_router(rank_router, tags=["Rank"])
