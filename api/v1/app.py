#!/usr/bin/python3
'''main app module'''

from os import getenv
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv("HBNB_API_HOST", default="0.0.0.0")
port = int(getenv("HBNB_API_PORT", default=5000))

@app.teardown_appcontext
def close(exc):
    '''close the storage session'''
    storage.close()

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
