import sqlite3
import pandas as pd
import sys
from src import queries

def get_connection(db_path="../data/olist.sqlite"):
    """
    Adjust the db_path depending on where you run the script from.
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database '{db_path}': {e}")
        sys.exit(1)

def get_orders_per_day(conn):
    return pd.read_sql_query(queries.orders_per_day, conn)

def get_orders_per_hour(conn):
    df = pd.read_sql_query(queries.orders_per_day_of_the_week_and_hour, conn)
    return df.set_index('day_of_week_name')

def get_order_product_and_shipping_costs(conn):
    return pd.read_sql_query(queries.order_product_and_shipping_costs, conn)

def get_category_sales_summary(conn):
    return pd.read_sql_query(queries.category_sales_summary, conn)

def get_ordered_categories(conn):
    return pd.read_sql_query(queries.ordered_categories, conn)

def get_categories_by_median(conn):
    return pd.read_sql_query(queries.categories_by_median, conn)

def get_monthly_sales_selected_categories(conn):
    df = pd.read_sql_query(queries.monthly_sales_selected_categories, conn)
    df = df.set_index('year_month')
    df.index = pd.to_datetime(df.index) # Format datetime to be pandas friendly
    return df
