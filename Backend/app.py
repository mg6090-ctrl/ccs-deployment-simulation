from flask import Flask, request, jsonify

app = Flask(__name__)

# This tells Flask: when someone visits http://127.0.0.1:5000/api/double, run this function
@app.route('/api/run-simulation', methods=['POST'])
def double_number():
    # 1. Grab the JSON data sent to us
    data = request.get_json()
    
    # 2. Extract specific numbers out of that data
    n_reps = data.get('n_reps', 100)
    sampling = data.get('sampling', 'coordinated')
    threshold_frac = data.get('THRESHOLD_FRAC', 0.5)
    base_rate = data.get('BASE_RATE', 0.05)

    # 3. Simulate math
    realized_volume = n_reps * 15.5 * (1 - base_rate)
    if threshold_frac > 0.6:
        collapse_rate = 0.45  # High thresholds cause more cluster collapses
    else:
        collapse_rate = 0.12
    
    # 4. Create final dictionary
    results = {
        "capture_survival_count": int(n_reps * (1 - collapse_rate)),
        "realized_volume_million_tonnes": round(realized_volume, 2),
        "total_collapse_rate": collapse_rate,
        "completion_time_years": 4.5 if sampling == 'coordinated' else 7.2,
        "status": "Success"
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)