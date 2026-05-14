export interface DailyOrdersResponse {
  day: string[];
  order_count: number[];
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
