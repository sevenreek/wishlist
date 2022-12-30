import uvicorn
from fastapi import FastAPI, status, Depends
from enum import Enum
from sqlmodel import Session

from .routes.auth import router as auth_router
from .routes.wishlist import router as wishlists_router
from app.models.item import Item, ItemCRUD, ItemRead, ItemCreate
from app.db import get_async_session

app = FastAPI()

app.include_router(auth_router)
app.include_router(wishlists_router)

@app.get('/')
async def root():
    return {'message': 'Hello world!'}

if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
