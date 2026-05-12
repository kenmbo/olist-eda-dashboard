import { useQuery } from '@tanstack/react-query';
import type { CategorySalesResponse } from '../../types/api';

const fetchCategorySales = async (): Promise<CategorySalesResponse> => {
  const response = await fetch(`https://localhbost:8000/api/categories/sales`);
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
