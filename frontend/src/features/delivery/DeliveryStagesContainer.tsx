import { useDeliveryStages } from './useDeliveryStages';
import DeliveryStagesChart from './DeliveryStagesChart';

export default function DeliveryStagesContainer() {
  const { data, isLoading, isError } = useDeliveryStages();

  if (isLoading) {
    return (
      <div className="w-full h-80 flex items-center justify-center bg-gray-900 rounded-lg border border-gray-800">
        <span className="text-gray-400 animate-pulse">Loading weight distributions...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-80 flex items-center justify-center bg-red-900/20 rounded-lg border border-red-800">
        <span className="text-red-400">Failed to load product weights.</span>
      </div>
    );
  }

  return <DeliveryStagesChart data={data} />;
}
