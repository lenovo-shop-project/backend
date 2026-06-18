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
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(client.router)

@app.get("/")
async def root():
    return {"message": "API работает"}

# Временный эндпоинт
@app.get("/products/top")
async def get_mock_products():
    # Временная заглушка для демонстрации интеграции
    return [
        {
            "id": 1, 
            "name": "Lenovo Legion 5 Pro", 
            "price": 54999, 
            "image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcTts9zE2kEFUcFsYcNVTE-OLhoXR3c92HuK3CKWp-grmOTxtSIJwkzMUmmoFun9e1hgCcRrgJNx8KYpfDLQ26Cy3bGnibPxZRTXDoxqVgO7WPx1CPVr6XJcrCdsXZrhyhdij4n8TQLh&usqp=CAc"
        },
        {
            "id": 2, 
            "name": "ThinkPad X1 Carbon", 
            "price": 72000, 
            "image": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcQv15jTOj1IpemYzdih8s6utP5V_X09CVrNoYstHMabOgUsgu7Ud9GTIZu66mJuq8w92uBLWN4JLlmnFXdRcRE4qYLZdskQ5wv5Xn7eG4mi7iWBQ99r3ayY5uWFoAl6VjwwGRJt7A&usqp=CAc"
        },
        {
            "id": 3, 
            "name": "IdeaPad Gaming 3", 
            "price": 35000, 
            "image": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTM967SRixsZYurIW2ADVf6E6MrPhgFMKyBjYo3jSIH3wbqA3iq-_abF80VvSpnNX_VTHbn0aJDLQigSv9f7BiGO4bR23bv2YtkrNFKdT0FRZBTmjGQFFNkmQH7kzuyU7cSNwf_kFE3KQ&usqp=CAc"
        }
    ]