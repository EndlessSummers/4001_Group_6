function myOnBlur(component) {
    // change style when an input field lose focus
    // do something here
    if (component === "username") {
        // email validation
        // do something here
    } else if (component === "password") {
        // password validation
        // do something here
    } else if (component === "repeat") {
        // repeat password validation
        // do something here
    }
}

function myOnFocus() {
    // change style when an input field is focused
    // do something here
}

function myOnSubmit(component) {
    // submit validation and submit redirection
    // do something here
    if (component === "email") {
        window.location.href="./email.html";
    } else if (component === "info") {
        window.location.href="./success.html";
    }
}


function togglePasswordView(e) {
    // change the visibility of password;
    // do something here
    e.preventDefault();

    passwd = document.getElementById("Password");
    repeat = document.getElementById("Repeat");
    const type = passwd.getAttribute("type") === "password" ? "text" : "password";
    passwd.setAttribute("type", type);
    repeat.setAttribute("type", type);
}