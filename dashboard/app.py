# dashboard/app.py
import json
import os
from flask import Flask, render_template, jsonify

# Trỏ đúng thư mục templates
app = Flask(__name__, template_folder='templates')

HISTORY_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'reports', 'history'
)

def get_history_dir():
    path = os.path.abspath(HISTORY_DIR)
    os.makedirs(path, exist_ok=True)
    return path

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/runs")
def api_runs():
    path = os.path.join(get_history_dir(), "index.json")
    if not os.path.exists(path):
        return jsonify([])
    with open(path, encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route("/api/run/<run_id>")
def api_run_detail(run_id):
    path = os.path.join(get_history_dir(), f"{run_id}.json")
    if not os.path.exists(path):
        return jsonify({"error": "Not found"}), 404
    with open(path, encoding="utf-8") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    print("Dashboard: http://localhost:5000")
    app.run(debug=True, port=5000)