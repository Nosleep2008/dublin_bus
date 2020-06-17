

// Initialize and add the map
function initMap() {
  // The location of Uluru
 var uluru = {lat: 53.3479538, lng: -6.2708115};
  // The map, centered at Uluru
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 12, center: uluru});
  // The marker, positioned at Uluru
  var marker = new google.maps.Marker({position: uluru, map: map});
}

