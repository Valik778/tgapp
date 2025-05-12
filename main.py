from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRODUCTS_FILE = "products.json"

class Product(BaseModel):
    name: str
    days: int

def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

@app.get("/products")
def get_products():
    return load_products()

@app.post("/products")
def add_product(product: Product):
    products = load_products()
    products.append(product.dict())
    save_products(products)
    return {"message": "Продукт додано"}

@app.put("/products/{index}")
def update_product(index: int, product: Product):
    products = load_products()
    if index >= len(products):
        raise HTTPException(status_code=404, detail="Продукт не знайдено")
    products[index] = product.dict()
    save_products(products)
    return {"message": "Продукт оновлено"}

@app.delete("/products/{index}")
def delete_product(index: int):
    products = load_products()
    if index >= len(products):
        raise HTTPException(status_code=404, detail="Продукт не знайдено")
    products.pop(index)
    save_products(products)
    return {"message": "Продукт видалено"}
