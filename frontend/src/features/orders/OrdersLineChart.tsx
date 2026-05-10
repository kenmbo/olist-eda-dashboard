import Plotly from 'plotly.js-basic-dist';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { DailyOrdersResponse } from '../../types/api';

// Create a Plot component to use in a JSX
const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: DailyOrdersResponse;
}

export default function OrdersLineChart({ data }: Props) {
  return (
    // Tailwind styling for the chart container
    <div className="w-full h-96 bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
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
          title: {
            text: 'Daily Orders',
            font: { color: '#6b7280' }, // Tailwind gray-500
          },
          autosize: true, // Tells Plotly to fill the container
          margin: { t: 40, r: 20, l: 40, b: 40 },
          paper_bgcolor: 'transparent', // Let the Tailwind bg color show through
          plot_bgcolor: 'transparent',
          xaxis: { 
            gridcolor: '#e5e7eb', // Tailwind gray-200
            tickfont: { color: '#9ca3af' }
          },
          yaxis: { 
            gridcolor: '#e5e7eb',
            tickfont: { color: '#9ca3af' }
          },
        }}
        useResizeHandler={true} // Essential for responsive Tailwind layouts
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }} // Hides the Plotly toolbar for a cleaner look
      />
    </div>
  );
}

