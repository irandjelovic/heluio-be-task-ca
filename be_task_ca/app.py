from typing import Dict

from fastapi import FastAPI

from .item.api import item_router
from .user.api import user_router


app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)


@app.get("/")
async def root() -> Dict:
    return {
        "message": "Thanks for shopping at Nile!"
    }  # the Nile is 250km longer than the Amazon
