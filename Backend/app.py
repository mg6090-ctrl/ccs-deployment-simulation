from flask import Flask, request, jsonify
from flask_cors import CORS
import world_1_s1 as w1_1
import world_1_s2 as w1_2
import world_2 as w2
import project_data as project_data

app = Flask(__name__)

CORS(app)

@app.route('/api/run-model', methods = ['GET', 'POST'])
def run_model():
    data = request.get_json(silent = True) or {}

    scenarios = data.get("scenarios", [])

    results = {}

    # world 1.1 params
    if "world1_1" in scenarios:
        w1_1_params = data.get('scenario1', {})

        w1_1_n_reps = w1_1_params.get('n_reps', 10)
        w1_1_sampling = w1_1_params.get('sampling', True)
        w1_1_frac_split = w1_1_params.get('frac_split', w1_1.FRAC_SPLIT)
        w1_1_base_rate = w1_1_params.get('base_rate', w1_1.BASE_RATE)
        w1_1_clusters = w1_1_params.get('clusters', project_data.CLUSTERS)
        w1_1_caps = w1_1_params.get('caps', project_data.CAPTURE)
        w1_1_caps_vol = w1_1_params.get('caps_vol', project_data.CAPTURE_VOLUMES)
        w1_1_trans = w1_1_params.get('trans', project_data.TRANSPORT)
        w1_1_trans_vol = w1_1_params.get('trans_vol', project_data.TRANSPORT_VOLUMES)
        w1_1_stor = w1_1_params.get('stor', project_data.STORAGE)
        w1_1_stor_vol = w1_1_params.get('stor_vol', project_data.STORAGE_VOLUMES)
        max_rate = w1_1_params.get('s1_max_rate', w1_1.MAX_RATE)
        cap_tolerance = w1_1_params.get('s1_cap_tol', w1_1.CAPTURE_TOLERANCE)
        w1_1_frac_split_approval = w1_1_params.get('frac_split_app', w1_1.FRAC_SPLIT[0])

        if cap_tolerance <= 0:
            return jsonify({"error": "capture tolerance must be greater than 0"}), 400

        w1_1_frac_split = [w1_1_frac_split_approval, 1-w1_1_frac_split_approval]

        w1_1_results = w1_1.monte_carlo(n_reps = w1_1_n_reps, 
                       base_rate = w1_1_base_rate, 
                       max_rate = max_rate,
                       cap_tolerance = cap_tolerance,
                       clusters = w1_1_clusters, 
                       caps = w1_1_caps, 
                       caps_vol = w1_1_caps_vol,
                       trans = w1_1_trans, 
                       trans_vol = w1_1_trans_vol,
                       stor = w1_1_stor, 
                       stor_vol = w1_1_stor_vol, 
                       frac_split = w1_1_frac_split, 
                       sampling = w1_1_sampling)

        w1_1_summary = w1_1.analyze_monte_carlo(w1_1_results)

        w1_1_bundle = {}
        w1_1_bundle["summary"] = w1_1_summary
        w1_1_bundle["reps"] = w1_1_results
        
        results['scenario1'] = w1_1_bundle
    
    # world 1.2 params

    # world 2 params
    if "world2" in scenarios:
        w2_params = data.get('scenario2', {})
        w2_n_reps = w2_params.get('n_reps', 10)
        w2_sampling = w2_params.get('sampling', True)
        w2_base_rate = w2_params.get('base_rate', w2.BASE_RATE)
        w2_clusters = w2_params.get('clusters', project_data.CLUSTERS)
        w2_caps = w2_params.get('caps', project_data.CAPTURE)
        w2_caps_vol = w2_params.get('caps_vol', project_data.CAPTURE_VOLUMES)
        w2_trans = w2_params.get('trans', project_data.TRANSPORT)
        w2_trans_vol = w2_params.get('trans_vol', project_data.TRANSPORT_VOLUMES)
        w2_stor = w2_params.get('stor', project_data.STORAGE)
        w2_stor_vol = w2_params.get('stor_vol', project_data.STORAGE_VOLUMES)
        w2_threshold_frac = w2_params.get('threshold_frac', w2.THRESHOLD_FRAC)
        w2_max = w2_params.get('max_rate', w2.MAX_RATE)
        w2_cap_tol = w2_params.get('cap_tol', w2.CAPTURE_TOLERANCE)
        w2_trans_tol = w2_params.get('trans_tol', w2.TRANSPORT_TOLERANCE)
        w2_stor_tol = w2_params.get('stor_tol', w2.STORAGE_TOLERANCE)

        if w2_cap_tol <= 0:
            return jsonify({"error": "capture tolerance must be greater than 0"}), 400
        if w2_trans_tol <= 0:
            return jsonify({"error": "transport tolerance must be greater than 0"}), 400
        if w2_stor_tol <= 0:
            return jsonify({"error": "storage tolerance must be greater than 0"}), 400

        w2_results = w2.monte_carlo(n_reps = w2_n_reps, 
                       base_rate = w2_base_rate, 
                       clusters = w2_clusters, 
                       capture_durations = w2_caps, 
                       capture_volumes = w2_caps_vol, 
                       transport_durations = w2_trans, 
                       transport_volumes = w2_trans_vol, 
                       storage_durations = w2_stor, 
                       storage_volumes = w2_stor_vol,
                       threshold_frac = w2_threshold_frac,
                       max_rate = w2_max,
                       capture_tolerance = w2_cap_tol,
                       transport_tolerance = w2_trans_tol,
                       storage_tolerance = w2_stor_tol,
                       sampling = w2_sampling)
        
        w2_summary = w2.analyze_monte_carlo(w2_results)
        
        w2_bundle = {}
        w2_bundle["summary"] = w2_summary
        w2_bundle["reps"] = w2_results

        results['scenario2'] = w2_bundle

    return jsonify(results)

@app.route('/api/download-results')
def download():
    return 

if __name__ == '__main__':
    app.run(debug=True, port=5000)