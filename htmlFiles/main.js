// global variable for help window
var _index=0;
var clearTime = null;

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
        e.preventDefault();
        return false;
    } else {
        document.getElementById("success").setAttribute("display", "block");
        console.log("VALID INPUT");
        return true;
    }
}

function openNav() {
    document.getElementById("mySidenav").style.width = "1000px";
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
    document.getElementById(Tagname).value = "2";
  } else if (v === '2') {
    document.getElementById(Tagname + "tag").style.color = "#111";
    document.getElementById(Tagname + "tag").title = "Like";
    document.getElementById(Tagname).value = "0";
  }
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
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
  e.preventDefault();
  const xhttp = new XMLHttpRequest();

  xhttp.onload = function() {
    document.getElementById("event_box").innerHTML = this.responseText;
    document.getElementById("event_box").removeAttribute("hidden");
    document.getElementById("close").onclick = function() {
      this.parentNode.parentNode.setAttribute("hidden", "True");
      this.parentNode.parentNode.removeChild(this.parentNode);
      console.log('window closed');
      _index = 0;
      clearInterval(clearTime);
      return false;
    }
  };

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      xhttp.addEventListener("load", help);
    }
  }

  if (info === "login") {
    xhttp.open("GET", "./window_login.html");
  } else if (info === "signUp") {
    xhttp.open("GET", "./window_reg_e.html");
  } else if (info === "forget") {
    xhttp.open("GET", "./window_forget_e.html");
  } else if (info === "cancel") {
    xhttp.open("GET", "./window_cancel.html");
  } else if (info === "edit") {
    xhttp.open("GET", "./window_user.html");
  } else if (info === "help") {
    xhttp.open("GET", "./window_help.html");
  }
  
  xhttp.send();

  console.log("btn clicked");
}

function removeimg(uploadimg) {
  document.getElementById(uploadimg).remove();
}

window.onload = function () {
  var input = document.getElementById("note-image");
  var div;
  // 当用户上传时触发事件
  input.onchange = function () {
    document.getElementById("image_view").innerHTML = "";
    readFile(this);
  }
  //处理图片并添加都dom中的函数
  var readFile = function (obj) {
    // 获取input里面的文件组
    var fileList = obj.files;
    if (fileList.length > 9) {
      return alert("The number of uploaded images cannot be greater than 9.");
    }
    //对文件组进行遍历，可以到控制台打印出fileList去看看
    var j = 0;
    for (var i = 0; i < fileList.length; i++) {
      if (!input['value'].match(/.jpg|.jpeg|.gif|.png|.bmp/i)) {  //判断所选文件格式
        return alert("The format of the uploaded images are incorrect.");
      }
      var reader = new FileReader();
      reader.readAsDataURL(fileList[i]);
      // 当文件读取成功时执行的函数
      reader.onload = function (e) {
        div = document.createElement('div');
        div.id = "uploadimg_"+j;
        div.innerHTML = '<img src="' + this.result + '" /><a class="removebtn" onclick="removeimg(\'uploadimg_'+j+'\')">&times;</a>';
        document.getElementById("image_view").appendChild(div);
        j++;
      }
    }
  }
}

function edit_usr_p(e) {
  console.log('function ' + edit_usr_p.name);

  $("#chg_usr_p").off().click(function () {
    console.log("img btn clicked");
    $("#img_slt").click();
  });

  var pic_change_flag = false;
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
  
  var box = document.getElementById('event_box')
  var infos = box.getElementsByTagName('p');
  var inputs = [];
  for (i=0; i<infos.length; i++) {
    let inputText = "<input type='text' value='' style='width: 100%;'>";
    let input = infos[i].innerHTML;
    inputs.push(input);
    infos[i].innerHTML = inputText.replace(/value=''/, function(x) {
      return x.slice(0, x.length-1) + input + x.slice(x.length-1);
    })
    // replace does not modify the original text;
  }

  console.log(inputs);
  $("#save").off().click(function () {
    console.log('function save called');
    for (i=0; i<infos.length; i++) {
      let input = infos[i].firstChild.value;
      console.log("input " + i + " " + input);
      infos[i].innerHTML = input;
    }

    if (infos[0].innerHTML != inputs[0]) { // user name changed
      var user_name = document.getElementById("user-profile").getElementsByTagName('p')[0];
      var new_name = user_name.innerHTML.replace(inputs[0], infos[0].innerHTML);
      user_name.innerHTML = new_name;
    }

    if (pic_change_flag) { // user profile changed
      document.getElementById('user_picture').src = document.getElementById('chg_usr_p').src;
    }
  });
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
    },3000);
  }

  auto();
}



// function save_usr_p(e) {
//   console.log('function ' + save_usr_p.name);
//   var box = document.getElementById('event_box')
//   var infos = box.getElementsByTagName('p');
//   for (i=0; i<infos.length; i++) {
//     let input = infos[i].firstChild.value;
//     infos[i].innerHTML = input;
//   }
// }

