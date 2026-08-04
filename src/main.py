import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess
from src import queries
from src import database
from src import utils

# Load .env file
load_dotenv()

app = FastAPI(
    title="Olist Dashboard API",
    description="Backend API serving data for the Olist E-commerce Dashboard"
)

origins_str = os.getenv("CORS_ORIGINS", "")

origins = [origin.strip() for origin in origins_str.split(",") if origin.strip()]

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
    """
    Retrieves qualified vs closed leads and conversion rates by origin.
    Formatted for a dual-axis Plotly chart.
    """
    conn = None
    try:
        conn = database.get_connection()
        # Execute the raw SQL from queries.py
        df = pd.read_sql_query(queries.lead_conversion, conn)

        # Clean the origin names for the UI
        df['origin'] = df['origin'].str.replace('_', ' ').str.title()

        return {
            "origins": df['origin'].tolist(),
            "qualified_leads": df['qualified_leads'].tolist(),
            "closed_leads": df['closed_leads'].tolist(),
            "conversion_rate": df['conversion_rate'].tolist()
        }

    except Exception as e:
        print(f"Error fetching lead conversions: {e}")
        return {"error": str(e)}
        
    finally:
        if conn:
            conn.close()

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
    conn = None 
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.product_weights, conn)
        top_categories = df['category'].value_counts().nlargest(5).index

        result = {}
        for cat in top_categories:
             cat_df = df[df['category'] == cat]
             filtered_cat_df = utils.remove_outliers_by_category(cat_df, 'weight', 0.8)
             result[cat] = filtered_cat_df['weight'].tolist()

        return result
        
    except Exception as e:
        print(f"Error fetching category weights: {e}")
        return {"error": str(e)}
        
    finally:
        if conn:
            conn.close()

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
    """
    Retrieves the total count of reviews grouped by their 1-5 star score.
    """
    conn = None
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.review_score_distribution, conn)
        
        # Format the X-axis labels to look like "1 ★", "2 ★", etc.
        df['review_score_label'] = df['review_score'].astype(str) + " ★"

        return {
            "scores": df['review_score_label'].tolist(),
            "counts": df['total_reviews'].tolist()
        }

    except Exception as e:
        print(f"Error fetching review distribution: {e}")
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()

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
        if conn:
            conn.close()

@app.get("/api/delivery/trend")
def get_delivery_trend():
    """
    Retrieves the daily average delivery time and calculates a LOWESS trendline.
    """
    conn = None
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.daily_delivery_time, conn)

        # Drop any weird outliers or nulls to keep the math clean
        df = df.dropna()

        # Calculate the LOWESS trendline
        # frac=0.1 means it uses 10% of the data points for each local regression (smooths it nicely)
        # We use np.arange for the X-axis because LOWESS requires numeric inputs, not datetime objects
        trend_data = lowess(df['avg_delivery_days'], np.arange(len(df)), frac=0.1)

        # Extract the smoothed Y-values (the second column of the lowess output array)
        df['trendline'] = trend_data[:, 1]

        # Package it up as a dictionary of arrays for Plotly
        return {
            "dates": df['order_date'].tolist(),
            "actual_days": df['avg_delivery_days'].tolist(),
            "trend_days": df['trendline'].tolist()
        }

    except Exception as e:
        print(f"Error fetching delivery trend: {e}")
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()

@app.get("/api/delivery/stages")
def get_delivery_stages():
    """
    Retrieves the average days spent in each delivery stage for the top 10 cities.
    """
    conn = None
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.city_delivery_stages, conn)

        return {
            # Title-case the city names so 'sao paulo' becomes 'Sao Paulo'
            "cities": df['city'].str.title().tolist(),
            "approval_days": df['approval_days'].tolist(),
            "carrier_days": df['carrier_days'].tolist(),
            "transit_days": df['transit_days'].tolist(),
        }

    except Exception as e:
        print(f"Error fetching delivery stages: {e}")
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()

@app.get("/api/leads/origin")
def get_leads_by_origin():
    """
    Retrieves the count of marketing qualified leads (MQLs) grouped by their acquisition origin.
    """
    conn = None
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.leads_by_origin, conn)

        # Clean up the origin names for the frontend (e.g. 'organic_search' -> 'Organic Search')
        df['origin'] = df['origin'].str.replace('_', ' ').str.title()

        return {
            "origins": df['origin'].tolist(),
            "leads": df['total_leads'].tolist()
        }

    except Exception as e:
        print(f"Error fetching leads by origin: {e}")
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()

@app.get("/api/sellers/review-sales")
def get_review_sales_scatter():
    """
    Retrieves total sales and average review scores per seller for clustering scatter plot.
    """
    conn = None
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.seller_review_vs_sales, conn)

        # Round the average score to 2 decimal places for cleaner tooltips
        df['avg_score'] = df['avg_score'].round(2)
        # Round sales to 2 decimal places
        df['total_sales'] = df['total_sales'].round(2)

        return {
            "seller_ids": df['seller_id'].tolist(),
            "total_sales": df['total_sales'].tolist(),
            "avg_scores": df['avg_score'].tolist(),
            "order_counts": df['order_count'].tolist()
        }

    except Exception as e:
        print(f"Error fetching review vs sales data: {e}")
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()

