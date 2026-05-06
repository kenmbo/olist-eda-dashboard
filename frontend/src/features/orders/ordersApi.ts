// src/features/orders/ordersApi.ts
import { DailyOrdersResponse } from '../../types/api';

export const fetchDailyOrders = async (): Promise<DailyOrdersResponse> => {
  const response = await fetch(`'http://localhost:8000/api/orders/daily`);
  
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  
  return response.json();
};
