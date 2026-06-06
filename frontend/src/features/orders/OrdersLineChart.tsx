import Plotly from 'plotly.js-basic-dist';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { DailyOrdersResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

// Create a Plot component to use in a JSX
const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: DailyOrdersResponse;
}

export default function OrdersLineChart({ data }: Props) {
  return (
    // Tailwind styling for the chart container
    <ChartCard heightClass="h-72" title="Daily Orders">
      <Plot
        data={[
          {
            x: data.day, // Plugs straight in, no mapping required
            y: data.order_count,
            type: 'scatter',
            mode: 'lines',
            line: { color: '#3b82f6', width: 2 }, // Tailwind blue-500
          },
        ]}
        layout={{
          autosize: true, // Tells Plotly to fill the container
          margin: { t: 40, r: 20, l: 40, b: 40 },
          paper_bgcolor: 'transparent', // Let the Tailwind bg color show through
          plot_bgcolor: 'transparent',
          coloraxis: {colorbar:'white'},
          xaxis: {
            gridcolor: '#555', // Tailwind gray-200
            zeroline: 'true',
            zerolinecolor: '#ff0000',
            zerolinewidth: 2,
            tickfont: { color: 'white' },
          },
          yaxis: { 
            gridcolor: '#444',
            griddash: 'dot',
            tickfont: { color: '#9ca3af' }
          },
        }}
        useResizeHandler={true} // Essential for responsive Tailwind layouts
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }} // Hides the Plotly toolbar for a cleaner look
      />
    </ChartCard>
  );
}

