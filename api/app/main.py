import uvicorn
from fastapi import FastAPI

from .routes.auth import router as auth_router
from .routes.wishlist import router as wishlists_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(wishlists_router)

@app.get('/')
async def root():
    return {'message': 'Hello world!'}

if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
