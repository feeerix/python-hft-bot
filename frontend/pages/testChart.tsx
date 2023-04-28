import React from 'react';
import { createChart, isUTCTimestamp } from 'lightweight-charts';
import { useEffect, useRef } from 'react';
import Papa from 'papaparse';

async function loadCsvData() {
  const response = await fetch('/testChart.csv');
  const file = await response.text();
  const parsedData = Papa.parse(file, { header: true }).data;
  return parsedData;
}


function TestChart() {
    const chartContainerRef = useRef<HTMLDivElement>(null);
    
    useEffect(() => {
        
        const container = chartContainerRef.current;
        if (container) {
          let csvdata = loadCsvData();
          
          const chart = createChart(container, { width: 1600, height: 800 });
          // isUTCTimestamp(true)
          // const ohlcSeries = chart.addCandlestickSeries();
          // ohlcSeries.setData(csvdata);
            
          const lineSeries = chart.addLineSeries();
          lineSeries.setData([
              { time: '2019-04-11', value: 80.01 },
              { time: '2019-04-12', value: 96.63 },
              { time: '2019-04-13', value: 76.64 },
              { time: '2019-04-14', value: 81.89 },
              { time: '2019-04-15', value: 74.43 },
              { time: '2019-04-16', value: 80.01 },
              { time: '2019-04-17', value: 96.63 },
              { time: '2019-04-18', value: 16.64 },
              { time: '2019-04-19', value: 91.89 },
              { time: '2019-04-20', value: 71.43 },
          ]);

          return () => {
              if (chart) {
                chart.remove();
              }
          };
        }
    }, []);
  
    return <div ref={chartContainerRef} />
  }

export default React.memo(TestChart);