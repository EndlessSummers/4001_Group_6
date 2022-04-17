// global variable for help window
var _index=0;
var clearTime = null;
var img_index = 8;
var upload_img_num = 0;

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
    } else if (info === "user") {
        state = validate_username();
    }

    if (!state) {
      console.log("INVALID INPUT");
      $("#error").removeAttr('style');
      e.preventDefault();
      return false;
    } else {
      console.log("VALID INPUT");
      // e.preventDefault();
      // return false;
      // console.log(info);
      // console.log("checkpoint1");
      $("#error").removeAttr('style').css("display", "none");
      $("#success").removeAttr('style').css("display", "none");
      if (info == "register") return true;
      if (info == "user") {
        save_usr_p(e);
        return true;
      }
      // if (info == "repeat") return true;
      if (info == "cancel") return true;
      return ajaxSubmit(info);
    }
}

function ajaxSubmit(info) {
  console.log("ajax function called");
  let string = {};
  $("#error").removeAttr('style').css("display", "none");
  $("#success").removeAttr('style').css("display", "none");
  $.ajax({
    url: "/",
    method: "POST",
    async: false,
    data: $('form').serialize(),
    success: function(args) {
      console.log("ajax success");
      string["status"] = args["status"];
      if (args["status"] == "failure") {
        $("#error").html(args["message"])
        $("#error").removeAttr('style').css("display", "block");
        // return false;
      } else if (args['status'] == 'success') {
        $("#success").html(args['message'])
        $("#success").removeAttr('style').css("display", "block");
        // return true;
      }
    },
    error: function(args) {
      console.log("!!!ajax failure!!!");
    }
  })
  console.log(info);
  if (info == "login") {
    console.log(string["status"]);
    if (string["status"] == "failure") return false;
    else return true;
  } else if (info == "register") {
    console.log("entered register");
    return true;
  }
  return false;
}

function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
}

function changeV(rangename) {
    if(rangename === 'Time') {
        var v = document.getElementById("Timerange").value;
        if (v === '0') {
            document.getElementById("Timevalue").innerHTML = "1 hours-";
        } else if (v === '9') {
            document.getElementById("Timevalue").innerHTML = "8 hours+";
        } else {
            document.getElementById("Timevalue").innerHTML = v + " hours";
        }
    } else if (rangename === 'Participant') {
        var v = document.getElementById("Participantrange").value;
        document.getElementById("Participantvalue").innerHTML = v;
    }
}

function ClearTags() {
  document.getElementById("Timerange").value = "-1";
  document.getElementById("Timevalue").innerHTML = "";
  document.getElementById("Participantrange").value = "-1";
  document.getElementById("Participantvalue").innerHTML = "";
  var Place = ["Home", "Outdoor", "Center", "Interest"];
  for (var j = 0; j < Place.length; j++) {
    document.getElementById(Place[j]).checked = false;
  }
  var Tags = ["Film", "Game", "Music", "Cooking", "Sports", "Handwork"];
  for (var i = 0; i < Tags.length; i++) {
    document.getElementById(Tags[i] + "tag").style.color = "#111";
    document.getElementById(Tags[i]).value = "0";
  }
}

function ChangeTags(Tagname) {
  var v = document.getElementById(Tagname).value;
  if(v === '0') {
    document.getElementById(Tagname + "tag").style.color = "#00ff00";
    document.getElementById(Tagname + "tag").title = "Dislike";
    document.getElementById(Tagname).value = "1";
  } else if (v === '1') {
    document.getElementById(Tagname + "tag").style.color = "#ff0000";
    document.getElementById(Tagname + "tag").title = "Remove";
    document.getElementById(Tagname).value = "-1";
  } else if (v === '-1') {
    document.getElementById(Tagname + "tag").style.color = "#111";
    document.getElementById(Tagname + "tag").title = "Like";
    document.getElementById(Tagname).value = "0";
  }
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    $("#filtersubmit").click(); 
    console.log("save button clicked")
}

