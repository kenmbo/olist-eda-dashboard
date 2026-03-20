import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3
import seaborn as sns
import numpy as np
import plotly
import squarify
import statsmodels
import folium
import dash
import sys

try:
	file = open("olist.sqlite", "r")
	content = file.read()
	file.close()

except FileNotFoundError:
	print("Error: The file \'olist.sqlite\' is not found. Please place it in the same directory as this file. Exiting program.")
	sys.exit(1)

conn = sqlite3.connect('olist.sqlite') # SQL server connect to the database (local file)


# SQL QUERIES

orders_per_day = """
SELECT
    DATE(order_purchase_timestamp) AS day,
    COUNT(*) AS order_count
FROM orders
GROUP BY day
"""

order_day_hour = """
SELECT
    -- Day of the week abreviated
    CASE STRFTIME('%w', order_purchase_timestamp)
        WHEN '1' THEN 'Mon'
        WHEN '2' THEN 'Tue'
        WHEN '3' THEN 'Wed'
        WHEN '4' THEN 'Thu'
        WHEN '5' THEN 'Fri'
        WHEN '6' THEN 'Sat'
        WHEN '0' THEN 'Sun'
        END AS day_of_week_name,
    -- Day of the week as integer (Sunday=7)
    CAST(STRFTIME('%w', order_purchase_timestamp) AS INTEGER) AS day_of_week_int,
    -- Hour of the day (0-24)
    CAST(STRFTIME("%H", order_purchase_timestamp) AS INTEGER) AS hour
FROM orders
"""

count_orders_per_hour = ',\n    '.join([
    f'COUNT(CASE WHEN hour = {i} THEN 1 END) AS "{i}"' \
    for i in range(24)
])

orders_per_day_of_the_week_and_hour = f"""
WITH OrderDayHour AS (
    {order_day_hour}
)
SELECT
    day_of_week_name,
    {count_orders_per_hour}
FROM OrderDayHour
GROUP BY day_of_week_int
ORDER BY day_of_week_int
"""

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

orders_per_city_reversed = f"""
SELECT *
FROM ({orders_per_city})
ORDER BY city_order_count
"""

order_price_stats = """
SELECT
    MIN(order_price) AS min_order_price,
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

order_product_and_shipping_costs = """
SELECT
    orders.order_id,
    SUM(price) AS product_cost,
    SUM(freight_value) AS shipping_cost
FROM
    orders
    JOIN order_items USING (order_id)
WHERE order_status = 'delivered'
GROUP BY orders.order_id
"""

ranked_categories = """
SELECT
    product_category_name_english AS category,
    SUM(price) AS sales,
    RANK() OVER (ORDER BY SUM(price) DESC) AS rank
FROM order_items
    JOIN orders USING (order_id)
    JOIN products USING (product_id)
    JOIN product_category_name_translation USING (product_category_name)
WHERE order_status = 'delivered'
GROUP BY product_category_name_english
"""

category_sales_summary = f"""
WITH RankedCategories AS (
    {ranked_categories}
)

SELECT
    category,
    sales
FROM RankedCategories
WHERE rank <= 18
-- Other categories, aggregated
UNION ALL
SELECT
    'Other categories' AS category,
    SUM(sales) AS sales
FROM RankedCategories
WHERE rank > 18
"""


ordered_categories = f"""
SELECT
    product_weight_g AS weight,
    product_category_name_english AS category,
    ROW_NUMBER() OVER(PARTITION BY product_category_name_english ORDER BY product_weight_g)
        AS category_row_n,
    COUNT(*) OVER(PARTITION BY product_category_name_english) AS category_count
FROM
    products
    JOIN order_items USING (product_id)
    JOIN product_category_name_translation USING (product_category_name)
WHERE
    product_category_name_english IN {top_18_categories}
"""

ategories_by_median = f"""
WITH OrderedCategories AS (
    {ordered_categories}
)
SELECT category
FROM OrderedCategories
WHERE
    -- Odd number of products: Select the middle row
    (category_count % 2 = 1 AND category_row_n = (category_count + 1) / 2) OR
    -- Even number of products: Select the two middle rows to be averaged
    (category_count % 2 = 0 AND category_row_n IN ((category_count / 2), (category_count / 2 + 1)))
