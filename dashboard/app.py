from flask import Flask, render_template
from flask_socketio import SocketIO
import logging

import os

# Mute Flask/Werkzeug default logging so it doesn't clutter the terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__,
            template_folder=root_dir,
            static_folder=root_dir,
            static_url_path='')
app.config['SECRET_KEY'] = 'cybersecurity_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/')
def index():
    return render_template('index.html')

def start_dashboard(port=5000):
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
