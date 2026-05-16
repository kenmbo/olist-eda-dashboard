import { useQuery } from '@tanstack/react-query';
import type { SellerShippingResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchSellerShipping = async (): Promise<SellerShippingResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/sellers/shipping-times`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useSellerShipping = () => {
  return useQuery({
    queryKey: ['sellerShipping'],
    queryFn: fetchSellerShipping,
    staleTime: 1000 * 60 * 5,
  });
};