GROUP BY category
ORDER BY AVG(weight)
"""

selected_categories = ('health_beauty', 'auto', 'toys', 'electronics', 'fashion_shoes')

monthly_sales_selected_categories = f"""
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS year_month,
    SUM(CASE WHEN product_category_name_english = 'health_beauty' THEN price END) AS health_beauty,
    SUM(CASE WHEN product_category_name_english = 'auto' THEN price END) AS auto,
    SUM(CASE WHEN product_category_name_english = 'toys' THEN price END) AS toys,
    SUM(CASE WHEN product_category_name_english = 'electronics' THEN price END) AS electronics,
    SUM(CASE WHEN product_category_name_english = 'fashion_shoes' THEN price END) AS fashion_shoes
FROM orders
    JOIN order_items USING (order_id)
    JOIN products USING (product_id)
    JOIN product_category_name_translation USING (product_category_name)
WHERE order_purchase_timestamp >= '2017-01-01'
    AND product_category_name_english IN {selected_categories}
GROUP BY year_month
"""

daily_sales_per_category = f"""
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

forecasted_sales_dec_2018 = f"""
WITH DailySalesPerCategory AS (
    {daily_sales_per_category}
),
LmPerCategory AS (
    {lm_per_category}
),
ForecastedSales AS (
    SELECT
        DATE(date, '+1 year') AS date,
        category,
        -- Increase in predicted sales * sales 1 year ago
        (intercept + slope * (day + CAST(JULIANDAY('2018-12-31') - JULIANDAY('2017-12-31') AS INTEGER)))
            / (intercept + slope * day) * sales
            AS forecasted_sales
    FROM DailySalesPerCategory
        JOIN LmPerCategory USING (category)
    -- Filter for days of December 2018
    WHERE day + CAST(JULIANDAY('2018-12-31') - JULIANDAY('2017-12-31') AS INTEGER)
        BETWEEN CAST(JULIANDAY('2018-12-01') - JULIANDAY('2017-01-01') AS INTEGER)
        AND CAST(JULIANDAY('2018-12-31') - JULIANDAY('2017-01-01') AS INTEGER)
)
SELECT
    CAST(strftime('%d', date) AS INTEGER) AS december_2018_day,
    category,
    -- 5-day moving average
    AVG(forecasted_sales)
        OVER (PARTITION BY category ORDER BY date ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING)
        AS moving_avg_sales
FROM ForecastedSales
"""

order_stage_times_top_10_citites = f"""
SELECT
    UPPER(customer_city)
        AS city,
    AVG(JULIANDAY(order_approved_at) - JULIANDAY(order_purchase_timestamp))
        AS approved,
    AVG(JULIANDAY(order_delivered_carrier_date) - JULIANDAY(order_approved_at))
        AS delivered_to_carrier,
    AVG(JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_delivered_carrier_date))
        AS delivered_to_customer,
    AVG(JULIANDAY(order_estimated_delivery_date) - JULIANDAY(order_delivered_customer_date))
        AS estimated_delivery
FROM orders
    JOIN customers USING (customer_id)
WHERE  customer_city IN {tuple(top_cities['customer_city'])}
GROUP BY  customer_city
ORDER BY approved + delivered_to_carrier + delivered_to_customer DESC
"""

daily_avg_shipping_time = """
SELECT
    DATE(order_purchase_timestamp) AS purchase_date,
    AVG(JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_purchase_timestamp))
        AS avg_delivery_time
FROM orders
WHERE order_purchase_timestamp >= '2017-06-01' AND order_purchase_timestamp <= '2018-06-30'
GROUP BY DATE(order_purchase_timestamp)
"""

review_score_count = """
SELECT
    review_score,
    COUNT(*) AS count
FROM order_reviews
GROUP BY review_score
"""

