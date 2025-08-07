from flask import Flask, request, render_template, Response
from threading import Lock

app = Flask(__name__)
sensor_data = {"temp": 0, "tds": 0, "ph": 0}
lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    global sensor_data
    if request.method == 'POST':
        data = request.get_json()
        print("Received JSON:", data)
        if data:
            with lock:
                sensor_data['temp'] = data.get('temperature', 0)
                sensor_data['tds'] = data.get('tds', 0)
                sensor_data['ph'] = data.get('ph', 0)
            return "OK", 200
        return "No JSON received", 400

    # If GET request
    with lock:
        text = f"temp={sensor_data['temp']}&ph={sensor_data['ph']}&tds={sensor_data['tds']}"
        return Response(text, mimetype='text/plain')
