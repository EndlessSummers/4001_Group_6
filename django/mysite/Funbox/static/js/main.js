function myOnSubmit(e, info) {
    var state;
    if (info === "login") {
        state = validate_email() && validate_passwd();
    } else if (info === "email") {
        state = validate_email();
    } else if (info === "register") {
        state = validate_email() && validate_passwd() && validate_repeat();
    } else if (info === "repeat") {
        state = validate_passwd() && validate_repeat();
    } else if (info === "change") {
        state = validate_change() && validate_passwd() && validate_repeat();
    } else if (info === "cancel") {
        state = true;
    }

    if (!state) {
        console.log("INVALID INPUT");
        e.preventDefault;
        return false;
    } else {
        console.log("VALID INPUT");
        return true;
    }
}

function validate_email() {
    let email = document.forms["form"]["email"].value;
    let p_email = document.getElementById("email_e");
    // Question: email should end with @link.cuhk.edu.cn?
    let reg_email = /^[a-zA-Z0-9][\w\-]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$/
    if (!reg_email.test(email)) {
        console.log("ERROR: EMAIL: INCORRECT EMAIL FORMAT");
        p_email.innerHTML = "incorrect email format";
        p_email.removeAttribute('hidden');
        return false;
    } else {
        // validation passed
        // do something here
        console.log("VAILD EMAIL");
        p_email.innerHTML = "some error happened";
        p_email.setAttribute('hidden', 'true');
    }
    return true;
}

function validate_change() {
    let oldPasswd = document.forms["form"]["oldpassword"].value;
    let passwd = document.forms["form"]["password"].value;
    let p_passwd = document.getElementById("oldpassword_e");
    if (oldPasswd == passwd) {
        console.log("ERROR: CHANGE: MATCH");
        p_passwd.innerHTML = "The new password is the same as the original password";
        p_passwd.removeAttribute('hidden');
        return false;
    } else {
        // validation passed
        // do something here
        console.log("DIFFERENT NEW PASSWORD");
        p_passwd.innerHTML = "some error happened";
        p_passwd.setAttribute('hidden', 'true');
    }
    return true;
}

function validate_passwd() {
    let passwd = document.forms["form"]["password"].value;
    let p_passwd = document.getElementById("password_e");
    if (passwd.length != passwd.trim().length) {
        console.log("ERROR: PASSWORD: LEADING/TAILING SPACE");
        p_passwd.innerHTML = "password should contain no leading or tailing spaces";
        p_passwd.removeAttribute('hidden');
        return false;
    } else if (passwd.length < 8 || passwd.length > 16) {
        console.log("ERROR: PASSWORD: LENGTH");
        p_passwd.innerHTML = "password must contain 8-16 (included) characters";
        p_passwd.removeAttribute('hidden');
        return false;
    } else if (!(/^.*[A-Za-z].*$/.test(passwd) && /^.*[0-9].*$/.test(passwd))) {
        console.log("ERROR: PASSWORD: FORMAT");
        p_passwd.innerHTML = "password must contain at least one letter and one digit";
        p_passwd.removeAttribute('hidden');
        return false;
    } else {
        console.log("VALID PASSWORD");
        p_passwd.innerHTML = "some error happened";
        p_passwd.setAttribute('hidden', 'true');
    }
    return true;
}

function validate_repeat() {
    let passwd = document.forms["form"]["password"].value;
    let repeat = document.forms["form"]["repeat"].value;
    let p_repeat = document.getElementById("repeat_e");
    if (passwd != repeat) {
        console.log("ERROR: REPEAT: NOT MATCH");
        p_repeat.innerHTML = "password did not match";
        p_repeat.removeAttribute('hidden');
        return false;
    } else {
        // validation passed
        // do something here
        console.log("DIFFERENT NEW PASSWORD");
        p_repeat.innerHTML = "some error happened";
        p_repeat.setAttribute('hidden', 'true');
    }
    return true;
}

function togglePasswordView(e, info) {
    // change the visibility of password;
    e.preventDefault();

    passwd = document.getElementById("Password");
    const type = passwd.getAttribute("type") === "password" ? "text" : "password";
    passwd.setAttribute("type", type);
    if (info === "repeat") {
        repeat = document.getElementById("Repeat");
        repeat.setAttribute("type", type);
    } else if (info === "triple") {
        repeat = document.getElementById("Repeat");
        oldpasswd = document.getElementById("OldPassword");
        repeat.setAttribute("type", type);
        oldpasswd.setAttribute("type", type);
    }
}
