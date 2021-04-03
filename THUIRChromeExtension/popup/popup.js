//var baseUrl = "http://166.111.138.86:15016";
var baseUrl = "http://127.0.0.1:8000";
//var baseUrl = "http://192.168.56.103:8080";
var checkUrl = baseUrl + "/user/check/";
var registerUrl = baseUrl + "/user/signup/";
var feedbackUrl = baseUrl + "/task/home/";
var downloadLink = "";

function userTab() {
    $("#failMsg1").hide();
    $("#failMsg2").hide();
    $("#failMsg3").hide();
    $("#login").hide();
    $("history").hide();
    document.getElementById('uploadBt').style.display = 'none';
    document.getElementById('deleteBt').style.display = 'none';
    document.getElementById('historyp').style.display = 'none';
    $("#logged").show();
}

function loginTab() {
    $("#logged").hide();
    $("#failMsg1").hide();
    $("#failMsg2").hide();
    $("#failMsg3").hide();
    $("history").hide();
    document.getElementById('historyp').style.display = 'none';
    document.getElementById('deleteBt').style.display = 'none';
    document.getElementById('uploadBt').style.display = 'none';
    $("#login").show();
}

function historyTab() {
    $("#logged").hide();
    $("#failMsg1").hide();
    $("#failMsg2").hide();
    $("#failMsg3").hide();
    $("#login").hide();
    $("history").show();
    document.getElementById('historyp').style.display = '';
    document.getElementById('deleteBt').style.display = '';
    document.getElementById('uploadBt').style.display = '';
    document.body.style = 'min-width : 450px; ';
}


function verifyUser() {
    //console.log("checking...");
    var result = -1;
    if (localStorage['username'] != undefined && localStorage['password'] != undefined) {
        var name = localStorage['username'];
        var psw = localStorage['password'];
        //console.log("POSTing...");
        $.ajax
        ({
            type: "POST",
            url: checkUrl,
            dataType: 'json',
            async: false,
            data: {username: name, password: psw},
            success: function (data, textStatus) {
                if (data == 0) {
                    result = 0;
                }
                if (data == 1) {
                    result = 1;
                }
                if (data == 2) {
                    result = 2;
                }
            },
            error: function () {
                result = -1;
            }
        });
    }
    return result;
}

function getLocalTime(nS) {
  var now = new Date(parseInt(nS));
  var yy = now.getFullYear();      //年
  var mm = now.getMonth() + 1;     //月
  var dd = now.getDate();          //日
  var hh = now.getHours();         //时
  var ii = now.getMinutes();       //分
  var ss = now.getSeconds();       //秒
  var clock = yy + "/";
  if(mm < 10) clock += "0";
  clock += mm + "/";
  if(dd < 10) clock += "0";
  clock += dd + " ";
  if(hh < 10) clock += "0";
  clock += hh + ":";
  if (ii < 10) clock += '0';
  clock += ii + ":";
  if (ss < 10) clock += '0';
  clock += ss;
  return clock;
}

function getData(str) {
  str = str.split('/');
  return str[0] + '/' + str[1] + '/' + str[2];
}

var newArr;
var tot;

function $allOnClick(){
    //console.log('allOn');
    //console.log($(this).attr('name'));
    //console.log($(this).prop("checked"));

    var input = document.getElementsByName($(this).attr('name'));
    //console.log(input);
    for(var i = 1; i < input.length; ++i) {
      input[i].checked = $(this).prop("checked");
      //console.log(i + ' ' + input[i].checked);
    }
}


