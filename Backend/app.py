import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, jsonify
from flask_cors import CORS
import world_1_s1 as w1_1
import world_1_s2 as w1_2
import world_2 as w2
import scenario_analysis_w1_1 as w1_1_analysis
import scenario_analysis_w1_2 as w1_2_analysis
import scenario_analysis_w2 as w2_analysis
import coordinated_network_data as project_data
import coordinated_network_data as w2_project_data

DEFAULT_END_YEAR = 2045

app = Flask(__name__)

CORS(app)

def deployment_timeline(analysis_module, node_df, end_year):
    timeline = analysis_module.deployment_over_time(node_df, end_year)
    return {
        "year": timeline["year"].tolist(),
        "mean": timeline["mean"].tolist(),
        "p10": timeline["p10"].tolist(),
        "p90": timeline["p90"].tolist()
    }

@app.route('/api/run-model', methods = ['GET', 'POST'])
def run_model():
    data = request.get_json(silent = True) or {}

    scenarios = data.get("scenarios", [])
    end_year = data.get("end_year", DEFAULT_END_YEAR)

    results = {}

    # world 1.1 params
    if "world1_1" in scenarios:
        w1_1_params = data.get('world1_1', {})
        w1_1_n_reps = w1_1_params.get('n_reps', 10)
        w1_1_sampling = w1_1_params.get('sampling', True)
        w1_1_norm_sampling = w1_1_params.get('norm_sampling', False)
        w1_1_uni_sampling = w1_1_params.get('uni_sampling', False)
        w1_1_no_sampling = w1_1_params.get('no_sampling', False)
        w1_1_frac_split = w1_1_params.get('frac_split', w1_1.FRAC_SPLIT)
        w1_1_base_rate = w1_1_params.get('base_rate', w1_1.BASE_RATE)
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

        switch = False
        override = None

        if w1_1_sampling:
            switch = True
            override = "lognormal"
        elif w1_1_norm_sampling:
            switch = True
            override = "normal"
        elif w1_1_uni_sampling:
            switch = True
            override = "uniform"
        elif w1_1_no_sampling:
            switch = False
            override = None

        w1_1_results, w1_1_node_df = w1_1_analysis.monte_carlo(n_reps = w1_1_n_reps,
                       base_rate = w1_1_base_rate,
                       max_rate = max_rate,
                       cap_tolerance = cap_tolerance,
                       caps = w1_1_caps,
                       caps_vol = w1_1_caps_vol,
                       trans = w1_1_trans,
                       trans_vol = w1_1_trans_vol,
                       stor = w1_1_stor,
                       stor_vol = w1_1_stor_vol,
                       frac_split = w1_1_frac_split,
                       sampling = switch,
                       dist_override = override)

        w1_1_summary = w1_1.analyze_monte_carlo(w1_1_results)

        w1_1_bundle = {}
        w1_1_bundle["summary"] = w1_1_summary
        w1_1_bundle["reps"] = w1_1_results
        w1_1_bundle["deployment"] = deployment_timeline(w1_1_analysis, w1_1_node_df, end_year)

        results['world1_1'] = w1_1_bundle
    
    # world 1.2 params
    if "world1_2" in scenarios:
        w1_2_params = data.get('world1_2', {})
        w1_2_n_reps = w1_2_params.get('n_reps', 10)
        w1_2_sampling = w1_2_params.get('sampling', True)
        w1_2_norm_sampling = w1_2_params.get('norm_sampling', False)
        w1_2_uni_sampling = w1_2_params.get('uni_sampling', False)
        w1_2_no_sampling = w1_2_params.get('no_sampling', False)
        w1_2_frac_split = w1_2_params.get('frac_split', w1_2.FRAC_SPLIT)
        w1_2_base_rate = w1_2_params.get('base_rate', w1_2.BASE_RATE)
        w1_2_caps = w1_2_params.get('caps', project_data.CAPTURE)
        w1_2_caps_vol = w1_2_params.get('caps_vol', project_data.CAPTURE_VOLUMES)
        w1_2_trans = w1_2_params.get('trans', project_data.TRANSPORT)
        w1_2_trans_vol = w1_2_params.get('trans_vol', project_data.TRANSPORT_VOLUMES)
        w1_2_stor = w1_2_params.get('stor', project_data.STORAGE)
        w1_2_stor_vol = w1_2_params.get('stor_vol', project_data.STORAGE_VOLUMES)
        max_rate = w1_2_params.get('s1_max_rate', w1_2.MAX_RATE)
        cap_tolerance = w1_2_params.get('s1_cap_tol', w1_2.CAPTURE_TOLERANCE)
        w1_2_frac_split_approval = w1_2_params.get('frac_split_app', w1_2.FRAC_SPLIT[0])
        w1_2_hammock_threshold = w1_2_params.get('hammock_threshold', w1_2.HAMMOCK_THRESHOLD)

        if cap_tolerance <= 0:
            return jsonify({"error": "capture tolerance must be greater than 0"}), 400

        w1_2_frac_split = [w1_2_frac_split_approval, 1-w1_2_frac_split_approval]

        switch = False
        override = None

        if w1_2_sampling:
            switch = True
            override = "lognormal"
        elif w1_2_norm_sampling:
            switch = True
            override = "normal"
        elif w1_2_uni_sampling:
            switch = True
            override = "uniform"
        elif w1_2_no_sampling:
            switch = False
            override = None

        w1_2_results, w1_2_node_df = w1_2_analysis.monte_carlo(n_reps = w1_2_n_reps,
                       base_rate = w1_2_base_rate,
                       max_rate = max_rate,
                       cap_tolerance = cap_tolerance,
                       caps = w1_2_caps,
                       caps_vol = w1_2_caps_vol,
                       trans = w1_2_trans,
                       trans_vol = w1_2_trans_vol,
                       stor = w1_2_stor,
                       stor_vol = w1_2_stor_vol,
                       frac_split = w1_2_frac_split,
                       sampling = switch,
                       hammock_threshold = w1_2_hammock_threshold,
                       dist_override = override)

        w1_2_summary = w1_2.analyze_monte_carlo(w1_2_results)

        w1_2_bundle = {}
        w1_2_bundle["summary"] = w1_2_summary
        w1_2_bundle["reps"] = w1_2_results
        w1_2_bundle["deployment"] = deployment_timeline(w1_2_analysis, w1_2_node_df, end_year)

        results['world1_2'] = w1_2_bundle

    # world 2 params
    if "world2" in scenarios:
        w2_params = data.get('world2', {})
        w2_n_reps = w2_params.get('n_reps', 10)
        w2_sampling = w2_params.get('sampling', True)
        w2_norm_sampling = w2_params.get('norm_sampling', False)
        w2_uni_sampling = w2_params.get('uni_sampling', False)
        w2_no_sampling = w2_params.get('no_sampling', False)
        w2_base_rate = w2_params.get('base_rate', w2.BASE_RATE)
        w2_caps = w2_params.get('caps', w2_project_data.CAPTURE)
        w2_caps_vol = w2_params.get('caps_vol', w2_project_data.CAPTURE_VOLUMES)
        w2_trans = w2_params.get('trans', w2_project_data.TRANSPORT)
        w2_trans_vol = w2_params.get('trans_vol', w2_project_data.TRANSPORT_VOLUMES)
        w2_stor = w2_params.get('stor', w2_project_data.STORAGE)
        w2_stor_vol = w2_params.get('stor_vol', w2_project_data.STORAGE_VOLUMES)
        w2_threshold_frac = w2_params.get('threshold_frac', w2.THRESHOLD_FRAC)
        w2_max = w2_params.get('max_rate', w2.MAX_RATE)
        w2_cap_tol = w2_params.get('cap_tol', w2.CAPTURE_TOLERANCE)
        w2_trans_tol = w2_params.get('trans_tol', w2.TRANSPORT_TOLERANCE)
        w2_stor_tol = w2_params.get('stor_tol', w2.STORAGE_TOLERANCE)
        w2_late_penalty = w2_params.get('late_penalty', w2.LATE_PENALTY)

        if w2_cap_tol <= 0:
            return jsonify({"error": "capture tolerance must be greater than 0"}), 400
        if w2_trans_tol <= 0:
            return jsonify({"error": "transport tolerance must be greater than 0"}), 400
        if w2_stor_tol <= 0:
            return jsonify({"error": "storage tolerance must be greater than 0"}), 400

        switch = False
        override = None

        if w2_sampling:
            switch = True
            override = "lognormal"
        elif w2_norm_sampling:
            switch = True
            override = "normal"
        elif w2_uni_sampling:
            switch = True
            override = "uniform"
        elif w2_no_sampling:
            switch = False
            override = None

        w2_results, w2_node_df = w2_analysis.monte_carlo(n_reps = w2_n_reps,
                       base_rate = w2_base_rate,
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
                       sampling = switch,
                       dist_override=override,
                       late_penalty=w2_late_penalty)

        w2_summary = w2.analyze_monte_carlo(w2_results)

        w2_bundle = {}
        w2_bundle["summary"] = w2_summary
        w2_bundle["reps"] = w2_results
        w2_bundle["deployment"] = deployment_timeline(w2_analysis, w2_node_df, end_year)

        results['world2'] = w2_bundle

    return jsonify(results)

@app.route('/api/download-results')
def download():
    return 

if __name__ == '__main__':
    app.run(debug=True, port=5000)