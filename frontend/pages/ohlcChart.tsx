import React, { useEffect, useRef } from 'react';
import { GetServerSideProps } from 'next';
import { createChart } from 'lightweight-charts';
import { parse } from 'papaparse';

type Data = {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
};

type Props = {
  data: Data[];
};

export const getServerSideProps: GetServerSideProps<Props> = async () => {
  const response = await fetch('data.csv');

  if (!response.ok) {
    throw new Error(`Failed to fetch data: ${response.status} ${response.statusText}`);
  }

  const csv = await response.text();
  const results = await parse(csv, { header: true });

  const data = results.data.map((d: any) => ({
    time: d.time,
    open: parseFloat(d.open),
    high: parseFloat(d.high),
    low: parseFloat(d.low),
    close: parseFloat(d.close),
  }));

  return { props: { data } };
};

function CandleChart({ data }: Props) {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!chartRef.current) return;

    const chart = createChart(chartRef.current, { width: 1600, height: 800 });
    const candlestickSeries = chart.addCandlestickSeries();

    candlestickSeries.setData(data);

    return () => {
      chart.remove();
    };
  }, [data]);

  return <div ref={chartRef} />;
}

export default CandleChart;
