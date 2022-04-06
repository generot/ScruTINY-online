import * as SocketIO from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js"

const serverSocket = SocketIO.io();
const popupDiv = document.getElementById("popup-div");

function makeContainer(msg) {
    let newElem = document.createElement("input");

    newElem.setAttribute("class", "ds-message");
    newElem.setAttribute("value", msg);
    newElem.readOnly = true;

    return newElem;
}

async function setup() {
    let route = window.location.pathname + "/getData";
    let allDisturbances = await get(route);

    if(allDisturbances.status == "OK") {
        console.log(allDisturbances);
        for(let i of allDisturbances.data) {
            let msg = `Disturbance: ${i} cm away from sensor.`;
            let render = makeContainer(msg);

            popupDiv.appendChild(render);
        }
    }
}

serverSocket.on("connect", () => {
    let uri = window.location.pathname;

    serverSocket.emit("connected-ids", { _uri: uri, _id: serverSocket.id });
})

serverSocket.on("post-data", (data) => {    
    let msg = `Disturbance: ${data["data"]} cm away from sensor.`;
    let elem = makeContainer(msg);

    popupDiv.appendChild(elem);
});

setup();