import createPlotlyComponent from 'react-plotly.js/factory';
import type { DeliveryTrendResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: DeliveryTrendResponse;
}

export default function DeliveryTrendChart({ data }: Props) {
  return (
    <ChartCard heightClass="h-80" title="Average Delivery Time with LOWESS Trend">
      <Plot
        data={[
          {
            // The raw, noisy daily averages
            x: data.dates,
            y: data.actual_days,
            type: 'scatter',
            mode: 'lines',
            name: 'Daily Average',
            line: { color: '#4b5563', width: 1 }, // Tailwind gray-600, thin line
            opacity: 0.5,
          },
          {
            // The smooth LOWESS trendline
            x: data.dates,
            y: data.trend_days,
            type: 'scatter',
            mode: 'lines',
            name: 'Trend',
            line: { color: '#3b82f6', width: 3 }, // Tailwind blue-500, thick line
          }
        ]}
        layout={{
          autosize: true,
          margin: { t: 10, r: 20, l: 40, b: 40 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: {
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' }
          },
          yaxis: {
            title: 'Days to Deliver',
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
            rangemode: 'tozero', // Forces the Y-axis to start at 0
          },
          legend: {
            font: { color: '#9ca3af' },
            orientation: 'h',
            yanchor: 'bottom',
            y: 1.02,
            xanchor: 'right',
            x: 1
          }
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </ChartCard>
  );
}
