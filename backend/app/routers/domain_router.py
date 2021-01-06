# from fastapi import APIRouter, Depends, HTTPException, Path, status
# from pydantic import BaseModel as BaseSchema
# from sqlalchemy.orm import Session

# from ..core.base_router import build_crud_by_owner
# from ..core.depends import get_db
# from ..schemas.domain_schema import DomainRequestSchema, DomainResponseSchema
# from ..services import domain_service

# domain_router = APIRouter()


# build_crud_by_owner(domain_router, "domain", "domains", domain_service,
#                     DomainRequestSchema, DomainResponseSchema,
#                     options={'update': False})
