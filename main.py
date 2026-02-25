import shioaji as sj
import socketio
import time
from datetime import datetime
from src.utils.config import config

print(f"Shioaji version: {sj.__version__}")

# Initialize Socket.IO client
sio = socketio.Client()
GATEWAY_URL = 'http://localhost:3001'

@sio.event
def connect():
    print(f'[{datetime.now()}] Connected to gateway server')
    sio.emit('python_status', {
        'status': 'connected',
        'timestamp': datetime.now().isoformat()
    })

@sio.event
def disconnect():
    print(f'[{datetime.now()}] Disconnected from gateway server')

@sio.on('*')
def catch_all(event, data):
    """Catch all events from gateway"""
    print(f'[Gateway] Event "{event}": {data}')

def main():
    api = None

    try:
        # Connect to gateway
        print(f'Connecting to gateway at {GATEWAY_URL}...')
        sio.connect(GATEWAY_URL)

        # Initialize Shioaji API
        print('Initializing Shioaji API...')
        api = sj.Shioaji(simulation=True)

        # Login
        api.login(
            api_key=config.api_key,
            secret_key=config.secret_key,
            fetch_contract=False
        )
        print("Shioaji login successful")

        # Activate CA
        api.activate_ca(
            ca_path=config.ca_cert_path,
            ca_passwd=config.ca_password,
        )
        print("CA activation successful")

        # Emit success status to gateway
        sio.emit('shioaji_ready', {
            'status': 'ready',
            'timestamp': datetime.now().isoformat(),
            'simulation': True
        })

        # Test: Get some contracts
        contracts = list(api.Contracts.Options.TXO.items())[:3]
        print(f"Sample contracts: {contracts}")

        # Emit sample data to gateway
        sio.emit('contracts_loaded', {
            'count': len(contracts),
            'sample': str(contracts),
            'timestamp': datetime.now().isoformat()
        })

        # Keep the process running
        print('Main loop started. Press Ctrl+C to exit.')
        while True:
            time.sleep(10)
            # Send heartbeat
            sio.emit('heartbeat', {
                'timestamp': datetime.now().isoformat(),
                'status': 'running'
            })

    except KeyboardInterrupt:
        print('\nShutting down...')
    except Exception as e:
        print(f'Error: {e}')
        # Emit error to gateway
        if sio.connected:
            sio.emit('python_error', {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
    finally:
        # Cleanup
        if api:
            print('Logging out from Shioaji...')
            api.logout()
        if sio.connected:
            sio.disconnect()
        print('Cleanup completed')

if __name__ == "__main__":
    main()
