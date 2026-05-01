from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from routers.boardgame_router import boardgame_router
from routers.status_router import status_router
from routers.faker_router import faker_router

app = FastAPI(title="LudarioAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: not allow every IP, just the VM's
    allow_credentials=False,   # allow_credentials is set to false cuz of wildcard, CHANGE LATER
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boardgame_router)
app.include_router(status_router)
app.include_router(faker_router)


@app.get("/")
async def root():
    return {"message": "Ludario API root"}
