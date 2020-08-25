from app import app
from flask import render_template, jsonify
from app.bestchange import Bestchange
import json

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/api/bc_rates', methods=['GET'])
def api_bc_rates():
    bestchange = Bestchange('tmp')
    rates = bestchange.get_rates()
    return jsonify({'exch': rates[0:11]})
    #with open(bestchange.tmp_dir + '/rates.json', 'w', encoding='utf-8') as outf:
    #    json.dump({'exch': rates}, outf, ensure_ascii=False, indent=4)

    #return {'result': 'true'}
