# from datetime import datetime
# from typing import Any, Dict

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from ..core.base_router import build_crud_by_owner
# from ..core.depends import get_db, get_user_from_access_token
# from ..routers.external.google_scraper import scraper
# from ..schemas.keyword_schema import (KeywordRequestSchema,
#                                       KeywordResponseSchema)
# from ..schemas.rank_schema import RankRequestSchema
# from ..services import domain_service, rank_service
# from ..services.keyword_service import keyword_service

# keyword_router = APIRouter()

# build_crud_by_owner(keyword_router,  "keyword", "keywords", keyword_service,
#                     KeywordRequestSchema, KeywordResponseSchema,
#                     options={'update': False, 'create': False})


# @keyword_router.post("/keywords",
#                      summary=f"Create a new keyword",
#                      response_model=KeywordResponseSchema
#                      )
# async def create(
#         db: Session = Depends(get_db),
#         user_token_data: Dict[str, Any] = Depends(
#             get_user_from_access_token),
#         *,
#         obj_in: KeywordRequestSchema
# ) -> Any:
#     """
#     Create an entity.
#     """
#     entity = keyword_service.create_by_owner(
#         db, obj_in=obj_in, owner_id=user_token_data["user_id"])

#     domain = domain_service.read_by_owner(
#         db, id=obj_in.domain_id, owner_id=user_token_data["user_id"])

#     return entity


# def update_keyword_rank_async(db, user_id, keyword_id, keyword, domain_url):
#     out_scraper = scraper(keyword, domain_url, True)
#     obj_in = {'keyword_id': keyword_id,
#               'rank': out_scraper['rank']}
#     rank_service.create(db, obj_in=RankRequestSchema(**obj_in))

#     obj_in = {'last_rank': out_scraper['rank'],
#               'last_rank_date': datetime.now()}
#     keyword_service.update_by_owner(
#         db, id=keyword_id,  owner_id=user_id, obj_in=obj_in)
