/**
 * Created by eric on 10/6/15.
 */

//var origin_info;

function submit_data() {
    //console.log("gotten");
    var xhr = new XMLHttpRequest();
    var action = $("#bcform").attr("action");
    xhr.open("POST", action, true);
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    request_data = $('#bcform').serialize();
    console.log(request_data);
    xhr.send(request_data);

    var i = 0;
    var interval = setInterval(function() {
      i = ++i % 4;
      $("#bcButton").html("Loading "+Array(i+1).join("."));
    }, 800);

    xhr.onreadystatechange = function() {
        console.log(xhr.readyState);
        if (xhr.readyState == 4 && xhr.status == 200) {
            var jsonResponse = JSON.parse(xhr.responseText);
            var relinquish = jsonResponse["relinquish"];
            var newField = "input[name='" + relinquish + "']";
            $(newField).show();
            $(newField).prop("disabled",false);
            $("#bcform").prop("action",jsonResponse["action"]);
            $("input[name='origin_city']").val(jsonResponse["origin_city"]); //update origin_info
            $("input[name='origin_coordinates']").val(jsonResponse["origin_coordinates"]); //update origin_info
            if ($("#map").css("display") == "none") {
                initMap(jsonResponse["origin_coordinates"]);
            }
            clearInterval(interval);
            if (jsonResponse["status"] == "ok") {
                $("#bcButton").hide();
                $("#complete").show();
            }
            $("#bcButton").html("Go!");
        }
    };
    //console.log("ajax'd");
}

var main = function() {
    var screenheight = window.innerHeight;   //measures the height of the user's screen

    var maincontain = document.getElementById("index_search");
    maincontain.style.marginTop = (screenheight/4) + "px";

    $("#bcform").on('submit', function(event) {
        event.preventDefault();
        console.log("submitted");
        submit_data();
    });

};

//Initialize a map with the origin location
var map;
function initMap(coordinate_string) {
    var latlng = coordinate_string.split(",");

    var originco = {lat: Number(latlng[0]), lng: Number(latlng[1])};

    map = new google.maps.Map(document.getElementById('map'), {
        center: originco,
        zoom: 15
      });

    var origin_mark = new google.maps.Marker({
        position: originco,
        map: map,
        label: "Origin"
    });

    $("#map").show();
}

$(document).ready(main);