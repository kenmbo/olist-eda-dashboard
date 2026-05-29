import { useQuery } from '@tanstack/react-query';
import type { HourlyOrdersResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:80';

const fetchHourlyOrders = async (): Promise<HourlyOrdersResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/orders/hourly`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useHourlyOrders = () => {
  return useQuery({
    queryKey: ['hourlyOrders'],
    queryFn: fetchHourlyOrders,
    staleTime: 1000 * 60 * 5,
  });
};
