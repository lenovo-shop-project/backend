from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin, auth, client

app = FastAPI(title="Lenovo Shop API")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    ],
    allow_headers=["Authorization"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(client.router)

@app.get("/")
async def root():
    return {"message": "API работает"}