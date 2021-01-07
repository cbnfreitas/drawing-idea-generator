
# from typing import Any, Dict

# from app.models.rank_model import RankModel
# from app.schemas.rank_schema import RankRequestSchema
# from app.services import rank_service
# from app.tests.utils import random_integer
# from sqlalchemy.orm import Session


# def create_random_rank_schema(random_rank: int = None, random_keyword_id: int = None) -> RankRequestSchema:
#     if not random_rank:
#         random_rank = random_integer()
#     if not random_keyword_id:
#         random_keyword_id = random_integer()
#     return RankRequestSchema(rank=random_rank, keyword_id=random_keyword_id)


# def create_random_rank_with_service(db: Session, random_rank: int = None, random_keyword_id: int = None) -> RankModel:
#     random_rank_schema = create_random_rank_schema(
#         random_rank, random_keyword_id)
#     return rank_service.create(db, obj_in=random_rank_schema)


# def create_random_rank_dict(random_rank: int = None, random_keyword_id: int = None) -> Dict[str, Any]:
#     return create_random_rank_schema(random_rank, random_keyword_id).dict()


# def assert_schema_db_rank(schema: RankRequestSchema, model: RankModel):
#     assert schema.rank == model.rank
#     assert schema.keyword_id == model.keyword_id
