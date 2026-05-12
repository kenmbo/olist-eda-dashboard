import { useQuery } from '@tanstack/react-query';
import type { CategorySalesResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchCategorySales = async (): Promise<CategorySalesResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/categories/sales`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useCategorySales = () => {
  return useQuery({
    queryKey: ['categorySales'],
    queryFn: fetchCategorySales,
    staleTime: 1000 * 60 * 5,
  });
};
