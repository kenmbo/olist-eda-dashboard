import { useQuery } from '@tanstack/react-query';
import type { DeliveryStagesResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchDeliveryStages = async (): Promise<DeliveryStagesResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/delivery/stages`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useDeliveryStages = () => {
  return useQuery({
    queryKey: ['deliveryStages'],
    queryFn: fetchDeliveryStages,
    staleTime: 1000 * 60 * 5,
  });
};
