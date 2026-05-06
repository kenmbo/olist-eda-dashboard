import { useDailyOrders } from './useOrders';
const OrdersContainer = () => {
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
