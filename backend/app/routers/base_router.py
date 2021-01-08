
from typing import Any, Dict, List, TypeVar

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel as BaseSchema
from sqlalchemy.orm import Session

from ..core.depends import (get_admin_from_access_token, get_db,
                            get_user_from_access_token)
from ..schemas.msg_schema import MsgResponseSchema
from ..services import BaseService


def build_simple_crud(
    router: APIRouter,
    uri: str,
    entity_name_plural: str,
    entity_name: str,
    base_service: BaseService,
    request_schema_type: Any,  # TODO
    response_schema_type: Any,  # TODO
    options: Dict[str, Any] = {},
    # admin_only: bool = True
):
    entity_id_name = f"{entity_name}_id"
    # args = Depends(
    #     get_admin_from_access_token) if admin_only else pass

    if not 'create' in options or options['create'] == True:
        @router.post(uri,
                     summary=f"Create a new {entity_name}",
                     response_model=response_schema_type
                     )
        def create(
                db: Session = Depends(get_db),
                *,
                obj_in: request_schema_type,
        ) -> Any:
            """
            Create an entity.
            """
            try:
                entity = base_service.create(db, obj_in=obj_in)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"?")

            if not entity:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No {entity_name} with {entity_id_name}={id}.")

            return entity

    if not 'read_one' in options or options['read_one'] == True:
        @router.get(f"{uri}/{{{entity_id_name}}}",
                    summary=f"Read a single {entity_name}",
                    response_model=response_schema_type,
                    responses={status.HTTP_404_NOT_FOUND: {
                        "model": MsgResponseSchema}}
                    )
        def read_one(
                db: Session = Depends(get_db),
                *,
                id: int = Path(..., alias=entity_id_name)
        ) -> Any:
            """
            Get an entity.
            """
            try:
                entity = base_service.read(db, id=id)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No {entity_name} with {entity_id_name}={id}.")

            return entity

    if not 'read_many' in options or options['read_many'] == True:
        @router.get(uri,
                    summary=f"Read many {entity_name_plural}",
                    response_model=List[response_schema_type]
                    )
        def read_many(
                db: Session = Depends(get_db),
                *,
                skip: int = None,
                limit: int = None
        ) -> Any:
            """
            Retrieve many entities. It includes pagination if skip and limit are provided.
            """

            try:
                entities = base_service.read_many(db, skip=skip, limit=limit)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"?")

            return entities

    # if not 'update' in options or options['update'] == True:
    #     @router.put(f"{uri}/{{{entity_id_name}}}",
    #                 summary=f"Update a single {entity_name}",
    #                 response_model=response_schema_type,
    #                 responses={status.HTTP_404_NOT_FOUND: {
    #                     "model": MsgResponseSchema}}
    #                 )
    #     def update(
    #             db: Session = Depends(get_db),
    #             *,
    #             id: int = Path(..., alias=entity_id_name),
    #             obj_in: request_schema_type
    #     ) -> Any:
    #         """
    #         Update an entity.
    #         """
    #         try:
    #             entity = base_service.update(db, id=id, obj_in=obj_in)
    #         except Exception as e:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail=f"No {entity_name} with {entity_id_name}={id}.")

    #         return entity

    # if not 'delete' in options or options['delete'] == True:
    #     @router.delete(f"{uri}/{{{entity_id_name}}}",
    #                    summary=f"Delete a single {entity_name}",
    #                    status_code=status.HTTP_204_NO_CONTENT,
    #                    responses={status.HTTP_404_NOT_FOUND: {
    #                        "model": MsgResponseSchema}}
    #                    )
    #     def delete(
    #             db: Session = Depends(get_db),
    #             *,
    #             id: int = Path(..., alias=entity_id_name),
    #     ) -> Any:
    #         """
    #         Delete an entity.
    #         """
    #         try:
    #             base_service.delete(db, id=id)
    #         except Exception as e:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail=f"No {entity_name} with {entity_id_name}={id}.")
    #             # e.args[0]
    #         return JSONResponse()

    return


# def build_crud_by_owner(
#     router: APIRouterType,
#     entity_name: str,
#     entity_name_plural: str,
#     base_service_by_owner: Any,  # TODO
#     request_schema_type: Any,  # TODO
#     response_schema_type: Any,  # TODO
#     options: Dict[str, Any] = {},
# ):

