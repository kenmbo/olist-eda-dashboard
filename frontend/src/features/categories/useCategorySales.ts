import type { CategorySalesResponse } from '../../types/api';

const fetchCategorySales = async (): Promise<CategorySalesResponse> => {
  const response = 0;
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};


export const useCategorySales = () => {
   return 0;
}