rfm_buckets = """
-- Calculate RFM scores
WITH RecencyScore AS (
    SELECT customer_unique_id,
           MAX(order_purchase_timestamp) AS last_purchase,
           NTILE(5) OVER (ORDER BY MAX(order_purchase_timestamp) DESC) AS recency
    FROM orders
        JOIN customers USING (customer_id)
    WHERE order_status = 'delivered'
    GROUP BY customer_unique_id
),
FrequencyScore AS (
    SELECT customer_unique_id,
           COUNT(order_id) AS total_orders,
           NTILE(5) OVER (ORDER BY COUNT(order_id) DESC) AS frequency
    FROM orders
        JOIN customers USING (customer_id)
    WHERE order_status = 'delivered'
    GROUP BY customer_unique_id
),
MonetaryScore AS (
    SELECT customer_unique_id,
           SUM(price) AS total_spent,
           NTILE(5) OVER (ORDER BY SUM(price) DESC) AS monetary
    FROM orders
        JOIN order_items USING (order_id)
        JOIN customers USING (customer_id)
    WHERE order_status = 'delivered'
    GROUP BY customer_unique_id
),
-- Assign each customer to a group
RFM AS (
    SELECT last_purchase, total_orders, total_spent,
        CASE
            WHEN recency = 1 AND frequency + monetary IN (1, 2, 3, 4) THEN "Champions"
            WHEN recency IN (4, 5) AND frequency + monetary IN (1, 2) THEN "Can't Lose Them"
            WHEN recency IN (4, 5) AND frequency + monetary IN (3, 4, 5, 6) THEN "Hibernating"
            WHEN recency IN (4, 5) AND frequency + monetary IN (7, 8, 9, 10) THEN "Lost"
            WHEN recency IN (2, 3) AND frequency + monetary IN (1, 2, 3, 4) THEN "Loyal Customers"
            WHEN recency = 3 AND frequency + monetary IN (5, 6) THEN "Needs Attention"
            WHEN recency = 1 AND frequency + monetary IN (7, 8) THEN "Recent Users"
            WHEN recency = 1 AND frequency + monetary IN (5, 6) OR
                recency = 2 AND frequency + monetary IN (5, 6, 7, 8) THEN "Potential Loyalists"
            WHEN recency = 1 AND frequency + monetary IN (9, 10) THEN "Price Sensitive"
            WHEN recency = 2 AND frequency + monetary IN (9, 10) THEN "Promising"
            WHEN recency = 3 AND frequency + monetary IN (7, 8, 9, 10) THEN "About to Sleep"
        END AS RFM_Bucket
    FROM RecencyScore
        JOIN FrequencyScore USING (customer_unique_id)
        JOIN MonetaryScore USING (customer_unique_id)
)
-- Calculate group statistics for plotting
SELECT RFM_Bucket,
       AVG(JULIANDAY('now') - JULIANDAY(last_purchase)) AS avg_days_since_purchase,
       AVG(total_spent / total_orders) AS avg_sales_per_customer,
       COUNT(*) AS customer_count
FROM RFM
GROUP BY RFM_Bucket
"""

clv = """
WITH CustomerData AS (
    SELECT
        customer_unique_id,
        customer_zip_code_prefix AS zip_code_prefix,
        COUNT(DISTINCT orders.order_id) AS order_count,
        SUM(payment_value) AS total_payment,
        JULIANDAY(MIN(order_purchase_timestamp)) AS first_order_day,
        JULIANDAY(MAX(order_purchase_timestamp)) AS last_order_day
    FROM customers
        JOIN orders USING (customer_id)
        JOIN order_payments USING (order_id)
    GROUP BY customer_unique_id
)
SELECT
    customer_unique_id,
    zip_code_prefix,
    order_count AS PF,
    total_payment / order_count AS AOV,
    CASE
        WHEN (last_order_day - first_order_day) < 7 THEN
            1
        ELSE
            (last_order_day - first_order_day) / 7
        END AS ACL
FROM CustomerData
"""
# Calculate average CLV per zip code prefix and load into DataFrame
avg_clv_per_zip_prefix = f"""
WITH CLV AS (
    {clv}
)
SELECT
    zip_code_prefix AS zip_prefix,
    AVG(PF * AOV * ACL) AS avg_CLV,
    COUNT(customer_unique_id) AS customer_count,
    geolocation_lat AS latitude,
    geolocation_lng AS longitude
FROM CLV
    JOIN geolocation ON CLV.zip_code_prefix = geolocation.geolocation_zip_code_prefix
GROUP BY zip_code_prefix
"""
# END OF SQL QUERIES



