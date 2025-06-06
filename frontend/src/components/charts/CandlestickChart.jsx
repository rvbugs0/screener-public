// components/CandlestickChart.jsx
import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

const CandlestickChart = ({ chartData,earlyShifts,swingHighs,swingLows,trendShifts,trend,highOrLowIndex,lastHopeIndex }) => {
  

  let candleData = []
  let dateData = []

  function timestampToDateString(timestamp) {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const day = String(date.getDate()).padStart(2, '0');
    
    return `${year}-${month}-${day}`;
  }
  
  Object.entries(chartData).forEach((_,key)=>{
    let item = chartData[key]
    
    candleData.push ([item.open.toFixed(2),item.close.toFixed(2),item.low.toFixed(2),item.high.toFixed(2)])
    dateData.push(timestampToDateString(item.time))
  })


  let markPoints = []

  earlyShifts.forEach((i)=>{
    // if((trend==-1 && i>lastHopeIndex) ){
    markPoints.push( { name: 'Early Trend Shift', value: chartData[i].close, coord: [i, chartData[i].close], symbol: 'diamond',itemStyle: { color: 'blue' } })
    // }else if((trend==1 && i>lastHopeIndex)){
      // markPoints.push( { name: 'Diamond', value: chartData[i].low, coord: [i, chartData[i].low], symbol: 'diamond',itemStyle: { color: 'blue' } })
    // }
  })

  trendShifts.forEach((i)=>{

    if((trend==-1 && i>lastHopeIndex) ||(trend==1 && i>lastHopeIndex)){
    markPoints.push( { name: 'Trend Shift', value: chartData[i].close, coord: [i, chartData[i].open], symbol: 'pin',itemStyle: { color: 'black' } })
    }
  })


  swingLows.forEach((i)=>{
    // if((trend==-1 && i>lastHopeIndex) ||(trend==1 && i>lastHopeIndex)){
    
    markPoints.push( { name: 'Swing Low', value: chartData[i].close, coord: [i, chartData[i].low], symbol: 'triangle',itemStyle: { color: 'orange' },symbolRotate: 180 , symbolSize:15})
    // }
  })

  swingHighs.forEach((i)=>{
    // if((trend==-1 && i>lastHopeIndex) ||(trend==1 && i>lastHopeIndex)){
      // mark swing highs only after last hope
      markPoints.push( { name: 'Swing High', value: chartData[i].close, coord: [i, chartData[i].high], symbol: 'triangle',itemStyle: { color: 'green' ,symbolSize: 15} })
      
    // }

  })

  if(trend==-1){
    markPoints.push( { name: 'High', value: chartData[lastHopeIndex].high, coord: [lastHopeIndex, chartData[lastHopeIndex].high], symbol: 'pin',itemStyle: { color: 'red' },symbolSize: 35,  })
  }
  if(trend==1){
    markPoints.push( { name: 'Low', value: chartData[lastHopeIndex].low, coord: [lastHopeIndex, chartData[lastHopeIndex].low], symbol: 'pin',itemStyle: { color: 'green' }, symbolSize: 35, position:'bottom' ,symbolRotate: 180})
  }

  
  let transformedData = {values:candleData,categoryData:dateData}
  
  const chartRef = useRef(null);
  //   https://echarts.apache.org/examples/en/editor.html?c=candlestick-sh

  // const upColor = '#00da3c';
  // const downColor = '#ec0000';

  const upColor = '#ddd';
  const downColor = '#000';
  const upBorderColor = '#8A0000';
  
  const downBorderColor = '#008F28';


  function calculateMA(dayCount) {
    var result = [];
    for (var i = 0, len = transformedData.values.length; i < len; i++) {
      if (i < dayCount) {
        result.push('-');
        continue;
      }
      var sum = 0;
      for (var j = 0; j < dayCount; j++) {
        sum += +transformedData.values[i - j][1];
      }
      result.push((sum / dayCount).toFixed(2));
    }
    return result;
  }

  useEffect(() => {
    const chartInstance = echarts.init(chartRef.current);


    const 
    options = {
      title: {
        text: '',
        left: 0
      },
      tooltip: {
        triggerOn: 'click',
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: ['Price']
      },
      grid: {

        bottom: '80'
      },
      xAxis: {
        type: 'category',
        data: transformedData.categoryData,
        axisLine: { lineStyle: { color: '#8392A5' } }
      },
      yAxis: {
        scale: true,
        splitArea: {
          show: true
        }
      },
      dataZoom: [
        {
          type: 'inside',
          start: 50,
          end: 100
        },
        {
          show: false,
          type: 'slider',
          top: '90%',
          start: 50,
          end: 100
        }
      ],
      series: [
        {
          name: 'Price',
          type: 'candlestick',
          data: transformedData.values,
          itemStyle: {
            color: upColor,
            color0: downColor,
            borderColor: upBorderColor,
            borderColor0: downBorderColor
          },
          markPoint: {
            
            symbolSize: 10, // Adjust size if needed
            label: {
              show: false,
              formatter: '{b}: {c}', // Show name and value
              position: 'inside',
            },
            data: markPoints,
            tooltip: {
              formatter: function (param) {
                return param.name + '<br>' + (param.data.coord[1] || '');
              }
            }
          },
        },
        

      ]
    };
    
    

    chartInstance.setOption(options);

    return () => {
      chartInstance.dispose();
    };
  }, [transformedData]);

  return <div ref={chartRef} style={{ width: '100%', height: '500px' }} />;
};

export default CandlestickChart;
