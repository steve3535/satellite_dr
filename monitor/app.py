from flask import Flask, request
import requests  
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)
#@app.route("/monitor")
def monitor():
    url="http://127.0.0.1:9001/status/"
    res=requests.get(url)
    
    res.json()

if __name__ == "__main__":
    #app.run(host="0.0.0.0",debug=True,port=9002)
    monitor()
