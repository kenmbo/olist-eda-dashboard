from fastapi import FastAPI
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from src import queries
from src import database
from src import utils

app = FastAPI(
    title="Olist Dashboard API",
    description="Backend API serving data for the Olist E-commerce Dashboard"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Default Vite port
    "http://localhost:5174",  # Vite port + 1 (5173+1=5174), for debugging
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
    """Returns product and shipping costs for histograms."""
    conn = database.get_connection()
    df = database.get_order_product_and_shipping_costs(conn)
    conn.close()
    return df.to_dict(orient="list")

@app.get("/api/categories/weights")
def get_category_weights():
    """Returns product weights by category, with outliers removed for box plots."""
    conn = database.get_connection()
    df = database.get_ordered_categories(conn)
    
    # Optional: If median sorting array is needed on the frontend, fetch it here
    # median_df = database.get_categories_by_median(conn)
    
    conn.close()
    
    # Clean the data using your standard deviation logic
    clean_df = utils.remove_outliers_by_category(df, 'weight')
    return clean_df.to_dict(orient="list")

@app.get("/api/sales/monthly")
def get_monthly_sales():
    """Returns monthly sales for selected categories (Line Graph)."""
    conn = database.get_connection()
    df = database.get_monthly_sales_selected_categories(conn)
    conn.close()
    
    # Because 'year_month' was set as the index in database.py, we reset it 
    # so it gets included in the JSON response as a standard column.
    return df.reset_index().to_dict(orient="list")

@app.get("/api/sales/regression")
def get_sales_regression():
    """Returns slope and intercept for category sales (Trendlines)."""
    conn = database.get_connection()
    df = database.get_lm_per_category(conn)
    conn.close()
    return df.to_dict(orient="records") 
    # orient="records" is better for reading slope/intercept objects

@app.get("/api/sales/forecast")
def get_sales_forecast():
    """Returns the forecasted moving average sales for December 2018."""
    conn = database.get_connection()
    df = database.get_forecasted_sales_dec_2018(conn)
    conn.close()
    return df.to_dict(orient="list")

@app.get("/api/shipping/stages-by-city")
def get_shipping_stages():
    """Returns the average days for each order stage by city (Stacked Bar)."""
    conn = database.get_connection()
    df = database.get_order_stage_times_top_cities(conn)
    conn.close()
    return df.reset_index().to_dict(orient="list")

@app.get("/api/shipping/daily-average")
def get_daily_shipping_average():
    """Returns daily average shipping times."""
    conn = database.get_connection()
    df = database.get_daily_avg_shipping_time(conn)
    conn.close()
    return df.to_dict(orient="list")

@app.get("/api/reviews/distribution")
def get_review_distribution():
    """Returns the count of each review score."""
    conn = database.get_connection()
    df = database.get_review_score_count(conn)
    conn.close()
    return df.to_dict(orient="list")

@app.get("/api/customers/rfm")
def get_rfm_segments():
    """Returns RFM segmentation statistics for scatter plots."""
    conn = database.get_connection()
    df = database.get_rfm_buckets(conn)
    conn.close()
    return df.to_dict(orient="list")

@app.get("/api/customers/clv-map")
def get_clv_map_data():
    """Returns geographic coordinates, customer counts, and average CLV for the Mapbox graph."""
    conn = database.get_connection()
    df = database.get_avg_clv_per_zip_prefix(conn)
    conn.close()
    return df.to_dict(orient="list")

@app.get("/api/categories/monthly-sales")
def get_monthly_category_sales():
    """
    Retrieves monthly sales data for the top 5 highest-grossing categories.
    Formatted as a split JSON to generate parallel time-series traces in Plotly.
    """
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.monthly_category_sales, conn)
        top_categories = df.groupby('category')['total_sales'].sum().nlargest(5).index
        filtered_df = df[df['category'].isin(top_categories)]
        # Pivot table: Months become the index, Categories become the columns
        pivot_df = filtered_df.pivot(index='order_month', columns='category', values='total_sales')
        pivot_df = pivot_df.fillna(0)
        json_data = pivot_df.to_json(orient="split")
        return Response(content=json_data, media_type="application/json")
        
    except Exception as e:
        print(f"Error fetching monthly category sales: {e}")
        return {"error": str(e)}

    finally:
        # This will ALWAYS run, safely releasing the database lock
        if conn:
            conn.close()
