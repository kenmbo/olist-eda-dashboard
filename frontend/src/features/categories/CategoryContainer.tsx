import { useCategorySales } from './useCategorySales';
import CategoryTreemap from './CategoryTreemap';

// TanStack Query State Management
export default function CategoryContainer() {
  const { data, isLoading, isError } = useCategorySales();

if (isLoading) {
    return <div className="spinner">Loading order data...</div>;
  }

  if (isError) {
    return <div className="error">Failed to load the chart. Please try again.</div>;
  }

   return <CategoryTreemap data={data} />;
}
