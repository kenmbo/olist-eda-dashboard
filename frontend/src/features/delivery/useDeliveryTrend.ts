import { useQuery } from '@tanstack/react-query';
import type { DeliveryTrendResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchDeliveryTrend = async (): Promise<DeliveryTrendResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/delivery/trend`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useDeliveryTrend = () => {
  return useQuery({
    queryKey: ['deliveryTrend'],
    queryFn: fetchDeliveryTrend,
    staleTime: 1000 * 60 * 5,
  });
};
