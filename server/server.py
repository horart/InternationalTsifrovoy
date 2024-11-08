import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
ctr = 0
# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def api(path):
    return path


if __name__ == '__main__':
    app.run()