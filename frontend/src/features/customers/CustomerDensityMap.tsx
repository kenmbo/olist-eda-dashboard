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
    <div className="w-full h-[500px] bg-gray-900 rounded-lg shadow-md p-4 border border-gray-800">
      <Plot
        data={[
          {
            type: 'densitymapbox',
            lon: data.longitude,
            lat: data.latitude,
            z: data.customer_count,
            radius: 15,
            colorscale: 'Viridis',
            hoverinfo: 'text',
            text: hoverText,
            colorbar: {
              title: { text: "Customers", font: { color: '#FFF' } },
              tickfont: { color: '#FFF' },
              bgcolor: "rgba(0,0,0,0.5)",
              x: 0.8,
              y: 0.9,
              len: 0.8,
              xanchor: "left",
              yanchor: "top"
            }
          },
        ]}
        layout={{
          title: {
            text: 'Customer Density',
            font: { color: '#9ca3af' },
          },
          autosize: true,
          margin: { t: 40, r: 0, l: 0, b: 0 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          mapbox: {
            style: 'carto-darkmatter',
            center: { lat: -14.2350, lon: -51.9253 }, // Centered on Brazil
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