# DATA FRAME INITIALIZATION (THIS IS COMPUTING THE FRAMEWORK)
#1
orders_per_day_df = pd.read_sql_query(orders_per_day, conn)
#2
count_orders_per_hour_df = pd.read_sql_query(orders_per_day_of_the_week_and_hour, conn)
count_orders_per_hour_df = count_orders_per_hour_df.set_index('day_of_week_name')
#3
order_product_and_shipping_costs_df = pd.read_sql_query(order_product_and_shipping_costs, conn)
#4
category_sales_summary_df = pd.read_sql_query(category_sales_summary, conn)
#5
ordered_categories_df = pd.read_sql_query(ordered_categories, conn)
#6
categories_by_median_df = pd.read_sql_query(categories_by_median, conn)
#7
monthly_sales_selected_categories_df = pd.read_sql_query(monthly_sales_selected_categories, conn)
monthly_sales_selected_categories_df = monthly_sales_selected_categories_df.set_index('year_month')
# format datetime to be pandas friendly
monthly_sales_selected_categories_df.index = pd.to_datetime(monthly_sales_selected_categories_df.index)
#8
lm_per_category_df = pd.read_sql_query(lm_per_category, conn)
#9
forecast_2018_12_df = pd.read_sql_query(forecasted_sales_dec_2018, conn)
#10
order_stage_times_top_10_citites_df = pd.read_sql_query(order_stage_times_top_10_citites, conn)
order_stage_times_top_10_citites_df = order_stage_times_top_10_citites_df.set_index('city')
#11
daily_avg_shipping_time_df = pd.read_sql_query(daily_avg_shipping_time, conn)
#12
review_score_count_df = pd.read_sql_query(review_score_count, conn)
#13
seller_review_scores_and_sales_df = pd.read_sql_query(seller_review_scores_and_sales, conn)
#14
seller_shipping_times_df = pd.read_sql_query(seller_shipping_times, conn)
#15
lead_conversion_df = pd.read_sql_query(lead_conversion, conn)

### Plotly Line Plot
fig1 = px.line(orders_per_day_df, x='day', y='order_count', title='Number of orders per day')
fig1.update_xaxes(
    tickangle=90,
    tickformat="%Y-%m-%d"
)

fig1.update_layout(
    title="Number of orders per day",
    xaxis_title="Day",
    yaxis_title="Number of orders",
    plot_bgcolor='rgba(0,0,0,0)',  # Set background to transparent
    paper_bgcolor='rgba(0,0,0,0)'   # Set background to transparent
)
i

### Plotly heatmap
fig2 = go.Figure(data=go.Heatmap(
                   z=count_orders_per_hour_df.values,
                   x=count_orders_per_hour_df.columns,
                   y=count_orders_per_hour_df.index,
                   colorscale='YlGnBu'
                   ))

fig2.update_layout(
    title="Number of orders by day of the week and hour of the day",
    xaxis_title="Hour of the day",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',  # Set background to transparent
    paper_bgcolor='rgba(0,0,0,0)'   # Set background to transparent
)


# Add text annotations
for y in range(len(count_orders_per_hour_df.index)):
    for x in range(len(count_orders_per_hour_df.columns)):
        fig2.add_annotation(
            x=count_orders_per_hour_df.columns[x],
            y=count_orders_per_hour_df.index[y],
            text=str(int(count_orders_per_hour_df.iloc[y, x])),
            showarrow=False,
            font=dict(
                color='white' if count_orders_per_hour_df.iloc[y, x] > mean_orders else 'black',
                size=10
            )
        )

## Plotly Barplot
from plotly.subplots import make_subplots

fig3 = make_subplots(rows=1, cols=2, subplot_titles=("Product cost for orders < R$500", "Shipping cost for orders < R$80"))

# Left histogram (Product cost)
fig3.add_trace(
    go.Histogram(
        x=order_product_and_shipping_costs_df['product_cost'],
        nbinsx=1000,
        name='Product Cost',
        marker_color='#6c87a3'
    ),
    row=1, col=1
)
fig3.update_xaxes(range=[0, 500], title_text="Product cost (Brazilian reals)", row=1, col=1)
fig3.update_yaxes(title_text="Frequency", row=1, col=1)

