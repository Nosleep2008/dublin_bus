// Initialize and add the map


function init() {
    // Get the weather of Dublin City
    getWeather();

    // The location of the centre of Dublin
    var dublin = {lat: 53.3479538, lng: -6.2708115};
    // The map, centered at Uluru
    var map = new google.maps.Map(
        document.getElementById('map'), {zoom: 12, center: dublin});
    // The marker, positioned at Dublin(no need now)
    // var marker = new google.maps.Marker({position: dublin, map: map});
    // Initialise the direction service
    var directionsRenderer = new google.maps.DirectionsRenderer();
    var directionsService = new google.maps.DirectionsService();
    // Render the map and display the route
    directionsRenderer.setMap(map);
    // Show the route on the right panel
    // directionsRenderer.setPanel(document.getElementById("right-panel"));


    // Get input from two input form
    var input_start = document.getElementById('start_location');
    var input_end = document.getElementById('end_location');
    // Initialise the autocomplete object for two input form
    var autocomplete_start = new google.maps.places.Autocomplete(input_start);
    var autocomplete_end = new google.maps.places.Autocomplete(input_end);
    // Bind the map's bounds (viewport) property to the autocomplete object,
    // so that the autocomplete requests use the current map bounds for the
    // bounds option in the request.
    autocomplete_start.bindTo('bounds', map);
    autocomplete_end.bindTo('bounds', map);


    // Initialise the datetime picker's parameters
    $("#datetime_picker").datetimepicker({
        format: "dd MM yyyy - hh:ii",
        autoclose: true, // Auto close the dropdown box when picking finished
        todayBtn: true, // The button pick up current date and time
        minuteStep: 5 // Time step every 5 mins
    });


    // Submit button upload the data
    $('#search_sumbit').on('click', function () {
        // Get timestamp from datetime picker
        var depart_time = $('#datetime_picker').datetimepicker('getDate');
        // Timestamp will have a tolerance on second not strictly 00 second, recommending a format later(no need now)
        // depart_time = depart_time.getTime() / 1000;

        // Call the function to generate the possible route
        calculateAndDisplayRoute(directionsService, directionsRenderer);

        // Handle Asynchronous problem
        setTimeout(function () {
            console.log(JSONallSteps);
            // AJAX send the POST request and receive the response from Django
            $.ajax({
                type: 'POST', // POST request
                url: "/route/", // Sends post request to the url '/route', which calls a function in views.py

                // Send the formatted JSON file to Django
                data: {
                    'csrfmiddlewaretoken': "{{ csrf_token }}",
                    'routeInfo': JSONallSteps
                },


                // Get response from Django
                success: function (response) {
                    console.log('success');
                    console.log(response);
                    estimateResultTable(response);
                },
            });
        }, 1000);

        return false; // Set false to prevent the form being submitted again

    });

}

function favourite() {
    var username = document.getElementById("userId").value;
    var start = document.getElementById('start_location').value;
    var end = document.getElementById('end_location').value;

    $.ajax({
        type: 'POST',
        url: "/favourite/",
        data: {
            'csrfmiddlewaretoken': "{{ csrf_token }}",
            'username': username,
            'start': start,
            'end': end
        },
        success: function (response) {
            console.log('success');
            console.log(response);
            FavouriteTable(response);
        },
    });
}

function showFavourite() {
    var username = document.getElementById("userId").value;

    $.ajax({
        type: 'POST',
        url: "/showFavourite/",
        data: {
            'csrfmiddlewaretoken': "{{ csrf_token }}",
            'username': username,
        },
        success: function (response) {
            FavouriteTable(response);
        },
    });
}

function favourite_select(index) {
    var start_str = 'start' + index.toString();
    var end_str = 'end' + index.toString();

    var start = document.getElementById(start_str).innerText;
    var end = document.getElementById(end_str).innerText;


    document.getElementById('start_location').value = start;
    document.getElementById('end_location').value = end;


}

function favourite_delete(index) {

    favourite_select(index);

    var username = document.getElementById("userId").value;
    var start = document.getElementById('start_location').value;
    var end = document.getElementById('end_location').value;

    if (start != null && end != null) {
        $.ajax({
            type: 'POST',
            url: "/deleteFavourite/",
            data: {
                'csrfmiddlewaretoken': "{{ csrf_token }}",
                'username': username,
                'start': start,
                'end': end
            },
            success: function (response) {
                console.log('success');
                console.log(response);
                FavouriteTable(response);
            },
        });

        document.getElementById('start_location').value = "";
        document.getElementById('end_location').value = "";
    }

}


