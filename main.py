from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()


@app.get("/")
async def root():
    return "Ludario API root"