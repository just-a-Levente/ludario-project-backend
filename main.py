from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from routers.boardgame_router import boardgame_router
from routers.status_router import status_router

app = FastAPI(title="LudarioAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boardgame_router)
app.include_router(status_router)


# @app.exception_handler(BoardgameValidationException)
# async def boardgame_validation_exception_handler(request, exception: BoardgameValidationException):
#     return Response(content={"message": f"{exception}"}, status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/")
async def root():
    return {"message": "Ludario API root"}
