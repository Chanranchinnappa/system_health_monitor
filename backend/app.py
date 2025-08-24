# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS module
import json
import time
from threading import Lock
import os  # Import the os module

# Set the FLASK_APP environment variable programmatically
if __name__ == "__main__":
    os.environ['FLASK_APP'] = 'app.py'

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simple in-memory storage with a lock for thread safety
db_lock = Lock()
machines = {}

# Load initial data if available
try:
    with open("machines.json", "r") as f:
        machines = json.load(f)
except FileNotFoundError:
    pass

def save_data():
    """Saves the current state to a file."""
    with db_lock:
        with open("machines.json", "w") as f:
            json.dump(machines, f)

# API Endpoints
@app.route("/api/v1/health", methods=["POST"])
def receive_health_data():
    """Accepts system data from the utility."""
    data = request.json
    if not data:
        return jsonify({"message": "Invalid data"}), 400
    
    machine_id = data.get("machine_id")
    if not machine_id:
        return jsonify({"message": "Missing machine_id"}), 400
        
    data["last_check_in"] = int(time.time())
    
    with db_lock:
        machines[machine_id] = data
        save_data()
        
    return jsonify({"message": "Data received successfully"}), 200

@app.route("/api/v1/machines", methods=["GET"])
def list_machines():
    """Lists all machines and their latest status."""
    return jsonify(list(machines.values())), 200

# Optional: CSV export endpoint
@app.route("/api/v1/export", methods=["GET"])
def export_csv():
    # This is a placeholder. You'd generate a CSV string here.
    return "CSV Export Placeholder", 200

if __name__ == "__main__":
    app.run(debug=True)