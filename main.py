from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Додаємо CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Дозволяємо доступ з усіх джерел
    allow_credentials=True,
    allow_methods=["*"],  # Дозволяємо всі методи
    allow_headers=["*"],  # Дозволяємо всі заголовки
)

PRODUCTS_FILE = "products.json"

class Product(BaseModel):
    name: str
    days: int

# Завантажуємо продукти з файлу
def load_products():
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Зберігаємо продукти в файл
def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

# Головний маршрут, щоб не було 404
@app.get("/")
def read_root():
    return {"message": "API is running"}

# Отримати список продуктів
@app.get("/products")
def get_products():
    return load_products()

# Додати продукт
@app.post("/products")
def add_product(product: Product):
    products = load_products()
    products.append(product.dict())
    save_products(products)
    return {"message": "Продукт додано"}

# Оновити продукт
@app.put("/products/{index}")
def update_product(index: int, product: Product):
    products = load_products()
    if index >= len(products):
        raise HTTPException(status_code=404, detail="Продукт не знайдено")
    products[index] = product.dict()
    save_products(products)
    return {"message": "Продукт оновлено"}

# Видалити продукт
@app.delete("/products/{index}")
def delete_product(index: int):
    products = load_products()
    if index >= len(products):
        raise HTTPException(status_code=404, detail="Продукт не знайдено")
    products.pop(index)
    save_products(products)
    return {"message": "Продукт видалено"}
