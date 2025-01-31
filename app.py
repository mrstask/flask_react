from flask import Flask, send_file
from flask_sock import Sock
from flask_cors import CORS
import json
import random
import time

app = Flask(__name__)
CORS(app, resources={r"/ws/*": {"origins": "*"}})
sock = Sock(app)

def generate_item():
    types = ['type1', 'type2', 'type3']
    return {
        'name': f'Item {random.randint(1, 100)}',
        'value': random.randint(0, 1000),
        'type': random.choice(types)
    }

def generate_data():
    return {
        'items': [generate_item() for _ in range(9)]
    }

@app.route('/')
def home():
    return send_file('index.html')

@sock.route('/ws')
def streaming(ws):
    while True:
        try:
            data = generate_data()
            ws.send(json.dumps(data))
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
