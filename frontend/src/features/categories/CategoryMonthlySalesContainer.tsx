import { useCategoryMonthlySales } from './useCategoryMonthlySales';
import CategoryMonthlySalesChart from './CategoryMonthlySalesChart';

export default function CategoryMonthlySalesContainer() {
  const { data, isLoading, isError } = useCategoryMonthlySales();

  if (isLoading) {
    return (
      <div className="w-full h-80 flex items-center justify-center bg-gray-900 rounded-lg border border-gray-800">
        <span className="text-gray-400 animate-pulse">Loading monthly sales data...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-80 flex items-center justify-center bg-red-900/20 rounded-lg border border-red-800">
        <span className="text-red-400">Failed to load sales timeline.</span>
      </div>
    );
  }

  return <CategoryMonthlySalesChart data={data} />;
}
