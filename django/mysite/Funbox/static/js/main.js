// global variable for help window
var _index=0;
var clearTime = null;

// global variable for dynamically loading 
// img_index for items (index.html) with no scrolling down, default load 8 items
// note_index for notes (project.html) with no scrolling down, default load 3 notes (if possible)
var img_index = 8;
var note_index = 3;

// front-end checking before submitting a form
function myOnSubmit(e, info) {
  var state;
  // based on info, do front-end validation
  // state is at last a boolean
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
    // front-end validation fails
    // show error message & hidden success message & prevent form submitting
    $("#error").removeAttr('style');
    $("#success").removeAttr('style').css("display", "none");
    e.preventDefault();
    return false;
  } else {
    // front-end validation success
    // hidden both error and success message
    $("#error").removeAttr('style').css("display", "none");
    $("#success").removeAttr('style').css("display", "none");
    
    // return true if does not submit in ajax
    // i.e. direct submit, will possibly reload/redirect page 
    if (info == "register") return true;
    if (info == "user") {
      save_usr_p(e);
      return true;
    }
    if (info == "cancel") return true;
    // submit in ajax 
    return ajaxSubmit(info);
  }
}

// ajax submission, get response from backend and update page without reload/redirect
function ajaxSubmit(info) {
  let response = {};

  // ajax routine
  $.ajax({
    url: "/",
    method: "POST",
    // wait for result before going forward
    async: false,
    // send form data
    data: $('form').serialize(),
    success: function(args) {
      // ajax submission suceess, processing the response
      // to copy ajax response for access outside the ajax routine
      response["status"] = args["status"];
      if (args["status"] == "failure") {
        // submission fails in backend
        // set error message and display
        $("#error").html(args["message"])
        $("#error").removeAttr('style').css("display", "block");
      } else if (args['status'] == 'success') {
        // submission success in backend
        // set success message and display
        $("#success").html(args['message'])
        $("#success").removeAttr('style').css("display", "block");
      }
    },
    error: function(args) {
      // ajax submission fails
      // usually django raise an error, check terminal
      console.log("!!!ajax failure!!!");
    }
  })

  // ajax submission specification
  if (info == "login") {
    // for login
    // return false when user/password error, login fails
    // return true when user/passwrod match, reload page
    if (response["status"] == "failure") return false;
    else return true;
  } else if (info == "register") {
    // for register
    // return true to redirect page
    return true;
  }

  // stop form from submitting
  // do not reload or redirect
  return false;
}

// open filterbar by setting width to 100%
function openNav() {
  document.getElementById("mySidenav").style.width = "100%";
}

// filterbar value change function for time & participants
function changeV(rangename) {
  if(rangename === 'Time') {
    // Time Change
    // Display text based on value
    var v = document.getElementById("Timerange").value;
    if (v === '0') {
      document.getElementById("Timevalue").innerHTML = "1 hours-";
    } else if (v === '9') {
      document.getElementById("Timevalue").innerHTML = "8 hours+";
    } else {
      document.getElementById("Timevalue").innerHTML = v + " hours";
    }
  } else if (rangename === 'Participant') {
    // Participant Change
    // Display text based on value
    var v = document.getElementById("Participantrange").value;
    document.getElementById("Participantvalue").innerHTML = v;
  }
}

// fliterbar reset all information
function ClearTags() {
  // reset Time & Participant 
  document.getElementById("Timerange").value = "0";
  document.getElementById("Timevalue").innerHTML = "";
  document.getElementById("Participantrange").value = "0";
  document.getElementById("Participantvalue").innerHTML = "";

  // reset Place
  var Place = ["Home", "Outdoor", "Center", "Interest"];
  for (var j = 0; j < Place.length; j++) {
    document.getElementById(Place[j]).checked = false;
  }

  // reset Tags
  var Tags = ["Film", "Game", "Music", "Cooking", "Sports", "Handwork"];
  for (var i = 0; i < Tags.length; i++) {
    document.getElementById(Tags[i] + "tag").style.color = "#111";
    document.getElementById(Tags[i]).value = "0";
  }
}

