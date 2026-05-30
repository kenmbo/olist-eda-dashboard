import { useHourlyOrders } from './useHourlyOrders';
import OrdersHeatmap from './OrdersHeatmap';

export default function OrdersHeatmapContainer() {
  const { data, isLoading, isError } = useHourlyOrders();

  if (isLoading) {
    return (
        <span className="text-gray-400 animate-pulse">Loading heatmap...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
        <span className="text-red-400">Failed to load hourly data.</span>
      </div>
    );
  }

  return <OrdersHeatmap data={data} />;
}