# Right histogram (Shipping cost)
fig3.add_trace(
    go.Histogram(
        x=order_product_and_shipping_costs_df['shipping_cost'],
        nbinsx=800,
        name='Shipping Cost',
        marker_color='#ad865f'
    ),
    row=1, col=2
)
fig3.update_xaxes(range=[0, 80], title_text="Product cost (Brazilian reals)", row=1, col=2)
fig3.update_yaxes(title_text="Frequency", row=1, col=2)


fig3.update_layout(
    barmode='overlay',
    height=500,
    width=1500,
    showlegend=False  # Hide legend if not needed
)


## Tree map
# Save copy of orignal to another dataframe
category_sales_summary_ORIGINAL_NAMES_df = category_sales_summary_df.copy()
# Scale the 'sales' column to the range 0.000 to 1.000
sales_min = category_sales_summary_df['sales'].min()
sales_max = category_sales_summary_df['sales'].max()
category_sales_summary_df['scaled_sales'] = (
    (category_sales_summary_df['sales'] - sales_min) / (sales_max - sales_min)
).round(3)
# Gemeral formatting
category_sales_summary_df['sales'] = pd.to_numeric(category_sales_summary_df['sales'])
category_sales_summary_df['sales'] = category_sales_summary_df['sales'].apply(lambda x: int(x))
fig4 = px.treemap(category_sales_summary_df, path=['category'], values='sales',
                 color='scaled_sales',
                 color_continuous_scale='viridis')
fig4.update_layout(
    title="Sales by category",
    plot_bgcolor='rgba(0,0,0,0)',  # Set background to transparent
    paper_bgcolor='rgba(0,0,0,0)',   # Set background to transparent
)

# Box plot
def remove_outliers_by_category(df, column, n_std=3):
  new_df = df.copy()
  for category in df['category'].unique():
    category_data = df[df['category'] == category]
    mean = category_data[column].mean()
    std = category_data[column].std()
    lower_bound = mean - n_std * std
    upper_bound = mean + n_std * std
    new_df = new_df[~((new_df['category'] == category) & ((new_df[column] < lower_bound) | (new_df[column] > upper_bound)))]
  return new_df

ordered_categories_df = remove_outliers_by_category(ordered_categories_df, 'weight')

fig5 = px.box(ordered_categories_df, x="weight", y="category",
             title="Product weight by category (top 18 categories by sales)",
             category_orders={"category": categories_by_median_df['category'].tolist()},
             color="category")
fig5.update_traces(boxpoints=False)

fig5.update_layout(
    yaxis=dict(
        tickfont=dict(size=9)  # Set the font size to 16
    ),
    xaxis=dict(
        range=[0, 26000],  # Set the x-axis range from 0 to 26,000
        dtick=1000,  # Set the tick interval to 2,500
    ),
    showlegend=False,
    #paper_bgcolor='rgba(255,255,255,1)',  # Set plotly background to transparent
    plot_bgcolor='rgba(51,51,51,1)'   # Set plot to dark grey
)

fig5.update_yaxes(title_text="Category")
# Update x-axis labels
fig5.update_xaxes(title_text="Product weigth (Grams)")


# Line graph
monthly_sales_selected_categories_df = pd.read_sql_query(monthly_sales_selected_categories, conn)
monthly_sales_selected_categories_df = monthly_sales_selected_categories_df.set_index('year_month')
#Make the date-time pandas compatible
monthly_sales_selected_categories_df.index = pd.to_datetime(monthly_sales_selected_categories_df.index)
fig6 = go.Figure()

for column in monthly_sales_selected_categories_df.columns:
  fig6.add_trace(go.Scatter(
      x=monthly_sales_selected_categories_df.index,
      y=monthly_sales_selected_categories_df[column],
      mode='lines+markers',
      name=column,
      line=dict(dash='dot')
  ))


