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

            //Reveal new input
            $(newField).show();
            $(newField).prop("disabled",false);
            //Set new form URL
            $("#bcform").prop("action",jsonResponse["action"]);
            //update origin_info
            $("input[name='origin_city']").val(jsonResponse["origin_city"]);
            $("input[name='origin_coordinates']").val(jsonResponse["origin_coordinates"]);
            clearInterval(interval);
            if (jsonResponse["status"] == "ok") {
                $("#bcButton").hide();
                //console.log(jsonResponse["route_coordinates"]);
                initMap(jsonResponse["origin_coordinates"]);
                setMarkers(jsonResponse["route_coordinates"], jsonResponse["route_names"]);
                $("input").hide();
                $("#index_search").css("margin-top","0");
            }
            $("#bcButton").html("Go!");
        }
    };
    //console.log("ajax'd");
}

var main = function() {
    var screenheight = window.innerHeight;   //measures the height of the user's screen
    var screenWidth = window.innerWidth;


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
function initMap(origin_coordinates) {

    map = new google.maps.Map(document.getElementById('map'), {
        center: origin_coordinates,
      });

    /*
    var origin_mark = new google.maps.Marker({
        position: origin_coordinates,
        map: map,
        label: "Origin"
    });
    */
    $("#map").show();
}

function setMarkers(route, names) {
    var bounds = new google.maps.LatLngBounds();
    var coordinates = route;
    //console.log(coordinates);
    for (i=0; i < coordinates.length; i++) {
        var marker = new google.maps.Marker({
            position: coordinates[i],
            map: map,
            label: String(i),
            title: names[i]
        });

        //console.log(coordinates[i]["lat"], coordinates[i]["lng"]);
        var LatLng = new google.maps.LatLng(coordinates[i]["lat"], coordinates[i]["lng"]);
        marker.setMap(map);
        bounds.extend(LatLng);
    }

    //console.log({lat: coordinates[-1]["lat"], lng: coordinates[-1]["lng"]});
    //var origin = google.maps.LatLng(coordinates[0]["lat"], coordinates[0]["lng"]);
    //var last = google.maps.LatLng(coordinates[-1]["lat"], coordinates[-1]["lng"]);

    map.fitBounds(bounds);

    //map.setZoom(12);
}

$(document).ready(main);