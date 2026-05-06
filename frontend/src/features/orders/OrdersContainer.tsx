import { useDailyOrders } from './useOrders';
import OrdersLineChart from './OrdersLineChart';

const OrdersContainer = () => {
onst OrdersContainer = () => {
  // TanStack Query handles all the heavy lifting
  const { data, isLoading, isError } = useDailyOrders();

  if (isLoading) {
    return <div className="spinner">Loading order data...</div>;
  }

  if (isError) {
    return <div className="error">Failed to load the chart. Please try again.</div>;
  }

  // If we reach here, we are guaranteed to have the data
  return (
    <div className="chart-wrapper">
      <h2>Daily Sales Volume</h2>
      {
	// Expecting JSON data from Fetcher
      }
      <OrdersLineChart data={data!} /> 
    </div>
  );
};

export default OrdersContainer;
