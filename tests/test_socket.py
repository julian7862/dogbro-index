"""
Socket.IO client test script for gateway communication
This demonstrates how to connect to the Node.js gateway and send/receive events
"""

import socketio
import time
from datetime import datetime

# Create Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print(f'[{datetime.now()}] Connected to gateway server')

    # Send test event
    sio.emit('python_ready', {
        'status': 'connected',
        'timestamp': datetime.now().isoformat()
    })

@sio.event
def disconnect():
    print(f'[{datetime.now()}] Disconnected from gateway server')

@sio.on('*')
def catch_all(event, data):
    """Catch all events from the server"""
    print(f'[{datetime.now()}] Received event "{event}": {data}')

# Custom event handlers
@sio.on('market_data')
def on_market_data(data):
    print(f'[{datetime.now()}] Market data received: {data}')

@sio.on('order_update')
def on_order_update(data):
    print(f'[{datetime.now()}] Order update: {data}')

def main():
    gateway_url = 'http://localhost:3001'

    try:
        print(f'Connecting to {gateway_url}...')
        sio.connect(gateway_url)

        # Send periodic test messages
        counter = 0
        while True:
            time.sleep(5)
            counter += 1

            # Emit test event
            sio.emit('heartbeat', {
                'count': counter,
                'timestamp': datetime.now().isoformat(),
                'message': f'Heartbeat #{counter}'
            })
            print(f'[{datetime.now()}] Sent heartbeat #{counter}')

    except KeyboardInterrupt:
        print('\nShutting down...')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        sio.disconnect()
        print('Disconnected')

if __name__ == '__main__':
    main()
