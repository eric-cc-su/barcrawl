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
        if (window.innerWidth > 768) {
            $("#title a").html(Array(3-i).join(" ") + Array(i+1).join("~") + " Barcrawl " + Array(i+1).join("~"));
        }
    }, 800);

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                processResponse(xhr.responseText, interval);
            }
            else if (xhr.status == 500) {
                alert("Sorry! This is an internal server error 500. Please try different inputs and report " +
                    "the issue to github.com/eric-cc-su/barcrawl");
                window.location.reload();
            }
        }
    };
}

var main = function() {
    calculate_numbers();

    window.onresize = function() {
        if (window.innerWidth > 768 && $("#map").css("display") == "none") {
            calculate_numbers();
        }
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
        mapDirections(createLatLng(jsonResponse["route_coordinates"]));
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
var directionsService;

function initMap(origin_coordinates) {

    map = new google.maps.Map(document.getElementById('map'), {
        center: origin_coordinates,
      });
    directionsService = new google.maps.DirectionsService();
    /*
    directionsRender = new google.maps.DirectionsRenderer({

        suppressMarkers: true
    });
    */

    var dimension = Math.min(500, window.innerWidth);
    if (dimension != 500) {
        $("#map").css("height", String(dimension*0.9));
        $("#map").css("width", String(dimension*0.9));
    }
    //directionsRender.setMap(map);
    $("#map").show();
}

function writeStops(names, addresses, index) {
    var li = document.createElement("li");                      // create <li>
    var title = document.createElement("h3");                   // create <h3>
    var t = document.createTextNode(names[index]);              // define h3 text
    var par = document.createElement("p");                      // create <p>
    var tp = document.createTextNode(addresses[index]);         // define p text
    var route_list = document.getElementById("route_details_ul");

    title.appendChild(t);
    par.appendChild(tp);
    li.appendChild(title);
    li.appendChild(par);
    route_list.appendChild(li);
    route_list.appendChild(document.createElement("hr"));
}

// Defines and sets the markers
function setMarkers(route, names, addresses) {
    var bounds = new google.maps.LatLngBounds();
    document.getElementById("route_details_ul").appendChild(
        document.createElement("hr"));
    for (i=0; i < route.length; i++) {
        var marker = new google.maps.Marker({
            clickable: true,
            position: route[i],
            map: map,
            label: String.fromCharCode(65+i),
            title: names[i]
        });

        var LatLng = new google.maps.LatLng(route[i]["lat"], route[i]["lng"]);
        marker.setMap(map);
        bounds.extend(LatLng);

        writeStops(names, addresses, i);
    }
    writeStops(names, addresses, 0); // Write origin at end
    map.fitBounds(bounds);
}

//Gets jsonResponse of route and converts to an array of LatLng objects
function createLatLng(route) {
    var LatLng = [];
    for (var i = 0; i < route.length; i++) {
        var lt = new google.maps.LatLng(route[i]["lat"], route[i]["lng"]);
        LatLng.push(lt);
    }
    return LatLng;
}

// Render route to map
function renderDirections(results) {
    var renderer = new google.maps.DirectionsRenderer({
            suppressMarkers: true
        });
    renderer.setMap(map);
    renderer.setDirections(results);
}

// Send requests to Google Maps Directions service to draw route on map
function mapDirections(route) {
    var waypts = [];

    //Add the origin to the end to finish loop
    route.push(route[0]);

    //number to track the route index we are at (needed if route length > 8)
    var tracking = 0;
    for (var i = 0; i < Math.ceil(route.length / 8); i++) {
        //Slice route into size-8 lists (due to GMaps constraints on waypoints)
        waypts = [];
        var sliced = route.slice(tracking, ((i+1) * 8));

        //construct waypoints
        for (var j = tracking; j < ((i+1) * 8); j++) {
            if (route[j]) {
                waypts.push({
                    location: route[j],
                    stopover: true
                });
            }
            else {
                break;
            }
        }

        //construct request
        var request = {
            origin: sliced[0],
            destination: sliced[sliced.length - 1],
            waypoints: waypts,
            travelMode: google.maps.TravelMode.DRIVING
        };

        //execute request
        directionsService.route(request, function (result, status) {
            console.log(result);
            if (status == google.maps.DirectionsStatus.OK) {
                renderDirections(result);
            }
            else {
                console.log(status);
            }
        });
        //update the tracking integer
        tracking = ((i+1) * 8) - 1;
    }
}

$(document).ready(main);
