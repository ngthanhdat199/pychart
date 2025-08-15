from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
import random
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # allow frontend to connect

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/candles')
def get_candles():
    candles = []
    base_time = int(time.time()) - (100 * 60)
    price = 100
    for i in range(100):
        open_price = round(price + random.uniform(-2, 2), 2)
        close_price = round(open_price + random.uniform(-2, 2), 2)
        high_price = round(max(open_price, close_price) + random.uniform(0, 2), 2)
        low_price = round(min(open_price, close_price) - random.uniform(0, 2), 2)
        candles.append({
            "time": base_time + i * 60,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price
        })
        price = close_price
    return jsonify(candles)

# 🔁 Background thread to emit new candles every few seconds
def generate_realtime_data():
    price = 120
    while True:
        time.sleep(1)
        now = int(time.time())
        open_price = round(price + random.uniform(-1, 1), 2)
        close_price = round(open_price + random.uniform(-1.5, 1.5), 2)
        high_price = round(max(open_price, close_price) + random.uniform(0, 1), 2)
        low_price = round(min(open_price, close_price) - random.uniform(0, 1), 2)
        candle = {
            "time": now,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price
        }
        price = close_price
        socketio.emit('new_candle', candle)

# 🔧 Start background thread after server starts
@socketio.on('connect')
def handle_connect():
    global thread
    if not thread.is_alive():
        thread.start()

# Start the background thread once
thread = threading.Thread(target=generate_realtime_data)
thread.daemon = True

if __name__ == '__main__':
    socketio.run(app, debug=True)
