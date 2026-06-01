import type { OrderCostsResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchOrderCosts = async (): Promise<OrderCostsResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/orders/costs`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useOrderCosts = () => {
     return fetchOrderCosts;
};