fig6.update_layout(
    title="Monthly Sales for Selected Categories",
    xaxis_title="Year-Month",
    yaxis_title="Total Sales",
    xaxis=dict(
        tickmode='array',
        tickvals=monthly_sales_selected_categories_df.index,
        ticktext=[date.strftime('%Y-%m') for date in monthly_sales_selected_categories_df.index]
    ),
    hovermode='x unified'
)

# limits for x-axis
days = np.arange(0, 604)

fig7 = go.Figure()

for category in selected_categories:
    lm = lm_per_category_df[lm_per_category_df['category'] == category]
    slope = lm['slope'].values[0]
    intercept = lm['intercept'].values[0]
    days = np.arange(0, 604)
    line = intercept + slope * days

    fig7.add_trace(go.Scatter(
        x=days,
        y=line,
        mode='lines',
        name=f'{category} (slope={slope:.2f})'
    ))

fig7.update_layout(
    title="Regression lines for the selected categories",
    xaxis_title="Days from 2017-01-01",
    yaxis_title="Daily sales (Brazilian reals)",
    hovermode='x unified'
)

# Sales forecast
for category in selected_categories:
    category_forecast = forecast_2018_12_df[forecast_2018_12_df['category'] == category]
fig8 = go.Figure()

for category in selected_categories:
    category_forecast = forecast_2018_12_df[forecast_2018_12_df['category'] == category]
    fig8.add_trace(go.Scatter(
        x=category_forecast['december_2018_day'],
        y=category_forecast['moving_avg_sales'],
        mode='lines',
        name=category,
        line=dict(dash='dot')
    ))

fig8.update_layout(
    title="Sales Forecast for December 2018",
    xaxis_title="Days of December 2018",
    yaxis_title="Forecasted Sales (Brazilian Reals)",
    xaxis=dict(
        tickmode='linear',  # Set tick mode to linear
        tick0=1,           # Starting tick value
        dtick=1           # Tick interval
    ),
    hovermode='x unified'

)

#Cities Bar Graph
# Get the index of each city
order_stage_times_top_10_citites_df = order_stage_times_top_10_citites_df.set_index('city')
fig9 = px.bar(order_stage_times_top_10_citites_df.reset_index(),
            x=['approved', 'delivered_to_carrier', 'delivered_to_customer', 'estimated_delivery'],
            y='city',
            orientation='h',
            title='Average days for each order stage (top 10 cities by sales)',
            labels={'value': 'Average Days', 'city': 'City'},
            range_x=[0, 31]
           )

fig9.update_layout(
   barmode='stack',  # Use stacked bars
   xaxis_title='Average Days',  # X-axis title
   yaxis_title='City',  # Y-axis title
)


# Line Graph for Shipping time
from statsmodels.nonparametric.smoothers_lowess import lowess

fig10 = go.Figure()

fig10.add_trace(go.Scatter(
    x=pd.to_datetime(daily_avg_shipping_time_df['purchase_date']),
    y=daily_avg_shipping_time_df['avg_delivery_time'],
    mode='lines',
    name='Daily Average'
))

fig10.add_trace(go.Scatter(
    x=pd.to_datetime(daily_avg_shipping_time_df['purchase_date']),
    y=[daily_avg_shipping_time_df['avg_delivery_time'].mean()] * len(daily_avg_shipping_time_df),
    mode='lines',
    name='Yearly Average',
    line=dict(color='red', dash='dash')
))

# Calculate LOWESS trend line
x_numeric = pd.to_numeric(pd.to_datetime(daily_avg_shipping_time_df['purchase_date']))
y = daily_avg_shipping_time_df['avg_delivery_time']
trend_line = lowess(y, x_numeric, frac=0.3)  # Adjust frac for smoothing

fig10.add_trace(go.Scatter(
    x=pd.to_datetime(daily_avg_shipping_time_df['purchase_date']),
    y=trend_line[:, 1],
    mode='lines',
    name='LOWESS Trend Line'
))


fig10.update_layout(
    title="Average Delivery Time",
    xaxis_title="Year-Month",
    yaxis_title="Days",
)

# Distirbution plot for review scores
fig11 = px.bar(review_score_count_df, x='review_score', y='count',
             color='review_score',
             color_continuous_scale=['red', 'green'],
             title='Distribution of Review Scores')

