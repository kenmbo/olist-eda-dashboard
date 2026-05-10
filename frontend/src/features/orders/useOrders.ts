import { useQuery } from '@tanstack/react-query';
import { DailyOrdersResponse } from '../../types/api';

const fetchDailyOrders = async (): Promise<DailyOrdersResponse> => {
  const response = await fetch('http://localhost:8000/api/orders/daily');
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useDailyOrders = () => {
  return useQuery({
    queryKey: ['dailyOrders'], // A unique key for caching
    queryFn: fetchDailyOrders,
    staleTime: 1000 * 60 * 5,  // Data stays fresh for 5 minutes (no refetching if user changes tabs)
  });
};
