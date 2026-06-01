import { useQuery } from '@tanstack/react-query';
import type { CustomerMapResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchCustomerMap = async (): Promise<CustomerMapResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/customers/clv-map`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useCustomerMap = () => {
  return useQuery({
    queryKey: ['customerMap'],
    queryFn: fetchCustomerMap,
    staleTime: 1000 * 60 * 5,
  });
};
