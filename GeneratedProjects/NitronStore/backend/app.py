from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI(
    title="NitronStore API",
    version="1.0"
)


# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Store products
products = [

    {
        "id": 1,
        "name": "Premium Hoodie",
        "price": 150,
        "category": "Hoodies",
        "image": "hoodie.jpg",
        "description": "Premium streetwear hoodie",
        "size": "S,M,L,XL",
        "color": "Black",
        "stock": 20
    },

    {
        "id": 2,
        "name": "Jordan Air Max Shoes",
        "price": 1000,
        "category": "Shoes",
        "image": "jordan.jpg",
        "description": "Luxury streetwear shoes",
        "size": "40,41,42,43",
        "color": "White",
        "stock": 15
    },

    {
        "id": 3,
        "name": "Anime BMW T-Shirt",
        "price": 150,
        "category": "T-Shirts",
        "image": "tshirt.jpg",
        "description": "Anime and BMW inspired design",
        "size": "S,M,L,XL",
        "color": "Black",
        "stock": 50
    },

    {
        "id": 4,
        "name": "Designer Trousers",
        "price": 180,
        "category": "Trousers",
        "image": "trousers.jpg",
        "description": "Modern fashion trousers",
        "size": "S,M,L,XL",
        "color": "Black",
        "stock": 30
    }

]


@app.get("/")
def home():

    return {
        "project": "NitronStore",
        "message": "NitronStore backend online"
    }



@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



@app.get("/products")
def get_products():

    return products



@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:

        if product["id"] == product_id:
            return product

    return {
        "error": "Product not found"
    }



if __name__ == "__main__":

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
