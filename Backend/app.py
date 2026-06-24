from models import scenario_1_final_refactored as s1
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import scenario_2_final_refactored as s2

app = Flask(__name__)

CORS(app)

@app.route('/api/run-s1', methods=['GET', 'POST'])
def double_number():
    data = request.get_json(silent = True) or {}
    
    n_reps = data.get('n_reps', 10)
    sampling = data.get('sampling', True)
    frac_split = data.get('frac_split', s1.FRAC_SPLIT)
    base_rate = data.get('base_rate', s1.BASE_RATE)
    replication_seed = data.get('replication_seed', 0)
    clusters = data.get('clusters', s1.CLUSTERS)
    caps = data.get('caps', s1.CAPTURE)
    caps_vol = data.get('caps_vol', s1.CAPTURE_VOLUMES)
    trans = data.get('trans', s1.TRANSPORT)
    trans_vol = data.get('trans_vol', s1.TRANSPORT_VOLUMES)
    stor = data.get('stor', s1.STORAGE)
    stor_vol = data.get('stor_vol', s1.STORAGE_VOLUMES)
    
    results = s1.monte_carlo(n_reps = n_reps, 
                       base_rate = base_rate, 
                       replication_seed = replication_seed, 
                       clusters = clusters, 
                       caps = caps, 
                       caps_vol = caps_vol, 
                       trans = trans, 
                       trans_vol = trans_vol, 
                       stor = stor, 
                       stor_vol = stor_vol, 
                       frac_split = frac_split, 
                       sampling = sampling)
    
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