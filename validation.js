function changed() {
    let para = document.getElementsByTagName("p");
    para[0].innerHTML = "input username cannot be empty";
    para[0].style.visibility = "visible";
}

function validate(component) {
    if (component === "username") { // username validation
        let line = document.forms["register"]["username"].value;
        let para = document.getElementById("username_e");
        if (line.trim() == "") {
            console.log("ERROR: USERNAME: EMPTY")
            para.innerHTML = "username cannot be empty";
            para.removeAttribute('hidden');
        } else if (/[^a-z0-9_]/i.test(line)) {
            console.log("ERROR: USERNAME: FORMAT")
            para.innerHTML = "username accepts English letters, numbers, and underscores";
            para.removeAttribute('hidden');
        } else {
            // validation passed
            // do something here
            console.log("VALID USERNAME");
            para.innerHTML = "some error happened";
            para.setAttribute('hidden');
        }
    } else if (component === "password") { // password validation
        let line = document.forms["register"]["password"].value;
        let para = document.getElementById("password_e");
        if (line.length != line.trim().length) {
            console.log("ERROR: PASSWORD: LEADING/TAILING SPACE");
            para.innerHTML = "password should contain no leading or tailing spaces";
            para.removeAttribute('hidden');
        } else if (line.length < 8 || line.length > 16) {
            console.log("ERROR: PASSWORD: LENGTH");
            para.innerHTML = "password must contain 8-16 (included) characters";
            para.removeAttribute('hidden');
        } else if (!(/^.*[A-Z].*$/.test(line) && /^.*[a-z].*$/.test(line) && /^.*[0-9].*$/.test(line))) {
            console.log("ERROR: PASSWORD: FORMAT");
            para.innerHTML = "password must contain at least one lowercase character, one uppercase character, and one digit";
            para.removeAttribute('hidden');
        } else {
            // validation passed
            // do something here
            console.log("VALID PASSWORD");
            para.innerHTML = "some error happened";
            para.setAttribute('hidden');
        }
    } else if (component === "repeat") {
        let line_0 = document.forms["register"]["password"].value;
        let line_1 = document.forms["register"]["repeat"].value;
        let para = document.getElementById("repeat_e");
        if (line_0 != line_1) {
            console.log("ERROR: REPEAT: NOT MATCH");
            para.innerHTML = "password did not match";
            para.removeAttribute('hidden');
        } else {
            // validation passed
            // do something here
            console.log("MATCHING REPEAT");
            para.innerHTML = "some error happened";
            para.setAttribute('hidden');
        }
    }
}

function validateForm() {
    let line = document.forms["register"]["username"].value;
    console.log("line: " + line)
    if (line != "") {
        console.log("ENTER if"); 
        let para = document.getElementsByTagName("p");
        para[0].innerHTML = line;
        para[0].removeAttribute("hidden");
        return false;
    } else {
        console.log("ENTER else");
        return false;
    }
}
