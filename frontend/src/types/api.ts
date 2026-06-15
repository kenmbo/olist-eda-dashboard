export interface DailyOrdersResponse {
  day: string[];
  order_count: number[];
}

export interface HourlyOrdersResponse {
  index: string[];    // The days of the week
  columns: string[];  // The hours of the day (0-23)
  data: number[][];   // The 2D array of order counts
}

export interface CategorySalesResponse {
  category: string[];
  sales: number[];
}

export interface SellerShippingResponse {
  bucket: string[];
  seller_id: string[];
  delivery_time: number[];
}

export interface OrderCostsResponse {
  order_id: string[];
  product_cost: number[];
  shipping_cost: number[];
}

export interface CustomerMapResponse {
  zip_prefix: number[];
  avg_CLV: number[];
  customer_count: number[];
  latitude: number[];
  longitude: number[];
}

export interface CategoryMonthlySalesResponse {
  index: string[];    // The months (e.g., '2017-01', '2017-02')
  columns: string[];  // The category names
  data: number[][];   // 2D array: rows are months, columns are sales for that category
}

export type CategoryWeightResponse = Record<string, number[]>;
