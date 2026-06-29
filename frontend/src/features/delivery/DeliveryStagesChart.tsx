import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { DeliveryStagesResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: DeliveryStagesResponse;
}

export default function DeliveryStagesChart({ data }: Props) {
  return (
    <ChartCard heightClass="h-80" title="Average Days per Order Stage (Top 10 Cities)">
      <Plot
        data={[
          {
            x: data.cities,
            y: data.approval_days,
            type: 'bar',
            name: 'Approval Time',
            marker: { color: '#eab308' },
          },
          {
            x: data.cities,
            y: data.carrier_days,
            type: 'bar',
            name: 'Carrier Prep',
            marker: { color: '#f97316' }, // Tailwind blue-500
          },
          {
            x: data.cities,
            y: data.transit_days,
            type: 'bar',
            name: 'Transit Time',
            marker: { color: '#e11d48' }, // Tailwind indigo-400
          }
        ]}
        layout={{
          barmode: 'stack', // This stacks the bars instead of grouping them side-by-side
          autosize: true,
          margin: { t: 10, r: 20, l: 40, b: 60 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: { 
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
            tickangle: -45, // Angle the city names so they fit nicely
          },
          yaxis: { 
            title: 'Average Days',
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
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
