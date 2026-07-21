from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import sys
import main

app = Flask(__name__)
# Initialize SocketIO with async_mode set to threading since we are running Ultron in a normal thread
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

def ui_callback(event_name, data):
    """Callback passed to Ultron's main loop to push events to the web UI."""
    socketio.emit(event_name, data)

@app.route('/')
def index():
    return render_template('index.html')

def start_ultron_thread():
    # We run the heavy voice loop in a background thread so it doesn't block the web server
    main.run_ultron(ui_callback=ui_callback)

if __name__ == '__main__':
    print("[*] Starting Ultron Web UI on http://127.0.0.1:5000")
    
    # Start Ultron
    ultron_thread = threading.Thread(target=start_ultron_thread, daemon=True)
    ultron_thread.start()
    
    # Start the Web Server
    socketio.run(app, host='127.0.0.1', port=5000, debug=False, use_reloader=False)
