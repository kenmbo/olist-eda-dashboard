import { useSellerShipping } from './useSellerShipping';
import SellerShippingBoxPlot from './SellerShippingBoxPlot';

export default function SellerShippingContainer() {
  const { data, isLoading, isError } = useSellerShipping();

  if (isLoading) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-gray-50 rounded-lg border border-gray-200">
        <span className="text-gray-500 animate-pulse">Loading shipping data...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-96 flex items-center justify-center bg-red-50 rounded-lg border border-red-200">
        <span className="text-red-500">Failed to load shipping times.</span>
      </div>
    );
  }

  return <SellerShippingBoxPlot data={data} />;
}