@app.get("/api/predictions/regression-trend")
def get_regression_trend():
    """
    Retrieves daily sales and calculates a linear regression trendline.
    """
    conn = None
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.daily_sales_trend, conn)
        
        # Drop any null dates that might have slipped through
        df = df.dropna(subset=['order_date', 'total_sales'])
        
        # Calculate the linear regression line (1st degree polynomial)
        # We use a simple numeric sequence (0 to N) for the X-axis in the math
        x_numeric = np.arange(len(df))
        z = np.polyfit(x_numeric, df['total_sales'], 1)
        p = np.poly1d(z)
        
        # Generate the Y values for the regression line
        df['regression_line'] = p(x_numeric).round(2)
        df['total_sales'] = df['total_sales'].round(2)

        return {
            "dates": df['order_date'].tolist(),
            "actual_sales": df['total_sales'].tolist(),
            "regression_trend": df['regression_line'].tolist()
        }

    except Exception as e:
        print(f"Error fetching regression trend: {e}")
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()

@app.get("/api/predictions/sales-forecast")
def get_sales_forecast():
    """
    Retrieves historical monthly sales and projects a forecast through Dec 2018,
    accounting for the November (Black Friday) seasonal spike.
    """
    conn = None
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.monthly_sales_history, conn)

        # 1. Calculate the baseline linear trend
        x_numeric = np.arange(len(df))
        z = np.polyfit(x_numeric, df['total_sales'], 1)
        p = np.poly1d(z)

        # 2. Calculate the historical November multiplier (Black Friday impact)
        nov_17_idx = df.index[df['order_month'] == '2017-11'].tolist()
        if nov_17_idx:
            idx = nov_17_idx[0]
            nov_17_actual = df.loc[idx, 'total_sales']
            nov_17_trend = p(idx)
            nov_multiplier = nov_17_actual / nov_17_trend if nov_17_trend > 0 else 1.5
        else:
            nov_multiplier = 1.5 # Fallback multiplier

        # 3. Project the next 4 months (Sept, Oct, Nov, Dec 2018)
        future_months = ['2018-09', '2018-10', '2018-11', '2018-12']
        future_x = np.arange(len(df), len(df) + 4)
        base_forecast = p(future_x)

        # Apply the multiplier to November 2018 (index 2 of future array)
        forecast_values = base_forecast.copy()
        forecast_values[2] = forecast_values[2] * nov_multiplier

        # 4. Prepare arrays for Plotly
        # To connect the lines visually, the forecast array must start with the LAST actual month's value
        all_months = df['order_month'].tolist() + future_months

        # Actuals: [val, val, val, null, null, null, null]
        actuals = df['total_sales'].round(2).tolist() + [None, None, None, None]

        # Forecast: [null, null, ..., LAST_ACTUAL_VAL, forecast1, forecast2, forecast3, forecast4]
        last_actual = df['total_sales'].iloc[-1]
        forecast = [None] * (len(df) - 1) + [round(last_actual, 2)] + [round(val, 2) for val in forecast_values]

        return {
            "months": all_months,
            "actual_sales": actuals,
            "forecast_sales": forecast
        }

    except Exception as e:
        print(f"Error generating sales forecast: {e}")
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()

@app.get("/api/predictions/rfm")
def get_rfm_segmentation():
    """
    Calculates Recency, Frequency, and Monetary values for all customers,
    assigns behavioral segments, and returns a representative sample for UI performance.
    """
    conn = None
    try:
        conn = database.get_connection()
        df = pd.read_sql_query(queries.rfm_raw_data, conn)

        # 1. Calculate Recency (Days since last purchase)
        df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])
        # Reference date: 1 day after the maximum date in the dataset
        ref_date = df['last_purchase_date'].max() + pd.Timedelta(days=1)
        df['recency'] = (ref_date - df['last_purchase_date']).dt.days

        # 2. Assign Scores (1-4 scale)
        # Recency: Lower days = higher score (4 is most recent)
        df['r_score'] = pd.qcut(df['recency'], q=4, labels=[4, 3, 2, 1])
        # Monetary: Higher spend = higher score
        df['m_score'] = pd.qcut(df['monetary'], q=4, labels=[1, 2, 3, 4])
        # Frequency: Olist is ~95% single-purchase. Manual scoring prevents quantile errors.
        df['f_score'] = df['frequency'].apply(lambda x: 1 if x == 1 else (2 if x == 2 else 3))

        # 3. Define Segmentation Logic
        def assign_segment(row):
            r, f, m = row['r_score'], row['f_score'], row['m_score']
            if r >= 3 and (f >= 2 or m >= 3): return "Champions"
            if r >= 3 and f == 1 and m <= 2: return "Recent/Promising"
            if r == 2 and m >= 3: return "Loyal"
            if r <= 2 and (f >= 2 or m >= 3): return "At Risk"
            return "Hibernating"

        df['segment'] = df.apply(assign_segment, axis=1)

        # 4. Sample for UI Performance (2000 random customers)
        df_sample = df.sample(n=2000, random_state=42)

        return {
            "recency": df_sample['recency'].tolist(),
            "frequency": df_sample['frequency'].tolist(),
            "monetary": df_sample['monetary'].round(2).tolist(),
            "segment": df_sample['segment'].tolist()
        }

    except Exception as e:
        print(f"Error calculating RFM: {e}")
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()
