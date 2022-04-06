import os
import json
import server.database as scrutiny_db

from flask import *
from flask_socketio import SocketIO

TEMPLATE_FOLDER_PATH = os.path.abspath("./client/html")
STATIC_FOLDER_PATH = os.path.abspath("./client/static")

server = Flask(__name__, static_folder=STATIC_FOLDER_PATH, template_folder=TEMPLATE_FOLDER_PATH)
socket = SocketIO(server)

all_clients = {}

@server.route("/")
def main_page():
    return render_template("index.html")

@server.route("/user/<uid>")
def load_user(uid):
    return render_template("view.html")

@server.route("/login")
def login():
    return render_template("login.html")

@server.route("/registerUser", methods=["POST"])
def signup():
    resp = request.get_data(as_text=True)
    obj = json.loads(resp)

    return scrutiny_db.register_user(obj)

@server.route("/verifyUser", methods=["GET"])
def verify():
    res = request.args.to_dict()
    return scrutiny_db.verify_user(res["uid"])

@server.route("/user/<uid>/getData", methods=["GET"])
def get_data(uid):
    data = scrutiny_db.get_data_from_db(uid)
    return data

@server.route("/postData/<uid>", methods=["POST"])
def handle_post2(uid):
    res = request.get_data(as_text=True)
    path = f"/user/{uid}"

    socket.emit("post-data", { "data": res }, to=f"{all_clients[path]}")
    scrutiny_db.add_data_to_db(uid, res)

    return "\r\nSEND OK\r\n"

@server.route("/postData", methods=["POST"])
def handle_post():
    res = request.get_data(as_text=True)

    socket.emit("post-data", { "data": res })

    return "\r\nSEND OK\r\n"

@socket.on("connected-ids")
def on_connect(data):
    conn_uri = data["_uri"]
    conn_socket_id = data["_id"]

    all_clients[conn_uri] = conn_socket_id