import uvicorn
from fastapi import FastAPI, status, Depends
from enum import Enum
from models.item import Item, ItemInput, ItemOutput, ItemCRUD
from db import get_async_session
from sqlmodel import Session

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello world!'}


@app.get('/list/{list_id}', response_model=list[Item], response_model_exclude_unset=True)
async def show_list_items(list_id: int, skip: int = 0, limit: int = 1, search: str | None = None):
    wishlist = next((wlist for wlist in wishlists if wlist['id'] == list_id), None)
    if search:
        return list(filter(lambda item: item['name'] and search.casefold() in item['name'].casefold(), wishlist['items']))[skip:skip+limit]
    else: 
        return wishlist['items'][skip:skip+limit]

@app.post('/list/{list_id}/items', status_code=status.HTTP_201_CREATED, response_model=ItemOutput)
async def add_item(item: ItemInput, Items=Depends(ItemCRUD.async_depend)):
    breakpoint()
    return None
    

if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
