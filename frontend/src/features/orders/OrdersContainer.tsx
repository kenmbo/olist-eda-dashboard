import { useDailyOrders } from './useOrders';
import OrdersLineChart from './OrdersLineChart';

export default function OrdersContainer() {
  const { data, isLoading, isError } = useDailyOrders();

  if (isLoading) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-gray-50 rounded-lg border border-gray-200">
        <span className="text-gray-500 animate-pulse">Loading chart data...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-red-50 rounded-lg border border-red-200">
        <span className="text-red-500">Failed to load data.</span>
      </div>
    );
  }

  return <OrdersLineChart data={data!} />;

}
