# Backend Architecture

This document describes the current Python/FastAPI backend so future migration agents can map it into another backend framework, such as Java + Spring Boot, without losing endpoint behavior or hidden data-shaping assumptions.

The `frontend/` folder is intentionally out of scope here.

## High-Level View

The backend is an analytics API for an Olist e-commerce dashboard. It serves JSON data for Plotly charts. Most endpoints follow the same pattern:

1. Receive a request in `src/main.py`.
2. Open a SQLite connection through `src/database.py`.
3. Run a SQL query defined in `src/queries.py`.
4. Load the SQL result into a pandas DataFrame.
5. Optionally reshape, clean, filter, smooth, pivot, or label the data.
6. Return JSON in a chart-friendly shape.

The backend is SQL-first and reporting-oriented. It is not a CRUD application and does not model database tables as domain entities. For a Spring Boot migration, `JdbcTemplate` or `NamedParameterJdbcTemplate` maps more naturally than JPA/Hibernate.

## Runtime

The FastAPI application lives in `src/main.py`.

Run command documented in the source:

```bash
uvicorn src.main:app --reload
```

The app loads environment variables with `python-dotenv`. CORS origins come from `CORS_ORIGINS`, parsed as a comma-separated list. If `CORS_ORIGINS` is unset or empty, `allow_origins` becomes an empty list, so browser calls from a separate frontend origin may be blocked.

The database connection default is:

```python
sqlite3.connect("data/olist.sqlite")
```

That path is relative to the current working directory. Running Uvicorn from the repository root works with the current root-level `data/olist.sqlite`; running from another directory may fail or open the wrong path.

## File Responsibilities

### `src/main.py`

`main.py` owns the HTTP layer:

- Creates the `FastAPI` app.
- Configures CORS.
- Defines all API routes under `/api/...`.
- Opens and closes SQLite connections per request.
- Calls `database.py` helper functions for many endpoints.
- Calls `pd.read_sql_query(...)` directly for several newer endpoints.
- Performs response-specific DataFrame operations.
- Returns JSON-compatible Python dict/list structures, or a raw `Response` for one pandas JSON string.

There is no Pydantic response model layer. Response shape is implicit in each endpoint function.

### `src/database.py`

`database.py` is a thin data-access wrapper:

- `get_connection(db_path="data/olist.sqlite")` opens a SQLite connection.
- Most other functions call `pd.read_sql_query(query_constant, conn)`.
- A few functions set a DataFrame index before returning it.

Connection errors print to stdout and call `sys.exit(1)`. In a web server context, this can terminate the process instead of returning an HTTP error.

### `src/queries.py`

`queries.py` is a catalog of SQL string constants. Some query constants are standalone SQL; others are built with Python f-strings from reusable CTE fragments and tuple constants.

Important patterns:

- Query constants encode chart logic, not just raw data access.
- Several queries use SQLite date functions such as `DATE`, `STRFTIME`, and `JULIANDAY`.
- Some queries use window functions (`RANK`, `ROW_NUMBER`, moving average windows).
- Some category queries join `product_category_name_translation` and return English category names.
- Other category queries use raw `products.product_category_name`, which may return untranslated category names.

### `src/utils.py`

`utils.py` contains DataFrame helpers:

- `remove_outliers_iqr(df, column, group_column)` removes outliers per group using the 1.5 IQR rule.
- `remove_outliers_by_category(df, column, n_std=3)` removes outliers per `category` using standard deviation bounds.
- `view_table(table, limit)` appears to be notebook/debug code. It references `conn` without accepting it as a parameter and is not used by the API.

## Response Shapes

The API uses several JSON shapes, depending on chart needs:

- `df.to_dict(orient="list")`: object keyed by column name; each value is an array.
- `df.to_dict(orient="split")`: object with `index`, `columns`, and `data`; useful for heatmaps or matrix-like data.
- `df.to_dict(orient="records")`: array of row objects.
- Custom dicts: arrays renamed specifically for frontend traces.
- `Response(content=df.to_json(...), media_type="application/json")`: used when pandas serializes directly.

