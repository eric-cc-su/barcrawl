/**
 * Created by eric on 10/6/15.
 */

function calculate_numbers() {
    var screenheight = window.innerHeight;   //measures the height of the user's screen

    var maincontain = document.getElementById("index_search");
    maincontain.style.marginTop = (screenheight/4) + "px";
    var fluid = document.getElementsByClassName("container-fluid")[0];
    var footerHeight = document.getElementById("footer").scrollHeight;
    fluid.style.height = (screenheight - footerHeight) + "px";
}

function submit_data() {
    var xhr = new XMLHttpRequest();
    var action = $("#bcform").attr("action");
    xhr.open("POST", action, true);
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    request_data = $('#bcform').serialize();
    xhr.send(request_data);

    var i = 0;
    var interval = setInterval(function() {
        i = ++i % 4;
        $("#bcButton").html("Loading "+Array(i+1).join("."));
        $("#title a").html(Array(3-i).join(" ") + Array(i+1).join("~") + " Barcrawl " + Array(i+1).join("~"));
    }, 800);

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            processResponse(xhr.responseText, interval);
        }
    };
}

var main = function() {
    calculate_numbers();

    window.onresize = function() {
        calculate_numbers();
    };

    $("#bcform").on('submit', function(event) {
        event.preventDefault();
        submit_data();
    });

    $("input[name='cities']").on("input", function() {
        if (this.value != '' && $("#bcButton").html() != "Go!") {
            $("#bcButton").html("Go!");
        }
        else if (this.value == '' && $("#bcButton").html() == "Go!") {
            $("#bcButton").html("Skip");
        }
    })
};

function processResponse(responseText, interval) {
    var jsonResponse = JSON.parse(responseText);
    var relinquish = jsonResponse["relinquish"];
    var newField = "input[name='" + relinquish + "']";

    //Reveal new input
    $(newField).show();
    $(newField).prop("disabled",false);
    //Set new form URL
    $("#bcform").prop("action",jsonResponse["action"]);

    if (jsonResponse["action"] == "/onecity/") {
        $("input[name='cities']").hide();
    }
    //update origin_info
    $("input[name='origin_city']").val(jsonResponse["origin_city"]);
    $("input[name='origin_coordinates']").val(jsonResponse["origin_coordinates"]);
    clearInterval(interval); // Stop "loading" message on button

    // bar crawl done
    if (jsonResponse["status"] == "ok") {
        var fluid = document.getElementsByClassName("container-fluid")[0];
        fluid.style.height = "inherit";
        $("#bcButton").hide();
        $("#subtitle").hide();
        $("input").hide();
        $("#route_details").show();
        initMap(jsonResponse["origin_coordinates"]);
        setMarkers(jsonResponse["route_coordinates"], jsonResponse["route_names"], jsonResponse["route_addresses"]);
        $("#index_search").css("margin-top","0");
    }

    $("#title a").html("Barcrawl");
    $("#bcButton").html("Go!");

    if (jsonResponse["relinquish"] == "cities") {
        $("#bcButton").html("Skip");
    }
}


//Initialize a map with the origin location
var map;
function initMap(origin_coordinates) {

    map = new google.maps.Map(document.getElementById('map'), {
        center: origin_coordinates,
      });

    var dimension = Math.min(500, window.innerWidth);
    if (dimension != 500) {
        $("#map").css("height", String(dimension*0.9));
        $("#map").css("width", String(dimension*0.9));
    }
    $("#map").show();
}

function writeStops(names, addresses, index) {
    var li = document.createElement("li");                      // create <li>
    var title = document.createElement("h3");                   // create <h3>
    var t = document.createTextNode(names[index]);              // define h3 text
    var par = document.createElement("p");                      // create <p>
    var tp = document.createTextNode(addresses[index]);    // define p text

    title.appendChild(t);
    par.appendChild(tp);
    li.appendChild(title);
    li.appendChild(par);
    document.getElementById("route_details_ol").appendChild(li);
}

function setMarkers(route, names, addresses) {
    var bounds = new google.maps.LatLngBounds();
    var coordinates = route;
    for (i=0; i < coordinates.length; i++) {
        var marker = new google.maps.Marker({
            position: coordinates[i],
            map: map,
            label: String(i),
            title: names[i]
        });

        var LatLng = new google.maps.LatLng(coordinates[i]["lat"], coordinates[i]["lng"]);
        marker.setMap(map);
        bounds.extend(LatLng);

        writeStops(names, addresses, i);
    }
    writeStops(names, addresses, 0); // Write origin at end
    map.fitBounds(bounds);
}

$(document).ready(main);