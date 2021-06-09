from flask import Flask, jsonify, request, render_template
from flask_restful import Api
#from apis.config import SECRET_KEY
#from apis import User
import sys
sys.path.append("/home/pi/pfoserver2/apis")
from config import SECRET_KEY, MONGO_URI
from airchat import User

app = Flask(__name__)
#app.config['SECRET_KEY'] = SECRET_KEY
app.config["MONGO_CONNECT"] = False

api = Api(app)
api.add_resource(User, "/user/", "/user/<id>")

@app.route("/")
def index():
    return "<html><body><h1>Test site running under Flask :) - Piero!</h1></body></html>"
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
