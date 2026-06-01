import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { OrderCostsResponse } from '../../types/api';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: OrderCostsResponse;
}

export default function OrderCostsHistograms({ data }: Props) {
  // Shared layout properties to keep the code DRY
  const sharedLayout = {
    autosize: true,
    margin: { t: 40, r: 20, l: 40, b: 40 },
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    yaxis: {
      title: 'Frequency',
      gridcolor: '#374151',
      tickfont: { color: '#9ca3af' },
    },
  };

  return (
    // Tailwind grid wrapper for side-by-side layout
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 w-full">
      
      {/* Left Chart: Product Cost */}
      <div className="h-96 bg-gray-900 rounded-lg shadow-md p-4 border border-gray-800">
        <Plot
          data={[
            {
              x: data.product_cost,
              type: 'histogram',
              nbinsx: 1000,
              marker: { color: '#6c87a3' },
            },
          ]}
          layout={{
            ...sharedLayout,
            title: {
              text: 'Product cost for orders < R$500',
              font: { color: '#9ca3af' },
            },
            xaxis: {
              title: 'Product cost (BRL)',
              gridcolor: '#374151',
              tickfont: { color: '#9ca3af' },
              range: [0, 500],
            },
          }}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
          config={{ displayModeBar: false }}
        />
      </div>

      {/* Right Chart: Shipping Cost */}
      <div className="h-96 bg-gray-900 rounded-lg shadow-md p-4 border border-gray-800">
        <Plot
          data={[
            {
              x: data.shipping_cost,
              type: 'histogram',
              nbinsx: 800,
              marker: { color: '#ad865f' },
            },
          ]}
          layout={{
            ...sharedLayout,
            title: {
              text: 'Shipping cost for orders < R$80',
              font: { color: '#9ca3af' },
            },
            xaxis: {
              title: 'Shipping cost (BRL)',
              gridcolor: '#374151',
              tickfont: { color: '#9ca3af' },
              range: [0, 80], // Filtering the view
            },
          }}
          useResizeHandler={true}
          style={{ width: '100%', height: '100%' }}
          config={{ displayModeBar: false }}
        />
      </div>

    </div>
  );
}
