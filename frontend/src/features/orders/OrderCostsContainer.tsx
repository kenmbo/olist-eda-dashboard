import { useOrderCosts } from './useOrderCosts';
import OrderCostsHistograms from './OrderCostsHistograms';

export default function OrderCostsContainer() {
  const { data, isLoading, isError } = useOrderCosts();

  if (isLoading) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-gray-800 rounded-lg border border-gray-700">
        <span className="text-gray-400 animate-pulse">Loading cost distributions...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-red-900/20 rounded-lg border border-red-800">
        <span className="text-red-400">Failed to load order costs.</span>
      </div>
    );
  }

  return <OrderCostsHistograms data={data} />;
}
