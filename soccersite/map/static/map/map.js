function initMap() {
  var laf = {lat: 40.7000662,lng: -75.2103164}
  var map = new google.maps.Map(
    document.getElementByID('map'), {zoom: 4, center: laf})
  );
  var marker = new google.maps.Marker({position: laf, map: map});
}
