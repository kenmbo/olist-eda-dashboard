import Plotly, { Data } from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { CategoryWeightResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: CategoryWeightResponse;
}

export default function CategoryWeightsBoxplot({ data }: Props) {
  // Dynamically generate a box trace for each category in the dictionary
  const traces: Data[] = Object.entries(data).map(([category, weights]) => ({
    y: weights,
    type: 'box',
    name: category.replace(/_/g, ' '), // Clean up snake_case
    boxpoints: 'outliers', // Show outlier dots
    marker: { size: 3 }, // Make the outlier dots a bit smaller
    line: { width: 1.5 },
    jitter: 1,
    boxpoints: 'outliers',
    pointpos: 0,
    boxmean: 'sd'
  }));

  return (
    <ChartCard heightClass="h-80" title="Product Weight Distribution by Category">
      <Plot
        data={traces}
        layout={{
          autosize: true,
          margin: { t: 10, r: 20, l: 60, b: 40 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          showlegend: false, // Hide legend since the x-axis already labels them
          xaxis: { 
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
          },
          yaxis: { 
            title: 'Weight (grams)',
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
            zerolinecolor: '#4b5563',
          },
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </ChartCard>
  );
}