### RFM Buckets TODO
RFM_Bucket_df = pd.read_sql_query(rfm_buckets, conn)

fig12 = px.scatter(RFM_Bucket_df,
                 x='avg_days_since_purchase',
                 y='avg_sales_per_customer',
                 size='customer_count',
                 size_max=60,
                 color=RFM_Bucket_df['RFM_Bucket'],
                 hover_name='RFM_Bucket',
                 title='RFM Segmentation of Customers',
                 text='RFM_Bucket'
)

fig12.update_layout(
    xaxis_title='Average Days Since Last Purchase',
    yaxis_title='Average Sales Per Customer'
)

####

# Folium Map
df = pd.read_sql_query(avg_clv_per_zip_prefix, conn)

# Create a map using Folium
map = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

# Add circle markers for each zip code prefix
for i, zip_prefix in df.iterrows():
    folium.CircleMarker(
        location=[zip_prefix['latitude'], zip_prefix['longitude']],
        radius=0.1 * np.sqrt(zip_prefix['customer_count']),
        color=None,
        fill_color='#85001d',
        fill_opacity=0.1 + 0.1 * np.sqrt(zip_prefix['avg_CLV'] / df['avg_CLV'].max()),
        popup=(
            f"<b>Zip Code Prefix:</b> {int(zip_prefix['zip_prefix'])}<br>"
            f"<b>Average CLV:</b> {int(zip_prefix['avg_CLV'])}<br>"
            f"<b>Customers:</b> {int(zip_prefix['customer_count'])}"
        )
    ).add_to(map)


# Review Score clusterubg
seller_review_scores_and_sales_df = pd.read_sql_query(seller_review_scores_and_sales, conn)
fig14 = px.scatter(seller_review_scores_and_sales_df, x='total_sales', y='avg_review_score',
                 size='num_orders', color='num_orders',
                 log_x=True,
                 opacity=0.7,
                 trendline="lowess",
                 trendline_options=dict(frac=0.1)
                 #, color_continuous_scale="matter"
                 )
fig14.update_traces(marker=dict(
                  sizeref=1),
                  )
fig14.update_layout(
    xaxis_title='Total sales',
    yaxis_title='Average review score'
)

seller_buckets = pd.read_sql_query(sellers_per_bucket, conn)
fig15 = px.bar(seller_buckets, x='bucket', y='seller_count',
             title='Number of sellers by orders (grouped)', color='bucket')
fig15.update_layout(
    xaxis_title='Amount of orders per seller',
    yaxis_title='Number of sellers'
)

# Whisker Plot
seller_shipping_times_df = pd.read_sql_query(seller_shipping_times, conn)

def remove_outliers_iqr(df, column, group_column):
  new_df = pd.DataFrame()
  for group_value in df[group_column].unique():
    group_df = df[df[group_column] == group_value]
    Q1 = group_df[column].quantile(0.25)
    Q3 = group_df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_group_df = group_df[(group_df[column] >= lower_bound) & (group_df[column] <= upper_bound)]
    new_df = pd.concat([new_df, filtered_group_df])
  return new_df

seller_shipping_times_df = remove_outliers_iqr(seller_shipping_times_df, 'delivery_time', 'bucket')

def remove_outliers_iqr(df, column, group_column):
  new_df = pd.DataFrame()
  for group_value in df[group_column].unique():
    group_df = df[df[group_column] == group_value]
    Q1 = group_df[column].quantile(0.25)
    Q3 = group_df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_group_df = group_df[(group_df[column] >= lower_bound) & (group_df[column] <= upper_bound)]
    new_df = pd.concat([new_df, filtered_group_df])
  return new_df

seller_shipping_times_df = remove_outliers_iqr(seller_shipping_times_df, 'delivery_time', 'bucket')

fig16 = px.box(seller_shipping_times_df, x='bucket', y='delivery_time',
             color='bucket', points='outliers',
             category_orders={'bucket': seller_buckets['bucket']})
fig16.update_traces(boxpoints=False)  # Disable fliers

fig16.update_layout(
    title="Delivery Time by Seller Order Volume",
    xaxis_title="Sellers with...",
    yaxis_title="Shipping time (days)",
)
fig16.show()
