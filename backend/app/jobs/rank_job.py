# from datetime import datetime

# from fastapi import Depends
# from sqlalchemy.orm import Session

# from ..core import s
# from ..core.db.base import Base
# from ..core.db.session import engine
# from ..core.depends import get_db
# from ..routers.external.google_scraper import scraper
# from ..schemas.rank_schema import RankRequestSchema
# from ..services import (domain_service, keyword_service, rank_service,
#                         user_service)


# def rank_job(db: Session = Depends(get_db)) -> None:

#     print('Running Rank Job!!!')

#     dt = datetime.now()
#     today_zero_hour = dt.replace(hour=0, minute=0, second=0, microsecond=0)

#     users = user_service.read_many(db)
#     for user in users:
#         domains = domain_service.read_many_by_owner(db, owner_id=user.id)
#         for domain in domains:
#             keywords = domain.keywords
#             for keyword in keywords:
#                 if not keyword.last_rank_date or \
#                         keyword.last_rank_date < today_zero_hour:

#                     update_keyword_rank(db, user_id=user.id, keyword_id=keyword.id,
#                                         keyword=keyword.keyword, domain_url=domain.url)


# def update_keyword_rank(db, user_id, keyword_id, keyword, domain_url):
#     out_scraper = scraper(keyword, domain_url, True)
#     obj_in = {'keyword_id': keyword_id,
#               'rank': out_scraper['rank']}
#     rank_service.create(db, obj_in=RankRequestSchema(**obj_in))
#     obj_in = {'last_rank': out_scraper['rank'],
#               'last_rank_date': datetime.now()}
#     keyword_service.update_by_owner(
#         db, id=keyword_id,  owner_id=user_id, obj_in=obj_in)

#     print(
#         f"{keyword}, com posição {out_scraper['rank']}")
