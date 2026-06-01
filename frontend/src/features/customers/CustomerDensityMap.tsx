// src/features/customers/CustomerDensityMap.tsx
import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { CustomerMapResponse } from '../../types/api';


const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: CustomerMapResponse;
}

export default function CustomerDensityMap({ data }: Props) {
  // Replicate the custom hover template from Python
  const hoverText = data.zip_prefix.map((zip, i) => 
    `Zip code: ${zip}<br>Average CLV: ${Math.round(data.avg_CLV[i])}<br>Customers: ${data.customer_count[i]}<br>Latitude: ${data.latitude[i].toFixed(4)}<br>Longitude: ${data.longitude[i].toFixed(4)}`
  );

return (
    // 2. Wrap the Plot in the ChartCard. Pass the custom height since maps look better taller.
    <div className="w-full h-[500px] bg-gray-900 rounded-lg shadow-md p-4 border border-gray-800">
      <Plot
        data={[{
          type: 'densitymap',
          lon: data.longitude,
          lat: data.latitude,
          z: data.customer_count,
          radius: 15,
          colorscale: 'Viridis',
          hoverinfo: 'text',
          text: hoverText,
          // ... keeping all your existing colorbar configs
        }]}
        layout={{
          title: { text: 'Customer Density', font: { color: '#9ca3af' } },
          autosize: true,
          margin: { t: 40, r: 0, l: 0, b: 0 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          map: {
            style: 'carto-darkmatter',
            center: { lat: -14.2350, lon: -51.9253 }, 
            zoom: 3,
          },
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </div>
  );
}
