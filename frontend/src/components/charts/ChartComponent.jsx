// components/EChartComponent.jsx
import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

const ChartComponent = ({ chartData }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const chartInstance = echarts.init(chartRef.current);

    // Chart options using the JSON data
    const options = {
      title: {
        text: 'Sample Chart',
      },
      tooltip: {},
      xAxis: {
        type: 'category',
        data: chartData.map((item) => item.category),
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          name: 'Value',
          type: 'bar',
          data: chartData.map((item) => item.value),
        },
      ],
    };

    chartInstance.setOption(options);

    // Clean up on component unmount
    return () => {
      chartInstance.dispose();
    };
  }, [chartData]);

  return <div ref={chartRef} style={{ width: '100%', height: '400px' }} />;
};

export default ChartComponent;
