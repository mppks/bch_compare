from app import app
from flask import render_template, jsonify
from app import bch


@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/api/bch', methods=['GET'])
def api_bch():
    bch.get_datafile()
    data = bch.exch_data()
    return jsonify({'exch': data[0:11]})