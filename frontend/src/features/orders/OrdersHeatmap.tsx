import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { HourlyOrdersResponse } from '../../types/api';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: HourlyOrdersResponse;
}

export default function OrdersHeatmap({ data }: Props) {
  return (
<div className="w-full h-96 bg-gray-900 rounded-lg shadow-md p-4 border border-gray-800">
	Coming soon
</div>
  );
}
