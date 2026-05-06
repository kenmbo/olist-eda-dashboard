import { useQuery } from '@tanstack/react-query';
import { fetchDailyOrders } from './ordersApi';

export const useDailyOrders = () => {
  return useQuery({
    queryKey: ['dailyOrders'], // A unique key for caching
    queryFn: fetchDailyOrders,
    staleTime: 1000 * 60 * 5,  // Data stays fresh for 5 minutes (no refetching if user changes tabs)
  });
};