Spring migration agents should preserve each endpoint's existing shape unless the frontend contract is intentionally updated.

## Endpoint Inventory

### Orders

`GET /api/orders/daily`

- Source: `database.get_orders_per_day` -> `queries.orders_per_day`
- SQL: groups `orders` by `DATE(order_purchase_timestamp)`.
- Response: `orient="list"` with `day` and `order_count`.

`GET /api/orders/hourly`

- Source: `database.get_orders_per_hour` -> `queries.orders_per_day_of_the_week_and_hour`
- SQL: extracts day-of-week and hour, then counts orders into 24 hour columns.
- DataFrame transform: sets `day_of_week_name` as index.
- Response: `orient="split"` with weekday index, hour columns, and count matrix.
- Edge case: `STRFTIME('%w')` returns Sunday as `0`, but the query comments say Sunday is `7`. The actual ordering uses `0` for Sunday and `1` through `6` for Monday through Saturday.

`GET /api/orders/costs`

- Source: `database.get_order_product_and_shipping_costs` -> `queries.order_product_and_shipping_costs`
- SQL: delivered orders only; sums item `price` and `freight_value` per order.
- Response: `orient="list"` with `order_id`, `product_cost`, and `shipping_cost`.

### Categories And Sales

`GET /api/categories/sales`

- Source: `database.get_category_sales_summary` -> `queries.category_sales_summary`
- SQL: ranks delivered-order categories by total sales, returns top 18 plus one aggregated `Other categories` row.
- Response: `orient="list"` with `category` and `sales`.

`GET /api/categories/weights`

- Source: direct `pd.read_sql_query(queries.product_weights, conn)`
- SQL: reads raw product category names and product weights from `order_items` joined to `products`.
- First definition in `main.py`: selects the top 5 categories by row count and applies `utils.remove_outliers_by_category(cat_df, "weight", 0.8)` before returning.
- Second definition in `main.py`: same route path and function name, but returns unfiltered weights for the top 5 categories.
- Response: object keyed by category, each value an array of weights.
- Edge case: the route is duplicated. FastAPI/Starlette registers both route handlers; runtime matching and OpenAPI output can become confusing. Treat this as a migration decision point and verify observed behavior before changing the frontend contract.
- Edge case: this endpoint uses raw category names, unlike several sales endpoints that use English translations.

`GET /api/categories/monthly-sales`

- Source: direct `pd.read_sql_query(queries.monthly_category_sales, conn)`
- SQL: delivered orders grouped by month and raw product category name.
- DataFrame transform: computes top 5 categories by total sales, filters to those categories, pivots months into rows and categories into columns, fills missing cells with `0`.
- Response: raw pandas JSON using `orient="split"` and `application/json`.
- Migration note: Java should reproduce `{ "columns": [...], "index": [...], "data": [...] }`.

`GET /api/sales/monthly`

- Source: `database.get_monthly_sales_selected_categories` -> `queries.monthly_sales_selected_categories`
- SQL: monthly sums for fixed selected English categories: `health_beauty`, `auto`, `toys`, `electronics`, `fashion_shoes`.
- DataFrame transform in `database.py`: sets `year_month` as index and converts it with `pd.to_datetime`.
- Endpoint transform: resets the index before serializing.
- Response: `orient="list"`.
- Edge case: because `year_month` is converted to pandas datetimes, FastAPI encoding may emit datetime-like values rather than the original `YYYY-MM` strings.

`GET /api/sales/regression`

- Source: `database.get_lm_per_category` -> `queries.lm_per_category`
- SQL: computes linear regression slope and intercept inside SQLite for selected categories using daily sales from 2017-01-01 through 2018-08-29.
- Response: `orient="records"` with one object per category.

`GET /api/sales/forecast`

- Source: `database.get_forecasted_sales_dec_2018` -> `queries.forecasted_sales_dec_2018`
- SQL: uses the regression query to project December 2018 category sales and calculates a 5-day moving average with a window function.
- Response: `orient="list"` with `december_2018_day`, `category`, and `moving_avg_sales`.

