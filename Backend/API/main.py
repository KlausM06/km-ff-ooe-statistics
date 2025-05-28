from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.other_router import router as other_router
import uvicorn

origins = [
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

app.include_router(other_router, prefix="", tags=["other"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
