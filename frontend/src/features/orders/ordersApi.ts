// src/features/orders/ordersApi.ts
import { DailyOrdersResponse } from '../../types/api';

// Use the URL in .env OR use default localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const fetchDailyOrders = async (): Promise<DailyOrdersResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/orders/daily`);

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  
  return response.json();
};
