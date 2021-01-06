# from fastapi import APIRouter

# from ..routers.external.giphy import get_meme
# from ..routers.external.google_scraper import scraper
# from ..schemas.find_rank_schema import FindRankRequestSchema
# from ..services import domain_service, keyword_service

# rank_router = APIRouter()


# @rank_router.post("/find_rank")
# def root(payload: FindRankRequestSchema):

#     out_scraper = scraper(payload.terms, payload.url_to_find, payload.is_city)
#     if not out_scraper['contains']:
#         tag = "cry"
#     elif out_scraper['rank'] > 10:
#         tag = "smile"
#     else:
#         tag = "success"

#     domain_service.create_by_owner
#     # Inserir na tabela
#     # Esperar

#     return {**out_scraper, "meme": get_meme(tag)}
