from websocket import WebSocketApp
import json
import time
from datetime import datetime

recent_delays = []

def on_message(ws, message):
    global recent_delays

    data = json.loads(message)
    price = float(data['p'])
    quantity = float(data['q'])
    trade_time = int(data['T'])
    trade_datetime = datetime.fromtimestamp(trade_time / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    is_buyer_maker = data['m']
    trade_side = 'Buy' if is_buyer_maker else 'Sell'

    current_time = time.time()
    delay = (current_time - (trade_time / 1000)) * 1000
    recent_delays.append((current_time, delay))

    # Remove delays older than 5 seconds
    recent_delays = [(t, d) for t, d in recent_delays if (current_time - t) <= 5]

    # Calculate the average delay
    if len(recent_delays) > 0:
        average_delay = sum(d for _, d in recent_delays) / len(recent_delays)
    else:
        average_delay = 0

    print(f'BINANCE BTCUSDT: {trade_side} | At: {price} | Qty: {quantity} | Trade time: {trade_datetime} | Delay: {average_delay:.0f} ms')

def on_error(ws, error):
    print(f'Error: {error}')

def on_close(ws):
    print('WebSocket closed')

def on_open(ws):
    print('WebSocket opened')

if __name__ == '__main__':
    symbol = 'btcusdt'
    websocket_url = f'wss://stream.binance.com:9443/ws/{symbol}@trade'

    ws = WebSocketApp(websocket_url,
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

