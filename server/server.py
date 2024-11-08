import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
ctr = 0
# Serve React App
@app.route('/api')
def api():
    global ctr
    ctr += 1
    print(ctr)
    return str(ctr)


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)