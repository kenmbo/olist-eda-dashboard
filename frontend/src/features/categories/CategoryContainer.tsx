import { useCategorySales } from './useCategorySales';
import CategoryTreemap from './CategoryTreemap';

// TanStack Query State Management
export default function CategoryContainer() {
  const { data, isLoading, isError } = useCategorySales();

  if (isLoading) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-gray-50 rounded-lg border border-gray-200">
        <span className="text-gray-500 animate-pulse">Loading category data...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-red-50 rounded-lg border border-red-200">
        <span className="text-red-500">Failed to load categories.</span>
      </div>
    );
  }

  return <CategoryTreemap data={data} />;
}
