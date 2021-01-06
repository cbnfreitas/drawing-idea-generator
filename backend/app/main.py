import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import s
from .core.baseline import baseline
from .core.session import SessionLocal
# from .jobs.rank_job import rank_job
from .routers import api_router

db = SessionLocal()
baseline(db)
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(api_router)


# @app.on_event("startup")
# async def start_event():
#     asyncio.create_task(scheduler())


# async def scheduler():
#     rank_job(db)
#     while True:
#         await asyncio.sleep(s.RANK_JOB_HOURS * 3600)
#         rank_job(db)
