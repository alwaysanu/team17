function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie() {
    var user = getCookie("username");
    if (user == "") {


        $("#id01").show();

    }
    else {
        var activity=getActivity();
        if (activity) {
            $("#id02 #Activity").html("Activity Name:&nbsp;"+activity);
            $("#id02").show();
        }
    }
}
function getActivity() {
    var user = getCookie("username");
    var activity='';
    $.ajax({
        url:"/graphql",
        contentType: "application/json", type: "POST",
        async: false,
        data: JSON.stringify({
            query: `{
                user(email:"${user}"){
                    username
                    lastActivity    {
                        name
                        category
                    }
                }
            }`
        }),
        success: function(result){
            console.log(JSON.stringify(result))
            if(result.data.user.lastActivity!=null)
            {
            activity=result.data.user.lastActivity.name;
            $("#activityType").html(result.data.user.lastActivity.category);
            }
        }
    });
    return activity;
}
