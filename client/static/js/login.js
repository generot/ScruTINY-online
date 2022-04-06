async function login() {
    let inp = document.querySelector("#user");
    let remainLogged = document.querySelector("#check");

    let uid = inp.value;
    let user = await get(`/verifyUser?uid=${uid}`);

    if(user.exists) {
        if(remainLogged.checked) {
            window.localStorage.setItem("user-id", uid);
        }

        window.location.replace(`/user/${uid}`);
    } else {
        alert("User does not exist? Please register and try again!");
    }
}

async function signup() {
    let name_ = document.querySelector("#user-sign-up");
    let val = name_.value;

    let resp = await post("/registerUser", { name: val });

    if(resp.status == "OK") {
        alert(`Sign up successful! Your unique ID(This will only be shown to you once. Copy it!): ${resp.uid}`);
        window.location.reload();
    } else {
        alert("Sign up unsuccessful. Possible server failure.");
    }
}

function logout() {
    let userId = window.localStorage.getItem("user-id");

    if(userId) {
        window.localStorage.removeItem("user-id");
    }

    window.location.replace("/");
}