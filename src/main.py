from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import database
from src import utils

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
    """Returns order counts grouped by day of the week and hour."""
    conn = database.get_connection()
    df = database.get_orders_per_hour(conn)
    conn.close()
    
    # For a heatmap, we might need a specific format depending on how 
    # we set up the React component, but 'split' or 'index' often work best 
    # for 2D matrix data. Let's send the index, columns, and raw 2D array.
    return df.to_dict(orient="split")

@app.get("/api/categories/sales")
def get_category_sales():
    """Returns top categories by sales volume."""
    conn = database.get_connection()
    df = database.get_category_sales_summary(conn)
    conn.close()
    
    return df.to_dict(orient="list")

@app.get("/api/sellers/performance")
def get_seller_performance():
    """Returns review scores, total sales, and order volume per seller for scatter plotting."""
    conn = database.get_connection()
    df = database.get_seller_review_scores_and_sales(conn)
    conn.close()
    
    return df.to_dict(orient="list")

@app.get("/api/leads/conversion")
def get_lead_conversions():
    """Returns qualified vs closed leads and conversion rates by origin."""
    conn = database.get_connection()
    df = database.get_lead_conversion(conn)
    conn.close()
    
    return df.to_dict(orient="list")

@app.get("/api/sellers/distribution")
def get_seller_distribution():
    """Returns the count of sellers grouped by their total order volume buckets."""
    conn = database.get_connection()
    df = database.get_sellers_per_bucket(conn)
    conn.close()
    
    return df.to_dict(orient="list")

@app.get("/api/sellers/shipping-times")
def get_seller_shipping():
    """Returns delivery times categorized by seller order volume, with outliers removed."""
    conn = database.get_connection()
    df = database.get_seller_shipping_times(conn)
    conn.close()
    
    # Clean the data before sending it to the frontend
    clean_df = utils.remove_outliers_iqr(df, column='delivery_time', group_column='bucket')
    
    return clean_df.to_dict(orient="list")

@app.get("/api/orders/costs")
def get_order_costs():
    return None

@app.get("/api/categories/weights")
def get_category_weights():
    return None

@app.get("/api/sales/monthly")
def get_monthly_sales():
    return None

@app.get("/api/sales/regression")
def get_sales_regression():
    return None
