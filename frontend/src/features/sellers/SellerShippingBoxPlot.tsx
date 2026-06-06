import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { SellerShippingResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: SellerShippingResponse;
}

export default function SellerShippingBoxPlot({ data }: Props) {
  return (
     <ChartCard title="Delivery Time by Seller Order Volume">
      <Plot
        data={[
          {
            x: data.bucket, // The categorical groups
            y: data.delivery_time, // The numerical values
            type: 'box',
            boxpoints: false, // Disables plotting individual dots, just like your Python script
            marker: { color: '#8b5cf6' }, // Tailwind purple-500
          },
        ]}
        layout={{
          autosize: true,
          margin: { t: 0, r: 5, l: 15, b: 15 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: {
            title: 'Sellers with...',
            gridcolor: '#e5e7eb',
            tickfont: { color: '#9ca3af' },
            // Force Plotly to display the buckets in correct numerical order
            categoryorder: 'array',
            categoryarray: ['1-9 orders', '10-99 orders', '100-999 orders', '1000+ orders'],
          },
          yaxis: {
            title: 'Shipping time (days)',
            gridcolor: '#e5e7eb',
            tickfont: { color: '#9ca3af' },
          },
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
     </ChartCard>
  );
}
