import Plotly from 'plotly.js-dist-min';
import createPlotlyComponent from 'react-plotly.js/factory';
import type { DeliveryTrendResponse } from '../../types/api';
import ChartCard from '../../components/common/ChartCard';

const Plot = createPlotlyComponent.default(Plotly);

interface Props {
  data: DeliveryTrendResponse;
}

export default function DeliveryTrendChart({ data }: Props) {

  // Calculate 25% and 75% markers based on the dataset length
  const totalPoints = data.dates.length;
  const startIndex = Math.floor(totalPoints * 0.25);
  const endIndex = Math.floor(totalPoints * 0.75);

  return (
    <ChartCard heightClass="h-80" title="Average Delivery Time with LOWESS Trend">
      <Plot
        data={[
          {
            x: data.dates,
            y: data.actual_days,
            type: 'scatter',
            mode: 'lines',
            name: 'Daily Average',
            line: { color: 'white', width: 1 }, // Tailwind gray-600, thin line
            opacity: 1,
	    fill: 'tozeroy',
  fillgradient: {
    type: 'vertical',
    colorscale: [
      //[0, 'rgba(255, 165, 10, 0)'], // Starting color with 80% opacity
      [0, 'rgba(0, 165, 10, 0)'], // Starting color with 80% opacity
      //[1, 'rgba(255, 165, 10, 0.5)']    // Fades to fully transparent at the other end
      [1, 'rgba(0, 165, 10, 0.5)']    // Fades to fully transparent at the other end
    ],
    // 'start' and 'stop' define the axis range the gradient spans
    // Note: If zooming/panning, you may need to update these values dynamically
    start: 0, 
    stop: 17  
  },
          },
          {
            // LOWESS trendline
            x: data.dates,
            y: data.trend_days,
            type: 'scatter',
            mode: 'lines',
            name: 'Trend',
            line: { color: '#ddd', width: 3 },
	    opacity: 0.4,
          }
        ]}
        layout={{
          autosize: true,
          margin: { t: 10, r: 20, l: 40, b: 40 },
          paper_bgcolor: 'transparent',
          plot_bgcolor: 'transparent',
          xaxis: { 
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
            rangemode: 'normal',
            range: [data.dates[startIndex], data.dates[endIndex]],
          },
          yaxis: { 
            title: 'Days to Deliver',
            gridcolor: '#374151',
            tickfont: { color: '#9ca3af' },
            rangemode: 'tozero',
            range: [0, 25],
          },
          legend: {
            font: { color: '#9ca3af' },
            orientation: 'h',
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
