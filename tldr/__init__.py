from flask import Flask

import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONF_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), '.config', 'app.json')
with open(CONF_FILE, 'r') as f:
    conf = json.load(f)

app = Flask(__name__)
for key, val in conf.items():
    app.config[key] = val
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://tldr:tldr@127.0.0.1/tldr?charset=utf8'
#app.config['SQLALCHEMY_ECHO'] = True

import tldr.views
import tldr.api
import tldr.model
import tldr.login
