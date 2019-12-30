from flask import Flask

import os
import urllib3
import json
import logging.config

# Configure Flask app logging
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

conf = {
    'SQLALCHEMY_TRACK_MODIFICATIONS': False, \
    'SQLALCHEMY_ECHO': False, \
}

conf.update({k[4:]: v for k, v in os.environ.items() if k.startswith('APP_')})

for key, val in conf.items():
    app.logger.info('Setting configuration {}={}'.format(key, val))
    app.config[key] = val

import tldr.views
import tldr.api
import tldr.model
import tldr.login
