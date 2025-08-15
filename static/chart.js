// Create the chart
const chart = LightweightCharts.createChart(document.getElementById('chart'), {
    layout: {
        background: { color: '#000' },
        textColor: '#ccc',
    },
    grid: {
        vertLines: { color: '#222' },
        horzLines: { color: '#222' },
    },
    timeScale: {
        timeVisible: true,
        secondsVisible: false,
    },
    crosshair: {
        mode: 0,
    },
});

// Global candle series
const candleSeries = chart.addCandlestickSeries();

// Load initial historical data
fetch('/api/candles')
    .then(res => res.json())
    .then(data => {
        candleSeries.setData(data);
    });

// Setup WebSocket for real-time updates
const socket = io();  // connects to Flask-SocketIO backend

socket.on('new_candle', (candle) => {
    console.log("New candle received:", candle);
    candleSeries.update(candle);
});
