// Initialize and add the map
function init() {
    // The location of the centre of Dublin
    var dublin = {lat: 53.3479538, lng: -6.2708115};
    // The map, centered at Uluru
    var map = new google.maps.Map(
        document.getElementById('map'), {zoom: 12, center: dublin});
    // The marker, positioned at Dublin
    var marker = new google.maps.Marker({position: dublin, map: map});


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


    // Initialise the datetimepicker's parameters
    $("#datetime_picker").datetimepicker({
        format: "dd MM yyyy - hh:ii",
        autoclose: true, // Auto close the dropdown box when picking finished
        todayBtn: true, // The button pick up current date and time
        minuteStep: 5 // Time step every 5 mins
    });


    // Get the picked time from datetime picker
    $('#search_sumbit').on('click', function () {
        var depart_time = $('#datetime_picker').datetimepicker('getDate');
        // Timestamp will have a tolerance on second not strictly 00 second, recommending a format later
        depart_time = depart_time.getTime() / 1000;
        var depart_loc = document.getElementById('start_location').value;
        var arrival_loc = document.getElementById('end_location').value;
    });

}


// Listener that call the initMap when the window finished render
google.maps.event.addDomListener(window, 'load', init);

