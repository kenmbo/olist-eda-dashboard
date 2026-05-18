import type { SellerShippingResponse } from '../../types/api';
import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: SellerShippingResponse;
}

export default function SellerShippingBoxPlot({ data }: Props) {
  return None;
}

export default function SellerShippingBoxPlot({ data }: Props) {
  return (
    <div className="w-full h-96 bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
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
       />
     </div>
   );
}