#     entity_id_name = f"{entity_name}_id"
#     uri = f"/{entity_name_plural}"

#     if not 'create' in options or options['create'] == True:
#         @router.post(uri,
#                      summary=f"Create a new {entity_name}",
#                      response_model=response_schema_type
#                      )
#         def create(
#                 db: Session = Depends(get_db),
#                 user_token_data: Dict[str, Any] = Depends(
#                     get_user_from_access_token),
#                 *,
#                 obj_in: request_schema_type
#         ) -> Any:
#             """
#             Create an entity.
#             """
#             entity = base_service_by_owner.create_by_owner(
#                 db, obj_in=obj_in, owner_id=user_token_data["user_id"])
#             return entity

#     if not 'read_many' in options or options['read_many'] == True:
#         @router.get(uri,
#                     summary=f"Read many {entity_name_plural}",
#                     response_model=List[response_schema_type]
#                     )
#         def read_many(
#                 db: Session = Depends(get_db),
#                 user_token_data: Dict[str, Any] = Depends(
#                     get_user_from_access_token),
#                 *,
#                 skip: int = 0,
#                 limit: int = 100
#         ) -> Any:
#             """
#             Retrieve many entities including pagination.
#             """
#             entities = base_service_by_owner.read_many_by_owner(
#                 db, skip=skip, limit=limit, owner_id=user_token_data["user_id"])
#             return entities

#     if not 'read_one' in options or options['read_one'] == True:
#         @router.get(f"{uri}/{{{entity_id_name}}}",
#                     summary=f"Read a single {entity_name}",
#                     response_model=response_schema_type,
#                     responses={status.HTTP_404_NOT_FOUND: {"model": Message}}
#                     )
#         def read_one(
#                 db: Session = Depends(get_db),
#                 user_token_data: Dict[str, Any] = Depends(
#                     get_user_from_access_token),
#                 *,
#                 id: int = Path(..., alias=entity_id_name)
#         ) -> Any:
#             """
#             Get an entity.
#             """
#             entity = base_service_by_owner.read_by_owner(
#                 db, id=id, owner_id=user_token_data["user_id"])
#             if not entity:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail=f"No {entity_name} with {entity_id_name}={id}.")
#             return entity

#     if not 'update' in options or options['update'] == True:
#         @router.put(f"{uri}/{{{entity_id_name}}}",
#                     summary=f"Update a single {entity_name}",
#                     response_model=response_schema_type,
#                     responses={status.HTTP_404_NOT_FOUND: {"model": Message}}
#                     )
#         def update(
#                 db: Session = Depends(get_db),
#                 user_token_data: Dict[str, Any] = Depends(
#                     get_user_from_access_token),
#                 *,
#                 id: int = Path(..., alias=entity_id_name),
#                 obj_in: request_schema_type
#         ) -> Any:
#             """
#             Update an entity.
#             """
#             entity = base_service_by_owner.update_by_owner(
#                 db, id=id, obj_in=obj_in, owner_id=user_token_data["user_id"])
#             if not entity:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail=f"No {entity_name} with {entity_id_name}={id}.")
#             return entity

#     if not 'delete' in options or options['delete'] == True:
#         @router.delete(f"{uri}/{{{entity_id_name}}}",
#                        summary=f"Delete a single {entity_name}",
#                        status_code=status.HTTP_204_NO_CONTENT,
#                        responses={status.HTTP_404_NOT_FOUND: {
#                            "model": Message}}
#                        )
#         def delete(
#                 db: Session = Depends(get_db),
#                 user_token_data: Dict[str, Any] = Depends(
#                     get_user_from_access_token),
#                 *,
#                 id: int = Path(..., alias=entity_id_name),
#         ) -> Any:
#             """
#             Delete an entity.
#             """
#             entity = base_service_by_owner.delete_by_owner(
#                 db, id=id, owner_id=user_token_data["user_id"])
#             if not entity:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND,
#                     detail=f"No {entity_name} with {entity_id_name}={id}.")

#             return JSONResponse()

#     return
