import os

from flask import *
from flask_socketio import SocketIO

TEMPLATE_FOLDER_PATH = os.path.abspath("./client/html")
STATIC_FOLDER_PATH = os.path.abspath("./client/static")

server = Flask(__name__, static_folder=STATIC_FOLDER_PATH, template_folder=TEMPLATE_FOLDER_PATH)
socket = SocketIO(server)

@server.route("/")
def main_page():
    return render_template("index.html")

@server.route("/postData", methods=["POST"])
def handle_post():
    res = request.get_data(as_text=True)

    socket.emit("post-data", { "data": res })

    return "\r\nSEND OK\r\n"