/**
 * Created by eric on 10/6/15.
 */


var main = function() {
    var screenheight = window.innerHeight;   //measures the height of the user's screen

    //$("#index_search").css("margin-top", windowheight/3);
    console.log(screenheight);
    var maincontain = document.getElementById("index_search");
    maincontain.style.marginTop = (screenheight/4) + "px";
};

$(document).ready(main);