/**
 * Created by eric on 10/6/15.
 */

function submit_data() {
    console.log("gotten");
    var xhr = new XMLHttpRequest();
    var action = $("#bcform").attr("action");
    xhr.open("POST", action, true);
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send($('#bcform').serialize());

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var relinquish = JSON.parse(xhr.responseText)["relinquish"];
            var newField = "input[name='" + relinquish + "']";
            $(newField).show();
            $(newField).prop("disabled",false);
            $("#bcform").prop("action",JSON.parse(xhr.responseText)["action"]);
        }
    };

    console.log("ajax'd");
}

var main = function() {
    var screenheight = window.innerHeight;   //measures the height of the user's screen

    //$("#index_search").css("margin-top", windowheight/3);
    console.log(screenheight);
    var maincontain = document.getElementById("index_search");
    maincontain.style.marginTop = (screenheight/4) + "px";

    $("#bcform").on('submit', function(event) {
        event.preventDefault();
        console.log("submitted");
        submit_data();
    })
};

$(document).ready(main);