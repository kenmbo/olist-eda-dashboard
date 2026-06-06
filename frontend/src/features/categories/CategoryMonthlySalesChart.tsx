import Plotly, { Data } from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { CategoryMonthlySalesResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: CategoryMonthlySalesResponse;
}

export default function CategoryMonthlySalesChart({ data }: Props) {
  // Dynamically generate a trace for each category in the payload
  const traces: Data[] = data.columns.map((category, colIndex) => ({
    x: data.index,
    y: data.data.map(row => row[colIndex]), // Extract the column data across all rows
    type: 'scatter',
    mode: 'lines',
    name: category.replace(/_/g, ' '), // Clean up the snake_case category names
    line: { width: 2, shape: 'spline' }, // 'spline' creates smooth curves
  }));

  return (
    <ChartCard heightClass="h-80" title="Monthly Sales for Selected Categories">
      <Plot data={traces}/>
    </ChartCard>
  );
}
