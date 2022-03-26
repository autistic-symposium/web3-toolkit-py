
from .routes import router as LocationRouter
from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {
        "message": "$CHOICES Timezone API ⏳✨. Try /docs to learn about this API"
    }

app.include_router(LocationRouter, prefix="/tzone")
