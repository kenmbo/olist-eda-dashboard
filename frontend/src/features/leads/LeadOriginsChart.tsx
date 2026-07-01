import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { LeadOriginResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: LeadOriginResponse;
}

export default function LeadOriginsChart({ data }: Props) {
  return (
    <ChartCard heightClass="h-80" title="Leads by Origin Channel">
      <Plot
        data={[
          {
            // Note: For horizontal bars, 'x' is the numerical value and 'y' is the category
            x: data.leads,
            y: data.origins,
            type: 'bar',
            orientation: 'h', 
            marker: { 
              color: '#8b5cf6', // Tailwind violet-500
              opacity: 0.9 
            },
            // Add data labels right on the bars for instant readability
            text: data.leads.map(String),
            textposition: 'auto',
            hoverinfo: 'y+text',
          }
        ]}
        layout={{
          autosize: true,
          margin: { t: 10, r: 40, l: 120, b: 40 }, // Expanded left margin (l: 120) so text fits
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: { 
            title: 'Number of Leads',
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' }
          },
          yaxis: { 
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
          }
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </ChartCard>
  );
}

