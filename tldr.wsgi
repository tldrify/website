import sys
import logging

sys.path.insert(0, '/var/www/tldrify.com')
logging.basicConfig(stream=sys.stderr)

from tldr import app as application