// filterbar tag selection with color
function ChangeTags(Tagname) {
  // access html element by Tagname
  var v = document.getElementById(Tagname).value;

  // change color based on tag value
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

// close filterbar by set width to 0 and submit filter information
function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
  $("#filtersubmit").click();
}

// front-end username checking
// username should contain less than 20 characters
function validate_username() {
  // access html elements
  let user_name = document.forms['myform']['name'].value;
  let error = document.getElementById("error");

  if (user_name.length > 20) {
    // validation fails, Length error, set error message
    error.innerHTML = "USERNAME TOO LONG";
    return false;
  } else {
    // validation success, clear error message
    error.innerHTML = '';
  }

  return true;
}

// front-end email checking
// email should contain at least one '@' and one '.' and not end with a '.'
function validate_email() {
  // access html elements
  let email = document.forms["form"]["email"].value;
  let p_email = document.getElementById("error");
  
  // regular expression to fit email requirement
  let reg_email = /^[a-zA-Z0-9][\w\-]+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+$/
  
  if (!reg_email.test(email)) {
    // validation fails, Format error, set error message
    p_email.innerHTML = "incorrect email format";
    return false;
  } else {
    // validation success, clear error message
    p_email.innerHTML = "";
  }

  return true;
}

// front-end password difference checking (reset password)
// in reset password, new and old password should be different
function validate_change() {
  // access html elements
  let oldPasswd = document.forms["form"]["oldpassword"].value;
  let passwd = document.forms["form"]["password"].value;
  let p_passwd = document.getElementById("error");

  if (oldPasswd == passwd) {
    // validation fails, Difference error, set error message
    p_passwd.innerHTML = "The new password is the same as the original password";
    return false;
  } else {
    // validation success, clear error message
    p_passwd.innerHTML = "";
  }

  return true;
}

// front-end password checking
// password should has no leading and tailing blank spaces 
// the length of password should in 8-16
// password should contain at least one character and one digit
function validate_passwd() {
  // access html elements
  let passwd = document.forms["form"]["password"].value;
  let p_passwd = document.getElementById("error");

  if (passwd.length != passwd.trim().length) {
    // validation fails, Leading/Tailing space error, set error message
    p_passwd.innerHTML = "password should contain no leading or tailing spaces";
    return false;
  } else if (passwd.length < 8 || passwd.length > 16) {
    // validation fails, Length error, set error message
    p_passwd.innerHTML = "password must contain 8-16 (included) characters";
    return false;
  } else if (!(/^.*[A-Za-z].*$/.test(passwd) && /^.*[0-9].*$/.test(passwd))) {
    // validation fails, Format error, set error message
    p_passwd.innerHTML = "password must contain at least one letter and one digit";
    return false;
  } else {
    // validation success, clear error message
    p_passwd.innerHTML = "";
  }

  return true;
}

// frontend password agreement checking (set password)
// in set password (including reset password), two new password should be the same
function validate_repeat() {
  // access html elements
  let passwd = document.forms["form"]["password"].value;
  let repeat = document.forms["form"]["repeat"].value;
  let p_repeat = document.getElementById("error");

  if (passwd != repeat) {
    // validation fails, Match error, set error message
    p_repeat.innerHTML = "password did not match";
    return false;
  } else {
    // validation success, clear error message
    console.log("DIFFERENT NEW PASSWORD");
    p_repeat.innerHTML = "";
  }

  return true;
}

// change the visibility of passwords
function togglePasswordView(e, info) {
  // prevent form from submitting
  e.preventDefault();

  // access html element
  passwd = document.getElementById("Password");
  
  // get type attribute and toggle
  const type = passwd.getAttribute("type") === "password" ? "text" : "password";

  // set type attribute
  passwd.setAttribute("type", type);

  // base on info, view other passwords as well
  if (info === "repeat") {
    // in set password
    repeat = document.getElementById("Repeat");
    repeat.setAttribute("type", type);
  } else if (info === "triple") {
    // in reset password
    repeat = document.getElementById("Repeat");
    oldpasswd = document.getElementById("OldPassword");
    repeat.setAttribute("type", type);
    oldpasswd.setAttribute("type", type);
  }
}

