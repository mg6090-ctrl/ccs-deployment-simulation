from models import scenario_1_final_refactored as s1
from flask import Flask, request, jsonify
from models import scenario_2_final_refactored as s2

app = Flask(__name__)

@app.route('/api/run-s1', methods=['GET'])
def double_number():
    data = request.get_json()
    
    n_reps = data.get('n_reps')
    sampling = data.get('sampling')
    frac_split = data.get('frac_split')
    base_rate = data.get('base_rate')
    replication_seed = data.get('replication_seed')
    clusters = data.get('clusters')
    caps = data.get('caps')
    caps_vol = data.get('caps_vol')
    trans = data.get('trans')
    trans_vol = data.get('trans_vol')
    stor = data.get('stor')
    stor_vol = data.get('stor_vol')
    
    results = {
        s1.monte_carlo(n_reps = n_reps, 
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