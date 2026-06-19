import Plotly, { Data } from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { CategoryWeightResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: CategoryWeightResponse;
}

export default function CategoryWeightsBoxplot({ data }: Props) {
  const traces: Data[] = Object.entries(data).map(([category, weights]) => ({
    y: weights,
    type: 'box',
    name: category.replace(/_/g, ' '), // Clean up snake_case
    boxpoints: 'outliers', // Show outlier dots
    marker: { size: 3 }, // Make the outlier dots a bit smaller
    line: { width: 1.5 },
  }));

  return (
    <ChartCard heightClass="h-80" title="Product Weight Distribution by Category">
      <Plot
        data={traces}
      />
    </ChartCard>
  );
}