function validate_username() {
  let user_name = document.forms['myform']['name'].value;
  console.log("user_name is "+user_name);
  let error = document.getElementById("error");

  if (user_name.length > 20) {
    console.log("ERROR: USER_NAME: CANNOT EXCEED 20 CHARACTERS")
    error.innerHTML = "USERNAME TOO LONG";
    return false;
  } else {
    console.log("VALIE USER_NAME");
    error.innerHTML = '';
  }

  return true;
}

function validate_email() {
    let email = document.forms["form"]["email"].value;
    let p_email = document.getElementById("error");
    // Question: email should end with @link.cuhk.edu.cn?
    let reg_email = /^[a-zA-Z0-9][\w\-]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$/
    if (!reg_email.test(email)) {
        console.log("ERROR: EMAIL: INCORRECT EMAIL FORMAT");
        p_email.innerHTML = "incorrect email format";
        return false;
    } else {
        // validation passed
        // do something here
        console.log("VAILD EMAIL");
        p_email.innerHTML = "";
    }
    return true;
}

function validate_change() {
    let oldPasswd = document.forms["form"]["oldpassword"].value;
    let passwd = document.forms["form"]["password"].value;
    let p_passwd = document.getElementById("error");
    if (oldPasswd == passwd) {
        console.log("ERROR: CHANGE: MATCH");
        p_passwd.innerHTML = "The new password is the same as the original password";
        return false;
    } else {
        // validation passed
        // do something here
        console.log("DIFFERENT NEW PASSWORD");
        p_passwd.innerHTML = "";
    }
    return true;
}

function validate_passwd() {
    let passwd = document.forms["form"]["password"].value;
    let p_passwd = document.getElementById("error");
    if (passwd.length != passwd.trim().length) {
        console.log("ERROR: PASSWORD: LEADING/TAILING SPACE");
        p_passwd.innerHTML = "password should contain no leading or tailing spaces";
        return false;
    } else if (passwd.length < 8 || passwd.length > 16) {
        console.log("ERROR: PASSWORD: LENGTH");
        p_passwd.innerHTML = "password must contain 8-16 (included) characters";
        return false;
    } else if (!(/^.*[A-Za-z].*$/.test(passwd) && /^.*[0-9].*$/.test(passwd))) {
        console.log("ERROR: PASSWORD: FORMAT");
        p_passwd.innerHTML = "password must contain at least one letter and one digit";
        return false;
    } else {
        console.log("VALID PASSWORD");
        p_passwd.innerHTML = "";
    }
    return true;
}

function validate_repeat() {
    let passwd = document.forms["form"]["password"].value;
    let repeat = document.forms["form"]["repeat"].value;
    let p_repeat = document.getElementById("error");
    if (passwd != repeat) {
        console.log("ERROR: REPEAT: NOT MATCH");
        p_repeat.innerHTML = "password did not match";
        return false;
    } else {
        // validation passed
        // do something here
        console.log("DIFFERENT NEW PASSWORD");
        p_repeat.innerHTML = "";
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

function load(e, info) {
  _index = 0;
  clearInterval(clearTime);
  e.preventDefault();
  const xhttp = new XMLHttpRequest();

  xhttp.onload = function() {
    document.getElementById("event_box").innerHTML = this.responseText;
    document.getElementById("event_box").removeAttribute("hidden");
    document.getElementById("close").onclick = function() {
      this.parentNode.parentNode.setAttribute("hidden", "True");
      this.parentNode.parentNode.removeChild(this.parentNode);
      console.log('window closed');
      return false;
    }
  };

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      xhttp.addEventListener("load", help);
    }
  }

  if (info === "login") {
    xhttp.open("GET", "/windows/window_login/");
  } else if (info === "signUp") {
    xhttp.open("GET", "/windows/window_reg_e/");
  } else if (info === "forget") {
    xhttp.open("GET", "/windows/window_forget_e/");
  } else if (info === "cancel") {
    xhttp.open("GET", "/windows/window_cancel/");
  } else if (info === "edit") {
    xhttp.open("GET", "/windows/window_user/");
  } else if (info === "help") {
    xhttp.open("GET", "/windows/window_help/");
  } else if (info === "profile") {
    path = "/windows/window_user?user=" + input;
    console.log(path);
    xhttp.open("GET", path);
  }
  
  xhttp.send();

  console.log("btn clicked");
}

