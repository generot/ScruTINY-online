async function get(route) {
    let resp = await fetch(route, {
        method: "GET",
        mode: "no-cors"
    });

    return resp.json();
}

async function post(route, data) {
    let resp = await fetch(route, {
        method: "POST",
        mode: "no-cors",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    return resp.json();
}