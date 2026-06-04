from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.boardgame_router import boardgame_router
from routers.review_router import review_router
from routers.status_router import status_router
from routers.faker_router import faker_router, faker_realtime_router
from routers.user_router import user_router
from routers.chat_router import chat_router, chat_realtime_router
from routers.log_router import log_router
from middleware.log_middleware import LogMiddleware


app = FastAPI(title="LudarioAPI")

app.add_middleware(LogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ludario-project.onrender.com", "https://ludario-project-new.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boardgame_router)
app.include_router(review_router)
app.include_router(status_router)
app.include_router(faker_router)
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(log_router)

app.include_router(chat_realtime_router)
app.include_router(faker_realtime_router)


@app.get("/")
async def root():
    return {"message": "Ludario API root"}
