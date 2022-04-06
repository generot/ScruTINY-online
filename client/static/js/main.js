import * as SocketIO from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js"

const serverSocket = SocketIO.io();
const popupDiv = document.getElementById("popup-div");

serverSocket.on("connect", () => {
    let uri = window.location.href;

    serverSocket.emit("connected-ids", { data: { _uri: uri, _id: serverSocket.id } });
})

serverSocket.on("post-data", (data) => {    
    let newElem = document.createElement("input");

    newElem.setAttribute("class", "ds-message");
    newElem.setAttribute("value", data["data"]);
    newElem.readOnly = true;

    popupDiv.appendChild(newElem);
});