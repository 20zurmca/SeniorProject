function initMap() {
  var map = new google.maps.Map(
      document.getElementById('map'), {
        center: {lat:32.560742, lng: -3.9314364},
        zoom: 2,
        gestureHandling: 'greedy'
      });
}