// load 'window's on button clicks using XMLHttpRequest
function load(e, info) {
  // reset global parameters for 'help window'
  _index = 0;
  clearInterval(clearTime);

  // prevent form from submitting
  e.preventDefault();
  
  // create XMLHttpRequest object
  const xhttp = new XMLHttpRequest();

  // set onload function
  // load window in pre-set wrapper 'event_box' and set close function 
  xhttp.onload = function() {
    // access html elements
    document.getElementById("event_box").innerHTML = this.responseText;
    document.getElementById("event_box").removeAttribute("hidden");

    // set close function
    document.getElementById("close").onclick = function() {
      this.parentNode.parentNode.setAttribute("hidden", "True");
      this.parentNode.parentNode.removeChild(this.parentNode);
      // prevent submitting
      return false;
    }
  };

  // call help function
  // will do nothing if not 'help window' loaded
  // will begin counting for automatically switch if 'help window' loaded
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      xhttp.addEventListener("load", help);
    }
  }

  // get 'window' based on given information
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
  }
  
  // send 'window' found by open method
  // 'window' begins to load -> xhttp.onload
  xhttp.send();
}

// remove loaded image (note editor)
function removeimg(uploadimg) {
  // clear both image and file selector 
  document.getElementById(uploadimg).remove();
  document.getElementById("note-image").value = '';
}

// click to edit user profile
function edit_usr_p(e) {
  // prevent form from submitting
  e.preventDefault()

  // set point style for profile image
  $("#chg_usr_p").css("cursor", "pointer");
  // set click function for profile image
  $("#chg_usr_p").off().click(function () {
    $("#img_slt").click();
  });

  // set on change function for file selector
  $("#img_slt").off().on("change", function(){
    // set flag to timely update front-end profile, do not refresh page
    pic_change_flag = true;

    // access html elements
    var selectedFile = document.getElementById('img_slt').files[0];
    var img = document.getElementById('chg_usr_p');

    // read select file (must be a image)
    var reader = new FileReader();
    reader.onload = function() {
      img.src = this.result
    }
    reader.readAsDataURL(selectedFile);
  });

  // access elements
  var infos = document.getElementsByClassName('data_container');
  var datas = [];
  let p = infos[0].getElementsByTagName("p")[0];

  // read data (original username) & hide 
  data = p.innerHTML;
  p.setAttribute("hidden", "True");
  datas.push(data);

  // set input value to (original username) & show
  input = infos[0].getElementsByTagName("input")[0]
  input.setAttribute("value", data);
  input.removeAttribute("hidden");

  // hide edit button and show save button
  $("#edit").css("display", "none");
  $("#save").removeAttr("style");

  return false;
}

// automatically switch for help window
function help() {
  // set hover function to bars
  $(".bottom ul li").off().hover(function(){
    // toggle the class of the current bar based on index
    // will alter length and color
    $(".bottom ul li").eq(_index).toggleClass("isActive");
    
    // get index of the bar, which users hover the mouse
    _index = $(this).index();

    // remove automatically switch
    clearInterval(clearTime);

    // fade in banner (image) based on index, all other banners fade out
    $(".help .top .img").eq(_index).fadeIn(200).siblings().fadeOut(200);
    // set isActive class, will alter length and color
    $(".bottom ul li").eq(_index).toggleClass("isActive");
    // show corresponding help text below
    $(".bottom #helpText").html($(".help .top .img").eq(_index).html());

    // call auto() again when user stop hovering
  },auto);

  // function for automatically switch
  function auto(){
    // set interval handler 
    clearTime = setInterval(function(){
      // toggle class based on index, will alter length and color
      $(".bottom ul li").eq(_index).toggleClass("isActive");
      
      // index increment but no exceeding boundary (3)
      _index++;
      if(_index>3) _index=0;

      // fade in banner based on index, all other banners fade out
      $(".help .top .img").eq(_index).fadeIn(200).siblings().fadeOut(200);
      // set isActive class, will alter length and color
      $(".bottom ul li").eq(_index).toggleClass("isActive");
      // show corresponding help text below
      $(".bottom #helpText").html($(".help .top .img").eq(_index).html());

      // Interval set to 5000 millisecons
      // call the procedure every 5000 milliseconds
    },5000);
  }

  // call auto(), begin to count down and switch
  auto();
}

