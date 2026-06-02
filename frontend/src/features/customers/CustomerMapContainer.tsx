import { useCustomerMap } from './useCustomerMap';
import CustomerDensityMap from './CustomerDensityMap';

export default function CustomerMapContainer() {
  const { data, isLoading, isError } = useCustomerMap();

  if (isLoading) {
    return (
      <div className="w-full h-[500px] flex items-center justify-center bg-gray-800 rounded-lg border border-gray-700">
        <span className="text-gray-400 animate-pulse">Loading customer map...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-[500px] flex items-center justify-center bg-red-900/20 rounded-lg border border-red-800">
        <span className="text-red-400">Failed to load customer map.</span>
      </div>
    );
  }

  return <CustomerDensityMap data={data} />;
}