function removeimg(uploadimg) {
  document.getElementById(uploadimg).remove();
  upload_img_num--;
  console.log("removing");
  console.log("image global number " + upload_img_num);
}

function edit_usr_p(e) {
  e.preventDefault()
  console.log('function ' + edit_usr_p.name);

  $("#chg_usr_p").css("cursor", "pointer");

  $("#chg_usr_p").off().click(function () {
    console.log("img btn clicked");
    $("#img_slt").click();
  });

  // var pic_change_flag = false;
  $("#img_slt").off().on("change", function(){
    console.log("changePic() called");
    pic_change_flag = true;
    var selectedFile = document.getElementById('img_slt').files[0];
    var img = document.getElementById('chg_usr_p');
    var reader = new FileReader();
    reader.onload = function() {
      img.src = this.result
    //   document.getElementById('user_picture').src = this.result;
    }
    reader.readAsDataURL(selectedFile);
  });

  // var form = document.getElementById('myform')
  var infos = document.getElementsByClassName('data_container');
  var datas = [];
  for (i=0; i<infos.length; i++) {
    let p = infos[i].getElementsByTagName("p")[0];
    data = p.innerHTML;
    p.setAttribute("hidden", "True");
    datas.push(data);
    input = infos[i].getElementsByTagName("input")[0]
    input.setAttribute("value", data);
    input.removeAttribute("hidden");
  }

  $("#edit").css("display", "none");
  $("#save").removeAttr("style");

  console.log(datas);

  // $("#save").one("click", function () {
  //   $("#edit").one("click", function(event) {
  //     edit_usr_p(event)
  //   });
  //   var inputs = [];
  //   $("#chg_usr_p").off();
  //   $("#chg_usr_p").removeAttr("style");
  //   console.log('function save called');
  //   for (i=0; i<infos.length; i++) {
  //     if (infos[i].getAttribute("name") == "email") continue;
  //     let input = infos[i].firstChild.value;
  //     inputs.push(input);
  //     console.log("input " + i + " " + input);
  //     // infos[i].innerHTML = input;
  //   }

    // var dict = {};
    // dict["name"] = inputs[0];
    // dict["title"] = inputs[1];
    // dict["email"] = inputs[2];
    // dict["phone"] = inputs[3];
    // dict["likes"] = inputs[4];
    // dict["want"] = inputs[5];
    // dict["hint"] = "profile";
    // dict["photo"] = document.getElementById('chg_usr_p').src;
    // dict['csrfmiddlewaretoken'] = $("input[name=csrfmiddlewaretoken]").val();

    // $.ajax({
    //   url: "/",
    //   method: "POST",
    //   async: false,
    //   data: dict,
    //   success: function(args) {
    //     console.log("ajax success");
    //     console.log(args["message"]);
    //     if (args["status"] == "failure") {
    //       $("#error").html(args["message"])
    //       $("#error").removeAttr('style').css("display", "block");
    //     } else if (args['status'] == 'success') {
    //       $("#success").html(args['message'])
    //       $("#success").removeAttr('style').css("display", "block");
    //     }
    //   },
    //   error: function(args) {
    //     console.log("!!!ajax failure!!!");
    //   }
    // })
    



    // myOnSubmit(e, "user");
  // });
  return false;
}

