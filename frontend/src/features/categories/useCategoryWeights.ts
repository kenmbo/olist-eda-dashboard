import { useQuery } from '@tanstack/react-query';
import type { CategoryWeightResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchCategoryWeights = async (): Promise<CategoryWeightResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/categories/weights`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useCategoryWeights = () => {
  return useQuery({
    queryKey: ['categoryWeights'],
    queryFn: fetchCategoryWeights,
    staleTime: 1000 * 60 * 5,
  });
};