### Sellers

`GET /api/sellers/performance`

- Source: `database.get_seller_review_scores_and_sales` -> `queries.seller_review_scores_and_sales`
- SQL: seller-level average review score, total sales, and order count; sellers must have more than 10 orders.
- Response: `orient="list"`.

`GET /api/sellers/distribution`

- Source: `database.get_sellers_per_bucket` -> `queries.sellers_per_bucket`
- SQL: buckets sellers by order volume: `1-9 orders`, `10-99 orders`, `100-999 orders`, `1000+ orders`.
- Response: `orient="list"` with bucket and seller count.

`GET /api/sellers/shipping-times`

- Source: `database.get_seller_shipping_times` -> `queries.seller_shipping_times`
- SQL: delivered-order delivery time in days per seller and seller bucket.
- DataFrame transform: `utils.remove_outliers_iqr(df, column="delivery_time", group_column="bucket")`.
- Response: `orient="list"`.
- Migration note: reproduce IQR filtering per bucket, not globally.

`GET /api/sellers/review-sales`

- Source: direct `pd.read_sql_query(queries.seller_review_vs_sales, conn)`
- SQL: seller total sales, average review score, and distinct order count; sellers must have more than 5 orders.
- DataFrame transform: rounds average score and total sales to 2 decimals.
- Response: custom arrays: `seller_ids`, `total_sales`, `avg_scores`, `order_counts`.

### Leads

`GET /api/leads/conversion`

- Source: direct `pd.read_sql_query(queries.lead_conversion, conn)`
- SQL: groups qualified and closed leads by origin, with missing origin as `unknown`; computes percentage conversion.
- DataFrame transform: replaces underscores with spaces and title-cases origin labels.
- Response: custom arrays: `origins`, `qualified_leads`, `closed_leads`, `conversion_rate`.

`GET /api/leads/origin`

- Source: direct `pd.read_sql_query(queries.leads_by_origin, conn)`
- SQL: counts marketing qualified leads by origin, excluding null, empty, and `other`; sorted ascending by count for Plotly bar orientation.
- DataFrame transform: replaces underscores with spaces and title-cases origin labels.
- Response: custom arrays: `origins`, `leads`.

### Shipping And Delivery

`GET /api/shipping/stages-by-city`

- Source: `database.get_order_stage_times_top_cities` -> `queries.order_stage_times_top_10_citites`
- SQL: fixed top city list; calculates average days between purchase, approval, carrier handoff, customer delivery, and estimated delivery.
- DataFrame transform: sets `city` as index in `database.py`, then endpoint resets index.
- Response: `orient="list"`.
- Edge case: query constant name contains typo `citites`; preserve or intentionally rename during migration.

`GET /api/shipping/daily-average`

- Source: `database.get_daily_avg_shipping_time`
- Expected query: `queries.daily_avg_shipping_time`
- Current edge case: `queries.daily_avg_shipping_time` is not defined in the current `queries.py`. This endpoint likely raises `AttributeError` if called.

`GET /api/delivery/trend`

- Source: direct `pd.read_sql_query(queries.daily_delivery_time, conn)`
- SQL: delivered orders grouped by purchase date; average delivery days from purchase to customer delivery.
- DataFrame transform: drops nulls, calculates LOWESS smoothing with `statsmodels.lowess`, using `np.arange(len(df))` as numeric x-values and `frac=0.1`.
- Response: custom arrays: `dates`, `actual_days`, `trend_days`.
- Migration note: LOWESS is the least direct Java port. Either use a Java statistics library that supports LOWESS/LOESS or intentionally choose and document a substitute smoothing method.

`GET /api/delivery/stages`

- Source: direct `pd.read_sql_query(queries.city_delivery_stages, conn)`
- SQL: dynamically finds top 10 cities by delivered order volume, then calculates approval, carrier, and transit days.
- DataFrame transform: title-cases city names.
- Response: custom arrays: `cities`, `approval_days`, `carrier_days`, `transit_days`.

