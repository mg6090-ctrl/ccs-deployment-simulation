from models import scenario_1_final_refactored as s1
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import scenario_2_final_refactored as s2

app = Flask(__name__)

CORS(app)

@app.route('/api/run-s1', methods=['GET', 'POST'])
def run_s1():
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

@app.route('/api/run-model', methods = ['GET', 'POST'])
def run_model():
    data = request.get_json(silent = True) or {}

    scenarios = data.get("scenarios", [])

    results = {}

    # scenario 1 params
    if "scenario1" in scenarios:
        s1_params = data.get('scenario1', {})
        s1_n_reps = s1_params.get('n_reps', 10)
        s1_sampling = s1_params.get('sampling', True)
        s1_frac_split = s1_params.get('frac_split', s1.FRAC_SPLIT)
        s1_base_rate = s1_params.get('base_rate', s1.BASE_RATE)
        s1_clusters = s1_params.get('clusters', s1.CLUSTERS)
        s1_caps = s1_params.get('caps', s1.CAPTURE)
        s1_caps_vol = s1_params.get('caps_vol', s1.CAPTURE_VOLUMES)
        s1_trans = s1_params.get('trans', s1.TRANSPORT)
        s1_trans_vol = s1_params.get('trans_vol', s1.TRANSPORT_VOLUMES)
        s1_stor = s1_params.get('stor', s1.STORAGE)
        s1_stor_vol = s1_params.get('stor_vol', s1.STORAGE_VOLUMES)

        s1_results = s1.monte_carlo(n_reps = s1_n_reps, 
                       base_rate = s1_base_rate, 
                       clusters = s1_clusters, 
                       caps = s1_caps, 
                       caps_vol = s1_caps_vol, 
                       trans = s1_trans, 
                       trans_vol = s1_trans_vol, 
                       stor = s1_stor, 
                       stor_vol = s1_stor_vol, 
                       frac_split = s1_frac_split, 
                       sampling = s1_sampling)
        
        results['scenario1'] = s1_results
        
    if "scenario2" in scenarios:
        s2_params = data.get('scenario2', {})
        s2_n_reps = s2_params.get('n_reps', 10)
        s2_sampling = s2_params.get('sampling', True)
        s2_base_rate = s2_params.get('base_rate', s2.BASE_RATE)
        s2_clusters = s2_params.get('clusters', s2.CLUSTERS)
        s2_caps = s2_params.get('caps', s2.CAPTURE)
        s2_caps_vol = s2_params.get('caps_vol', s2.CAPTURE_VOLUMES)
        s2_trans = s2_params.get('trans', s2.TRANSPORT)
        s2_trans_vol = s2_params.get('trans_vol', s2.TRANSPORT_VOLUMES)
        s2_stor = s2_params.get('stor', s2.STORAGE)
        s2_stor_vol = s2_params.get('stor_vol', s2.STORAGE_VOLUMES)
        s2_threshold_frac = s2_params.get('threshold_frac', s2.THRESHOLD_FRAC)
        s2_max = s2_params.get('max_rate', s2.MAX_RATE)
        s2_cap_tol = s2_params.get('cap_tol', s2.CAPTURE_TOLERANCE)
        s2_trans_tol = s2_params.get('trans_tol', s2.TRANSPORT_TOLERANCE)
        s2_stor_tol = s2_params.get('stor_tol', s2.STORAGE_TOLERANCE)

        s2_results = s2.monte_carlo(n_reps = s2_n_reps, 
                       base_rate = s2_base_rate, 
                       clusters = s2_clusters, 
                       capture_durations = s2_caps, 
                       capture_volumes = s2_caps_vol, 
                       transport_durations = s2_trans, 
                       transport_volumes = s2_trans_vol, 
                       storage_durations = s2_stor, 
                       storage_volumes = s2_stor_vol,
                       threshold_frac = s2_threshold_frac,
                       max_rate = s2_max,
                       capture_tolerance = s2_cap_tol,
                       transport_tolerance = s2_trans_tol,
                       storage_tolerance = s2_stor_tol,
                       sampling = s2_sampling)
        
        results['scenario2'] = s2_results

    return jsonify(results)

@app.route('/api/download-results')
def download():
    return 

if __name__ == '__main__':
    app.run(debug=True, port=5000)