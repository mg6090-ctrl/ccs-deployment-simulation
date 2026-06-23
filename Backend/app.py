from flask import Flask, request, jsonify
from models import scenario_1_final_copy, scenario_2_final_copy
from pathlib import Path
import os
import json
import copy
import io
import base64
from typing import Dict, List, Tuple, Optional
import pandas as pd
import random 

app = Flask(__name__)

@app.route('/api/defaults', methods=['GET'])
def double_number():
    data = request.get_json()
    
    n_reps = data.get('n_reps', 100)
    sampling = data.get('sampling', 'coordinated')
    threshold_frac = data.get('THRESHOLD_FRAC', 0.5)
    base_rate = data.get('BASE_RATE', 0.05)

    realized_volume = n_reps * 15.5 * (1 - base_rate)
    if threshold_frac > 0.6:
        collapse_rate = 0.45
    else:
        collapse_rate = 0.12
    
    results = {
        "capture_survival_count": int(n_reps * (1 - collapse_rate)),
        "realized_volume_million_tonnes": round(realized_volume, 2),
        "total_collapse_rate": collapse_rate,
        "completion_time_years": 4.5 if sampling == 'coordinated' else 7.2,
        "status": "Success"
    }

    return jsonify(results)

@app.route('/api/run-model')
def run_model():
    data = request.get_json()
    results = {}
    return jsonify(results)

@app.route('/api/download-results')
def download():
    return 

if __name__ == '__main__':
    app.run(debug=True, port=5000)