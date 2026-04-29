from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import database 

app = FastAPI(
    title="Olist Dashboard API",
    description="Backend API serving data for the Olist E-commerce Dashboard"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Default Vite port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# To run the server locally:
# uvicorn src.main:app --reload

# ==========================================
# API ENDPOINTS
# ==========================================

@app.get("/api/orders/daily")
def get_daily_orders():
    """Returns the number of orders per day."""
    conn = database.get_connection()
    df = database.get_orders_per_day(conn)
    conn.close()
    
    # Format for Plotly.js: Columnar arrays
    return df.to_dict(orient="list")

@app.get("/api/orders/hourly")
def get_hourly_orders():
    return None

@app.get("/api/categories/sales")
def get_category_sales():
    return None
