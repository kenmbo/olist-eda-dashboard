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
      <Plot
        data={traces}
        layout={{
          autosize: true,
          margin: { t: 10, r: 20, l: 40, b: 40 }, // Top margin reduced to 10
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: { 
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
            tickangle: -45, // Angled text to prevent month labels from overlapping
          },
          yaxis: { 
            title: 'Revenue (BRL)',
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' }
          },
          legend: {
            font: { color: '#9ca3af' },
            orientation: 'h', // Horizontal legend looks better on wide charts
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