function getHistory() {
    var str = "";
    historyTab();
    var arr = new Array();
    for (var i = localStorage.length - 1; i >= 0; i--) {
        var lastkey = localStorage.key(i);
        if (lastkey.match(/[0-9]*/g)[0] != lastkey) continue;
        var Msg = JSON.parse(localStorage[lastkey]);
        var tmp = '';
        tmp += getLocalTime(lastkey) + '$';
        tmp += Msg.title + '$';
        tmp += '<a href="' + Msg.url +'" target="_blank" style="color: #5D5D5D">' + Msg.url.substr(0, Msg.url.indexOf('/', 9)) + '</a>';
        tmp += '$' + lastkey;
        arr.push(tmp);
    }
    arr.sort();
    newArr = new Array();
    newArr.push({
      'str' : arr[0].split('$').slice(0, 3).join('$'),   // 展示内容
      'key' : [arr[0].split('$')[3],]  // 时间戳
    });

    for(var i = 1; i < arr.length; ++i) {
      //console.log(newArr[newArr.length-1]);
      //console.log(newArr[newArr.length-1].str);
      var lastTitle = newArr[newArr.length-1].str.split('$')[1];
      var nowTitle = arr[i].split('$')[1];
      if(lastTitle != nowTitle) {
        newArr.push({
          'str' : arr[i].split('$').slice(0, 3).join('$'),   // 展示内容
          'key' : [arr[i].split('$')[3],]  // 时间戳
        });
      }
      else {
        newArr[newArr.length-1].key.push(arr[i].split('$')[3]);
      }
    }
    //console.log(newArr);
    tot = 0;
    // 大标题 name 为日期  id 为 Date'i'
    for(var i = newArr.length-1; i >= 0; --i) {
      if(i == newArr.length-1 || newArr[i].str.split(' ')[0] != newArr[i + 1].str.split(' ')[0]) {
        str += '<input type = "checkbox" checked = "checked"  name = "' + newArr[i].str.split(' ')[0] + '" id = "Date' + (++tot) + '"/>';
        str += '<font size="4">' + getData(newArr[i].str.split(' ')[0]) + '</font>\n<hr style=" height:1px;border:none;border-top:1px solid #F0F0F0;" />';
      }
      // 小标题 name 为日期  id 为 'i'
      str += '<p><input type="checkbox" checked = "checked" name ="' + newArr[i].str.split(' ')[0] + '" id = "' + i + '"/>';
      var tmp = newArr[i].str.split('$');
      tmp[0] = tmp[0].split(' ');
      tmp[0].shift();

      tmp[0] = '<font color="#5D5D5D">' + tmp[0] + '</font>';
      str += tmp.join('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;');
      str += '</p>\n';
    }

    document.getElementById('historyp').innerHTML=str;

    for (var i = 1; i <= tot; i++) { // 给大标题绑定全选事件
      document.getElementById('Date'+i).addEventListener("click", $allOnClick);
    }

}

function Delete() {
  var msg = "are you sure to delete these records? deleted records can not be retrieved or uploaded!";
  if(!confirm(msg)) return ;
  var bg = chrome.extension.getBackgroundPage();
  for (var i = 0; i < newArr.length - 1; i++)
    if(document.getElementById(''+i).checked == true) {
      for(var j = 0; j < newArr[i].key.length; ++j) {
        var lastkey = newArr[i].key[j];
        var Msg = localStorage[lastkey];
        bg.deleteInfo(lastkey);
      }
    }
  confirm('delete success');
  location.reload()
}

function Upload() {
    var msg = "are you sure to upload?";
    var flag = 1;
    if (!confirm(msg)) return ;
    var bg = chrome.extension.getBackgroundPage();
    for (var i = 0; i < newArr.length; i++)
      if(document.getElementById(''+i).checked == true) {
        for(var j = 0; j < newArr[i].key.length; ++j) {
          var lastkey = newArr[i].key[j];
          var Msg = localStorage[lastkey];
          bg.deleteInfo(lastkey);
          ms = bg.sendInfo(Msg);
          //console.log(JSON.parse(Msg));
          //console.log(Msg);
          if(ms == 0) flag = 0;
        }
      }
    if(flag) confirm('upload success');
    else confirm('upload failed, please try again');
    location.reload()
}

function register() {
    window.open(registerUrl);
}

function trylogin() {
    //console.log("logging...");
    localStorage['password'] = "" + $("#psw").val();
    localStorage['username'] = "" + $("#username").val();
    var verified = verifyUser();
    if (verified == 0) {
        userTab();
        chrome.browserAction.setBadgeText({text: 'on'});
        chrome.browserAction.setBadgeBackgroundColor({color: [255, 0, 0, 255]});
    } else {
        chrome.browserAction.setBadgeText({text: ''});
        if (verified == 1) {
            $("#failMsg2").hide();
            $("#failMsg3").hide();
            $("#failMsg1").show();
        }
        if (verified == 2) {
            $("#failMsg1").hide();
            $("#failMsg3").hide();
            $("#failMsg2").show();
        }
        if (verified == -1) {
            $("#failMsg1").hide();
            $("#failMsg2").hide();
            $("#failMsg3").show();
        }
    }
}

function feedback() {
    //if (confirm("提示: 若正在进行搜索任务(搜索页面未关闭),请在进行标注前关闭搜索页面!\n若没有请忽略此信息"))
    window.open(feedbackUrl);
}

function download() {
    window.open(downloadLink, '_blank');
}

function logout() {
    localStorage['username'] = null;
    localStorage['password'] = null;
    localStorage['log_status'] = "off";
    chrome.browserAction.setBadgeText({text: ''});
    location.reload();
}

if (jQuery) {
    loginTab();
    $("#bt1").click(register);
    $("#bt2").click(trylogin);
    $("#bt4").click(feedback);
    $("#bt8").click(feedback);
    $("#bt6").click(logout);
    $("#historyBt").click(getHistory);
    $("#uploadBt").click(Upload);
    $("#deleteBt").click(Delete);
    if (verifyUser() == 0) {
        userTab();
        chrome.browserAction.setBadgeText({text: 'on'});
        chrome.browserAction.setBadgeBackgroundColor({color: [255, 0, 0, 255]});
    }
    else {
        chrome.browserAction.setBadgeText({text: ''});
    }
} else {
    console.log("jQuery is needed!");
}
