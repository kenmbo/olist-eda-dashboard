import { useHourlyOrders } from './useHourlyOrders';
import OrdersHeatmap from './OrdersHeatmap';

export default function OrdersHeatmapContainer() {
  const { data, isLoading, isError } = useHourlyOrders();

  if (isLoading) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-gray-800 rounded-lg border border-gray-700">
        <span className="text-gray-400 animate-pulse">Loading heatmap...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-red-900/20 rounded-lg border border-red-800">
        <span className="text-red-400">Failed to load hourly data.</span>
      </div>
    );
  }

  return <OrdersHeatmap data={data} />;
}
