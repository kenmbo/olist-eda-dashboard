import { useLeadOrigins } from './useLeadOrigins';
import LeadOriginsChart from './LeadOriginsChart';

export default function LeadOriginsContainer() {
  const { data, isLoading, isError } = useLeadOrigins();

  if (isLoading) {
    return (
      <div className="w-full h-80 flex items-center justify-center bg-gray-900 rounded-lg border border-gray-800">
        <span className="text-gray-400 animate-pulse">Loading lead origins...</span>
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="w-full h-80 flex items-center justify-center bg-red-900/20 rounded-lg border border-red-800">
        <span className="text-red-400">Failed to load lead origins.</span>
      </div>
    );
  }

  return <LeadOriginsChart data={data} />;
}
