import uvicorn
from fastapi import FastAPI, status, Depends
from enum import Enum
from sqlmodel import Session

from .routes.auth import router as auth_router
from app.models.item import Item, ItemCRUD, ItemRead, ItemCreate
from app.db import get_async_session

app = FastAPI()

app.include_router(auth_router)

@app.get('/')
async def root():
    return {'message': 'Hello world!'}


@app.get('/list/{list_id}', response_model=list[Item], response_model_exclude_unset=True)
async def show_list_items(list_id: int, skip: int = 0, limit: int = 1, search: str | None = None):
    return None

@app.post('/list/{list_id}/items', status_code=status.HTTP_201_CREATED, response_model=ItemRead)
async def add_item(item: ItemCreate, Items: ItemCRUD=Depends()):
    return None
    

if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
