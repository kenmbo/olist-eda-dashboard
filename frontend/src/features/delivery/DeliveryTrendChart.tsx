import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { DeliveryTrendResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: DeliveryTrendResponse;
}

export default function DeliveryTrendChart({ data }: Props) {
  return (
    <ChartCard heightClass="h-80" title="Average Delivery Time with LOWESS Trend">
      <Plot
        data={[
          {
            // The raw, noisy daily averages
            x: data.dates,
            y: data.actual_days,
            type: 'scatter',
            mode: 'lines',
            name: 'Daily Average',
            line: { color: '#4b5563', width: 1 },
            opacity: 0.5,
          },
          {
            // The smooth LOWESS trendline
            x: data.dates,
            y: data.trend_days,
            type: 'scatter',
            mode: 'lines',
            name: 'Trend',
            line: { color: '#3b82f6', width: 3 },
          }
        ]}
      />
    </ChartCard>
  );
}
