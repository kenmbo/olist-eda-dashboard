import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { HourlyOrdersResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: HourlyOrdersResponse;
}

export default function OrdersHeatmap({ data }: Props) {
  return (
    <ChartCard heightClass="h-72">
      <Plot
        data={[
          {
            x: data.columns, 
            y: data.index,
            z: data.data,
            type: 'heatmap',
            colorscale: 'YlGnBu', // Replicating your Python script
            hoverongaps: false,
          },
        ]}
        layout={{
          title: {
            text: 'Orders by Day and Hour',
            font: { color: '#9ca3af' }, // Tailwind gray-400
          },
          autosize: true,
          margin: { t: 40, r: 20, l: 40, b: 40 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: {
            title: 'Hour of Day',
            gridcolor: '#374151', // Tailwind gray-700
            tickfont: { color: '#9ca3af' },
          },
          yaxis: {
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
            autorange: 'reversed', // Keeps Monday at the top, Sunday at the bottom
          },
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </ChartCard>
  );
}
