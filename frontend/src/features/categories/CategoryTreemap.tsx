import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { CategorySalesResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: CategorySalesResponse;
}

export default function CategoryTreemap({ data }: Props) {
  // Plotly requires a 'parents' array of the exact same length as the labels.
  // Since thiis IS a flat hierarchy, they all share an empty string parent.
  const parents = Array(data.category.length).fill('');

  return (
     <ChartCard>
      <Plot
        data={[
          {
            type: 'treemap',
            labels: data.category,
            values: data.sales,
            parents: parents,
            marker: {
              colors: data.sales,
              colorscale: 'Viridis', // From nootebook
              showscale: true, // Adds the legend on the side
            },
            textinfo: 'label+value',
            hoverinfo: 'label+value+percent parent',
          },
        ]}
        layout={{
          title: {
            text: 'Sales by Category',
            font: { color: '#6b7280' },
          },
          autosize: true,
          margin: { t: 40, r: 0, l: 0, b: 0 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
        }}
        useResizeHandler={true}
        style={{ width: '100%', height: '100%' }}
        config={{ displayModeBar: false }}
      />
    </ChartCard>
  );
}
