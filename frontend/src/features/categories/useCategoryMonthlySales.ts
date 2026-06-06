import { useQuery } from '@tanstack/react-query';
import type { CategoryMonthlySalesResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchCategoryMonthlySales = async (): Promise<CategoryMonthlySalesResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/categories/monthly-sales`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useCategoryMonthlySales = () => {
  return useQuery({
    queryKey: ['categoryMonthlySales'],
    queryFn: fetchCategoryMonthlySales,
    staleTime: 1000 * 60 * 5,
  });
};
