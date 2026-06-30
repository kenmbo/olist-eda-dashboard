import { useQuery } from '@tanstack/react-query';
import type { LeadOriginResponse } from '../../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const fetchLeadOrigins = async (): Promise<LeadOriginResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/leads/origin`);
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
};

export const useLeadOrigins = () => {
  return useQuery({
    queryKey: ['leadOrigins'],
    queryFn: fetchLeadOrigins,
    staleTime: 1000 * 60 * 5,
  });
};