function log_out(e) {
  // const xhttp = new XMLHttpRequest();
  // xhttp.open("GET", "/logout/");
  // console.log("logout request send")
  // xhttp.send();
  // window.location.href = "{% url 'logout/' %}";
}

function help() {
  console.log("function help called");

  $(".bottom ul li").off().hover(function(){
    console.log("entered");
    $(".bottom ul li").eq(_index).toggleClass("isActive");
    _index = $(this).index();
    console.log("index " + _index);
    clearInterval(clearTime);
    $(".help .top .img").eq(_index).fadeIn(200).siblings().fadeOut(200);
    $(".bottom ul li").eq(_index).toggleClass("isActive");
    $(".bottom #helpText").html($(".help .top .img").eq(_index).html());
  },auto);

  function auto(){
    console.log("_index " + _index);
    clearTime = setInterval(function(){
      $(".bottom ul li").eq(_index).toggleClass("isActive");
      _index++;
      if(_index>4) _index=0;
      $(".help .top .img").eq(_index).fadeIn(200).siblings().fadeOut(200);
      $(".bottom ul li").eq(_index).toggleClass("isActive");
      $(".bottom #helpText").html($(".help .top .img").eq(_index).html());
    },5000);
  }

  auto();
}

function save_usr_p(e) {
  console.log('function ' + save_usr_p.name);
  $("#chg_usr_p").off();
  $("#chg_usr_p").removeAttr("style");

  var infos = document.getElementsByClassName('data_container');
  var datas = [];
  for (i=0; i<infos.length; i++) {
    input = infos[i].getElementsByTagName("input")[0];
    data = input.value;
    input.setAttribute("hidden", "True");
    datas.push(data);
    let p = infos[i].getElementsByTagName("p")[0];
    p.innerHTML = data;
    p.removeAttribute("hidden");
    // input.removeAttribute("value");
  }
  console.log(datas);

  var user_name = document.getElementsById('profile_name');
  var new_name = infos[0].getElementsByTagName("p")[0].innerHTML;
  // console.log(new_name+"<br>"+document.getElementsByName("email")[0].innerHTML);
  user_name.innerHTML = new_name;

  document.getElementById('user_picture').src = document.getElementById('chg_usr_p').src;

  $("#save").css("display", "none");
  $("#edit").removeAttr("style");
}

function like(e, info) {
  if ($("#user-profile").attr("style") == "display:none;"){
    alert("You cannot like a event when not logging in");
    return;
  }
  $("#like_button").toggleClass("heart");
  console.log($(this).html);
  var value;
  if ($("#like_button").hasClass("heart")) {
    $("#likes").html(parseInt($("#likes").html())+1);
    value = 1;
  } else {
    $("#likes").html(parseInt($("#likes").html())-1);
    value = -1;
  }

  $.ajax({
    url: "/project/",
    method: "GET",
    data: {
      "hint": "like",
      "value": value,
      "image": info,
    },
    success: function(args) {
      console.log("ajax success");
    },
    error: function(args) {
      console.log("!!!ajax failure!!!");
    }
  })
}

function like_note(e, info, ind, image) {
  if ($("#user-profile").attr("style") == "display:none;"){
    alert("Log in to like a note");
    return;
  }
  button_name = "#like_note_button"+ind;
  console.log(button_name);
  like_name = "#note_likes"+ind;
  $(button_name).toggleClass("heart");
  var value;
  if ($(button_name).hasClass("heart")) {
    $(like_name).html(parseInt($(like_name).html())+1);
    value = 1;
  } else {
    $(like_name).html(parseInt($(like_name).html())-1);
    value = -1;
  }

  $.ajax({
    url: "/project/",
    method: "GET",
    data: {
      "hint": "like_note",
      "value": value,
      "id": info,
      "image": image,
    },
    success: function(args) {
      console.log("ajax success");
    },
    error: function(args) {
      console.log("!!!ajax failure!!!");
    }
  })
}