### Reviews

`GET /api/reviews/distribution`

- Source: direct `pd.read_sql_query(queries.review_score_distribution, conn)`
- SQL: counts reviews by score.
- DataFrame transform: creates display labels from numeric scores.
- Response: custom arrays: `scores`, `counts`.
- Migration note: preserve the exact score label format expected by the frontend.

### Customers

`GET /api/customers/rfm`

- Source: `database.get_rfm_buckets`
- Expected query: `queries.rfm_buckets`
- Current edge case: `queries.rfm_buckets` is not defined in the current `queries.py`. This endpoint likely raises `AttributeError` if called.

`GET /api/customers/clv-map`

- Source: `database.get_avg_clv_per_zip_prefix` -> `queries.avg_clv_per_zip_prefix`
- SQL: computes customer lifetime value ingredients per customer, then aggregates by zip prefix and joins to averaged geolocation coordinates.
- Response: `orient="list"` with zip prefix, average CLV, customer count, latitude, and longitude.

## Known Edge Cases And Migration Risks

The following behaviors deserve special attention before or during migration:

- Duplicate route: `/api/categories/weights` is defined twice in `main.py`.
- Missing query constants: `database.py` references `queries.daily_avg_shipping_time`, `queries.review_score_count`, and `queries.rfm_buckets`, but these names are not currently defined in `queries.py`.
- Unused or risky utility: `utils.view_table` uses a free variable `conn` and interpolates a table name directly into SQL. It appears unused by the API.
- CWD-relative database path: `data/olist.sqlite` depends on where the server process starts.
- Process exit on DB connection failure: `database.get_connection` calls `sys.exit(1)`.
- Mixed query styles: some endpoints use `database.py`; others bypass it and call `pd.read_sql_query` directly from `main.py`.
- Mixed response styles: endpoints return multiple JSON orientations and custom shapes.
- Mixed category naming: some endpoints use translated English categories; others return raw Olist product category names.
- Date/time semantics: SQLite `JULIANDAY` differences return fractional days. Preserve numeric precision unless intentionally rounding.
- Day-of-week ordering: the hourly heatmap query orders by SQLite `%w`, where Sunday is `0`.
- SQL typo in unused query: `queries.order_price_stats` references `MIN(order_order_price)`, which does not match the derived `order_price` alias.
- Typo in query name: `order_stage_times_top_10_citites` is misspelled but used by `database.py`.
- Error handling is inconsistent: several endpoints catch exceptions and return `{"error": "..."}` with HTTP 200, while many endpoints do not catch exceptions.
- Connection cleanup is manual. Most endpoints close connections, but a few rely on `finally`; one duplicate `/api/categories/weights` definition calls `conn.close()` without checking whether `conn` was assigned.

## Spring Boot Mapping Guide

A direct migration can preserve the current architecture with these roles:

- FastAPI routes -> Spring `@RestController`.
- `database.py` query wrappers -> service or repository methods.
- `queries.py` constants -> `.sql` resource files, Java text blocks, or repository constants.
- SQLite connection -> Spring `DataSource` configured with SQLite JDBC.
- pandas `orient="list"` -> `Map<String, List<?>>`.
- pandas `orient="split"` -> DTO with `index`, `columns`, and `data`.
- pandas `orient="records"` -> `List<Map<String, Object>>` or typed records.
- custom dict responses -> typed Java records where possible.
- pandas filtering/pivoting -> service-layer Java code using lists, maps, sorting, and grouping.

Recommended migration strategy:

1. Preserve all endpoint paths and JSON response shapes first.
2. Move every SQL query as-is before optimizing.
3. Add snapshot-style response tests against the current FastAPI output for representative endpoints.
4. Port simple `orient="list"` endpoints first.
5. Port matrix, pivot, outlier-filtering, and LOWESS endpoints last.
6. Decide explicitly whether to preserve or fix known bugs such as missing query constants and duplicate routes.