function drawChart() {
    a = parseInt(window.a)
    b = parseInt(window.b)
    c = parseInt(window.c)
    google.load('visualization', '1.0', {'packages': ['corechart']});
    var data = google.visualization.arrayToDataTable([
        ['Duration', 'Time'],
        ['walkingTime', a],
        ['transitTime', b],
        ['totalEstimateWaitingTime', c]
    ]);

    var options = {
        title: 'Percentage Of Travel Time'
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
}

function FavouriteTable(response) {
    var str = "";
    str += "<table class=\"table\">" +
        "<caption>Favourite Route</caption>\n" +
        "<thead>" +
        "<tr>" +
        "<th>ID</th>" +
        "<th>Origin</th>" +
        "<th>Destination</th>" +
        "<th>Select</th>"
    "</tr>" + "</thead>" + "<tbody>";
    favourite_routes = response[0]['favourite'];
    favourite_routes.forEach(function (route, index) {
        var index_table = index + 1;
        str += "<tr>";
        str += "<td>" + index_table + "</td>" +
            "<td id='start" + index_table + "'>" + route[0] + "</td>" +
            "<td id='end" + index_table + "'>" + route[1] + "</td>" +
            "<td><button class=\"btn btn-primary\" onclick=\"favourite_select(" + index_table + ")\">Select</button></td>" +
            "<td><button class=\"btn btn-primary\" onclick=\"favourite_delete(" + index_table + ")\">Delete</button></td>";
        str += "</tr>";
    });
    str += "</tbody></table>";
    $("#favouriteRoutes").html(str);
}

function estimateResultTable(response) {
    response = response[0];
    window.a = response['walkingTime'];
    window.b = response['transitTime'];
    window.c = response['totalEstimateWaitingTime'];
    var str = "<script type = 'text/javascript'>\n" +
        "      google.charts.load('current', {'packages':['corechart']});\n" +
        "      google.charts.setOnLoadCallback(drawChart);\n" +
        "      </script>";

    str += "<p> Walking Distance: " + response['walkingDistance'] + " m</p>";
    str += "<p> Total Walking Time: " + response['walkingTime'] + " s</p>";
    str += "<p> Total TransitTime: " + response['transitTime'] + " s</p>";
    str += "<p> Total Estimate Waiting Time: " + response['totalEstimateWaitingTime'] + " s</p>";
    str += "<table class=\"table\">" +
        "<caption>Transit Info</caption>\n" +
        "<thead>" +
        "<tr>" +
        "<th>Route Name</th>" +
        "<th>Estimated Arrival Time</th>" +
        "<th>Estimated Waiting Time</th>"
    "</tr>" +
    "</thead>" + "<tbody>";
    response['stepsInfo'].forEach(function (data, index) {
        if (data['travelMode'] == "BUS" || data['travelMode'] == "TRAM") {
            str += "<tr>";
            str += "<td>" + data['routeName'] + "</td><td>" + data['transitArrivalTime'] + "</td><td>" + data['estimateWaitingTime'] + "</td>";
            str += "</tr>";
        }
    })
    str += "</tbody></table>";
    $("#detailResult").html(str);

}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    // Get locations of start and end from input box
    var start = document.getElementById('start_location').value;
    var end = document.getElementById('end_location').value;
    // It is a date object
    var depart_time = $('#datetime_picker').datetimepicker('getDate');
    var request = {
        origin: start,
        destination: end,
        // default travelMode is transit
        travelMode: "TRANSIT",
        transitOptions: {
            // Set the depart time
            departureTime: depart_time,
        },
    };
    directionsService.route(request, function (response, status) {
            if (status === "OK") {
                // Render and display the route on the map
                directionsRenderer.setDirections(response);

                // Handle the textual display of directions as a series of steps
                directionsRenderer.setPanel(document.getElementById('directionsPanel'));

                // Check the response
                console.log(response);
                // Origin and destination address
                originAddress = response.request.destination.query;
                destinationAddress = response.request.destination.query;
                // console.log(originAddress);

                // Pick the first (best) route from the given request
                bestRoute = response.routes[0];
                // The transit steps in the bestRoute
                bestRoute = bestRoute.legs[0];

                // The steps number of whole route
                transitStep = bestRoute.steps
                stepNum = transitStep.length;

                // Initialise the dictionary and assign the origin and destination
                var routeDict = {};
                routeDict['departTime'] = response.request.transitOptions.departureTime;
                routeDict['originAddress'] = originAddress;
                routeDict['destinationAddress'] = destinationAddress;

                // Initialise the list
                var allSteps = [];

                // iterate each step to get the information needed
                transitStep.forEach(function (data, index) {
                    // Initialise the dictionary stored each step info
                    var stepDict = {};

                    // Public variable (can be used in any transit mode)
                    // Distance
                    stepDistance = data.distance;
                    // Google estimated duration
                    googleDuration = data.duration;

                    // Travel mode
                    if (data.travel_mode == "WALKING") {
                        // Walking mode
                        stepDict['travelMode'] = "WALKING";
                        stepDict['distance'] = stepDistance;
                        stepDict['googleDuration'] = googleDuration;
                    } else {
                        // public variable of Tram and Bus mode
                        // Google arrival time and duration estimation
                        var googleDepartTime = {};
                        googleDepartTime['text'] = data.transit.departure_time.text; // When the bus comes = when customer departs
                        googleDepartTime['value'] = data.transit.departure_time.value; //value is a date object
                        // Line name
                        lineName = data.transit.line.short_name;

                        if (data.transit.line.vehicle.type == "TRAM") {
                            // Tram (luas) mode
                            stepDict['travelMode'] = "TRAM";
                            stepDict['lineName'] = lineName;
                            stepDict['distance'] = stepDistance;
                            stepDict['startStop'] = data.transit.departure_stop.name; // no stop id only name for tram
                            stepDict['endStop'] = data.transit.arrival_stop.name; // no stop id only name for tram
                            stepDict['googleDepart'] = googleDepartTime;
                            stepDict['googleDuration'] = googleDuration;
                        } else {
                            // Bus mode
                            stepDict['travelMode'] = "BUS";
                            stepDict['lineName'] = lineName;
                            stepDict['distance'] = stepDistance;
                            stepDict['startStop'] = {
                                // split the origin string like Westmoreland Street, stop 317
                                // Warning: Some stop may not return a stop with stop id
                                // Both name and id keys matching is recommended
                                'name': data.transit.departure_stop.name.split(',')[0],
                                'id': data.transit.departure_stop.name.split('stop ')[1]
                            };
                            stepDict['endStop'] = {
                                'name': data.transit.arrival_stop.name.split(',')[0],
                                'id': data.transit.arrival_stop.name.split('stop ')[1]
                            };
                            stepDict['googleDepart'] = googleDepartTime;
                            stepDict['googleDuration'] = googleDuration;
                        }
                    }
                    // Push dict into given list
                    allSteps.push(stepDict);
                })
                // check the step list
                // console.log(allSteps);
                routeDict['steps'] = allSteps;
                // Jsonify the list
                JSONallSteps = JSON.stringify(routeDict);
            } else {
                // Alert the wrong input
                window.alert("It seems something is wrong. Please check the input location and time. (Autocomplete is recommended).");
            }
        }
    );
}

function getWeather() {
    var cityName = "Dublin"
    var OPEN_WEATHER_API = "ae1cb5df0561ea9915f81e08ce8299fc"
    var url = "http://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + OPEN_WEATHER_API;

    return fetch(url).then(function (response) {
        return response.json();
    }).then(function (infoJson) {
        var weather_main = infoJson["weather"][0]["main"];
        var temper = Math.round(infoJson["main"]["temp"] - 273);
        var icon = "http://openweathermap.org/img/wn/" + infoJson["weather"][0]["icon"] + "@2x.png";
        // console.log(weather_main, temper, icon);
        var str="<img src=" + icon + ">" + "<br>";
        str += "<p>Weather:"+ weather_main +"</p>";
        str += "<p>Temperature:"+ temper +"°C</p>";
        $("#show_weather").html(str);
    })
}


// Listener that call the initMap when the window finished render
google.maps.event.addDomListener(window, 'load', init);

