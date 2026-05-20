import { useSellerShipping } from './useSellerShipping';
import SellerShippingBoxPlot from './SellerShippingBoxPlot';

export default function SellerShippingContainer() {
  const { data, isLoading, isError } = useSellerShipping();

if (isLoading) {
    return <div className="spinner">Loading order data...</div>;
  }

if (isError) {
    return <div className="error">Failed to load the chart. Please try again.</div>;
  }

  // If we reach here, we are guaranteed to have the data
  return (
    <div className="chart-wrapper">
            <SellerShippingBoxPlot data={data!} /> 
    </div>
  );
};
