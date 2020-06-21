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
    // Set the bound of Dublin city
    var cityBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(53.00, -6.85),
        new google.maps.LatLng(53.68, -5.90));
    var options = {
        bounds: cityBounds,
        strictBounds: true,
    };
    // Initialise the autocomplete object for two input form
    var autocomplete_start = new google.maps.places.Autocomplete(input_start, options);
    var autocomplete_end = new google.maps.places.Autocomplete(input_end, options);


    // Initialise the datetimepicker's parameters
    $("#datetime_picker").datetimepicker({
        format: "dd MM yyyy - hh:ii",
        autoclose: true, // Auto close the dropdown box when picking finished
        todayBtn: true, // The button pick up current date and time
        minuteStep: 5 // Time step every 5 mins
    });
}


// Listener that call the initMap when the window finished render
google.maps.event.addDomListener(window, 'load', init);