// click to save user profile information
function save_usr_p(e) {
  // remove cursor style and click function for profile image
  $("#chg_usr_p").off();
  $("#chg_usr_p").removeAttr("style");

  // get html elements
  var infos = document.getElementsByClassName('data_container');
  var datas = [];

  // access data (new username) & hide input
  input = infos[0].getElementsByTagName("input")[0];
  data = input.value;
  input.setAttribute("hidden", "True");
  datas.push(data);

  // overwrite old name with data & show
  let p = infos[0].getElementsByTagName("p")[0];
  p.innerHTML = data;
  p.removeAttribute("hidden");

  // timely change username in sidebar
  var user_name = document.getElementById('profile_name');
  var new_name = infos[0].getElementsByTagName("p")[0].innerHTML;
  user_name.innerHTML = new_name;

  // timely change user profile in sidebar
  document.getElementById('user_picture').src = document.getElementById('chg_usr_p').src;

  // hide save & show edit
  $("#save").css("display", "none");
  $("#edit").removeAttr("style");
}

// like a project, alter heart color and send information to backend
function like(e, info) {
  // check login status (in a complicated way, but work)
  if ($("#user-profile").attr("style") == "display:none;"){
    // alert & do nothing if not login
    alert("You cannot like a event when not logging in");
    return;
  }

  // toggle class, will change color and play animation
  $("#like_button").toggleClass("heart");

  // value to send to back-end
  // 1: True (in back-end); -1: False (in back-end)
  var value;

  // alter the value follow the heart (how many people like the activity)
  if ($("#like_button").hasClass("heart")) {
    $("#likes").html(parseInt($("#likes").html())+1);
    value = 1;
  } else {
    $("#likes").html(parseInt($("#likes").html())-1);
    value = -1;
  }

  // send by ajax
  $.ajax({
    url: "/project/",
    method: "GET",
    // data
    data: {
      "hint": "like",
      "value": value,
      "image": info,
    },
    success: function(args) {
      // do nothing
      console.log("ajax success");
    },
    error: function(args) {
      // do nothing
      console.log("!!!ajax failure!!!");
    }
  })
}

// like a note, alter heart color and send information to backend
function like_note(e, info, ind, image) {
  // check login status (in a complicated way, but work)
  if ($("#user-profile").attr("style") == "display:none;"){
    // alert & do nothing if not login
    alert("Log in to like a note");
    return;
  }

  // find the corresponding heart button & number follows the button
  button_name = "#like_note_button"+ind;
  like_name = "#note_likes"+ind;

  // toggle class, will change color and play animation
  $(button_name).toggleClass("heart");
  
  // value to send to back-end
  // 1: True (in back-end); -1: False (in back-end)
  var value;

  // alter the value follow the heart (how many people like the note)
  if ($(button_name).hasClass("heart")) {
    $(like_name).html(parseInt($(like_name).html())+1);
    value = 1;
  } else {
    $(like_name).html(parseInt($(like_name).html())-1);
    value = -1;
  }

  // send by ajax
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
      // do nothing
      console.log("ajax success");
    },
    error: function(args) {
      // do nothing
      console.log("!!!ajax failure!!!");
    }
  })
}

// load others' profile but cannot edit using XMLHttpRequest
function load_other(e, user) {
  // create XMLHttpRequest object
  const xhttp = new XMLHttpRequest();

  // set onload function
  // load window in pre-set wrapper 'event_box' and set close function 
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

  // create path to that user's profile
  path = "/windows/window_other?user=" + user;

  // get 'window' based on path
  xhttp.open("GET", path);

  // send 'window' found by open method
  // 'window' begins to load -> xhttp.onload
  xhttp.send();
} 