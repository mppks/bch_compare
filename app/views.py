from app import app
from flask import render_template
from app import bch

@app.route('/')
@app.route('/index')
def home():
    bch.get_datafile()
    return render_template('index.html', bch=bch.exch_data())
