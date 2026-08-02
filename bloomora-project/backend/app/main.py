from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes_diet import router as diet_router

app = FastAPI(
    title="Bloomora API",
    description="Rule-based pregnancy nutrition plan generator, backed by IFCT 2017.",
    version="0.1.0",
)

# Open CORS for local development; tighten this before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diet_router)


@app.get("/health")
def health():
    return {"status": "ok"}


# Serves frontend/index.html at "/" so `uvicorn app.main:app` alone can run the whole app.
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
