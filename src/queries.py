# ==========================================
# CONSTANTS & PLACEHOLDERS
# ==========================================


# ==========================================
# SQL QUERIES
# ==========================================

# 1. Orders per day
orders_per_day = """
SELECT
    DATE(order_purchase_timestamp) AS day,
    COUNT(*) AS order_count
FROM orders
GROUP BY day
"""

# 2. Orders per city (Top 10)
orders_per_city = """
SELECT
    customer_city AS customer_city,
    UPPER(customer_city) AS city,
    COUNT(orders.order_id) as city_order_count
FROM
    customers
    JOIN orders USING (customer_id)
GROUP BY customer_city
ORDER BY city_order_count DESC
LIMIT 10
"""

# 3. Order price statistics
order_price_stats = """
SELECT
    MIN(order_order_price) AS min_order_price,
    ROUND(AVG(order_price), 2) AS avg_order_price,
    MAX(order_price) AS max_order_price
FROM (
    SELECT
        orders.order_id,
        SUM(order_items.price + order_items.freight_value) AS order_price
    FROM orders
        JOIN order_items USING (order_id)
    GROUP BY orders.order_id
)
"""

# 4. Daily Sales Per Category (Note: This is formatted to accept a python variable 'selected_categories')
daily_sales_per_category = """
SELECT
    DATE(order_purchase_timestamp) AS date,
    -- Days since 2017-01-01
    CAST(JULIANDAY(order_purchase_timestamp) - JULIANDAY('2017-01-01') AS INTEGER) AS day,
    product_category_name_english AS category,
    SUM(price) AS sales
FROM
    orders
    JOIN order_items USING (order_id)
    JOIN products USING (product_id)
    JOIN product_category_name_translation USING (product_category_name)
WHERE
    order_purchase_timestamp BETWEEN '2017-01-01' AND '2018-08-29'
    AND category IN {selected_categories}
GROUP BY
    day,
    product_category_name_english
"""

# 5. Linear Regression (Slope and Intercept) per category using a CTE
lm_per_category = f"""
WITH DailySalesPerCategory AS (
    {daily_sales_per_category}
)
SELECT
    category,
    -- Slope
    (COUNT(*) * SUM(day * sales) - SUM(day) * SUM(sales)) /
    (COUNT(*) * SUM(day * day) - SUM(day) * SUM(day))
    AS slope,
    -- Intercept
    (SUM(sales) -
    ((COUNT(*) * SUM(day * sales) - SUM(day) * SUM(sales)) /
    (COUNT(*) * SUM(day * day) - SUM(day) * SUM(day))) *
    SUM(day)) / COUNT(*)
    AS intercept
FROM
    DailySalesPerCategory
GROUP BY
    category
"""

# ==========================================
# MISSING QUERIES 
# ==========================================
