from flask import Flask

app = Flask(__name__, static_url_path='')
app.config['JSON_AS_ASCII'] = False
from app import views
