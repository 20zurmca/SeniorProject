
var center_ = {lat: 32.560742, lng: -3.9314364} //somewhere near the Mediterranean Sea

/**
 * The CenterControl adds a control to the map that recenters the map
 * This constructor takes the control DIV as an argument.
 * @constructor
 */
 function CenterControl(controlDiv, map) {

   // Set CSS for the control border.
   var controlUI = document.createElement('div');
   controlUI.style.backgroundColor = '#fff';
   controlUI.style.border          = '2px solid #fff';
   controlUI.style.borderRadius    = '3px';
   controlUI.style.boxShadow       = '0 2px 6px rgba(0,0,0,.3)';
   controlUI.style.cursor          = 'pointer';
   controlUI.style.marginBottom    = '22px';
   controlUI.style.textAlign       = 'center';
   controlUI.title                 = 'Click to recenter the map';
   controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
   var controlText = document.createElement('div');
   controlText.style.color        = 'rgb(25,25,25)';
   controlText.style.fontFamily   = 'Roboto,Arial,sans-serif';
   controlText.style.fontSize     = '16px';
   controlText.style.lineHeight   = '38px';
   controlText.style.paddingLeft  = '5px';
   controlText.style.paddingRight = '5px';
   controlText.innerHTML          = 'Center Map';
   controlUI.appendChild(controlText);

   // recenters the maps upon click.
   controlUI.addEventListener('click', function() {
      map.setCenter(center_);
      map.setZoom(2);
    });
}

/**
 * The HeatMapControl adds a control to the map that toggles a heat map
 * This constructor takes the control DIV as an argument.
 * @constructor
 */
 function HeatMapControl(controlDiv, map) {

   // Set CSS for the control border.
   var controlUI = document.createElement('div');
   controlUI.style.backgroundColor = '#fff';
   controlUI.style.border          = '2px solid #fff';
   controlUI.style.borderRadius    = '3px';
   controlUI.style.boxShadow       = '0 2px 6px rgba(0,0,0,.3)';
   controlUI.style.cursor          = 'pointer';
   controlUI.style.marginBottom    = '22px';
   controlUI.style.marginTop       = '10px';
   controlUI.style.textAlign       = 'center';
   controlUI.style.display         = 'inline-block';
   controlUI.style.height          = '39px';
   controlUI.title                 = 'Click to toggle the heat map';
   controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
   var controlText = document.createElement('div');
   controlText.style.color        = 'rgb(25,25,25)';
   controlText.style.fontFamily   = 'Roboto,Arial,sans-serif';
   controlText.style.fontSize     = '16px';
   controlText.style.lineHeight   = '38px';
   controlText.style.paddingLeft  = '5px';
   controlText.style.paddingRight = '5px';
   controlText.innerHTML          = 'Toggle Heat Map';
   controlUI.appendChild(controlText);

   let clickCount = 0; //counter for toggling bold text
   controlUI.addEventListener('click', function() {
     clickCount++;
     if(clickCount % 2) {
       controlText.style.fontWeight = "bold";
     } else {
       controlText.style.fontWeight = "normal";
     }
      //TODO: implement functionality
    });
}

/**
 * The HeatMapControl adds a control to the map that toggles pins
 * This constructor takes the control DIV as an argument.
 * @constructor
 */
 function MarkerControl(controlDiv, map) {
   // Set CSS for the control border.
   var controlUI = document.createElement('div');
   controlUI.style.backgroundColor = '#fff';
   controlUI.style.border          = '2px solid #fff';
   controlUI.style.borderRadius    = '3px';
   controlUI.style.boxShadow       = '0 2px 6px rgba(0,0,0,.3)';
   controlUI.style.cursor          = 'pointer';
   controlUI.style.marginBottom    = '22px';
   controlUI.style.marginTop       = '10px';
   controlUI.style.marginLeft      = '3px';
   controlUI.style.textAlign       = 'center';
   controlUI.style.display         = 'inline-block';
   controlUI.style.height          = '39px';
   controlUI.title                 = 'Click to toggle map pins';
   controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
   var controlText = document.createElement('div');
   controlText.style.color        = 'rgb(25,25,25)';
   controlText.style.fontFamily   = 'Roboto,Arial,sans-serif';
   controlText.style.fontSize     = '16px';
   controlText.style.lineHeight   = '39px';
   controlText.style.paddingLeft  = '5px';
   controlText.style.paddingRight = '5px';
   controlText.innerHTML          = 'Toggle Markers';
   controlUI.appendChild(controlText);

   let clickCount = 0; //counter for toggling bold text
   controlUI.addEventListener('click', function() {
      clickCount++;
      if(clickCount % 2) {
        controlText.style.fontWeight = "bold";
      } else {
        controlText.style.fontWeight = "normal";
      }

      //TODO: implement functionality
    });
}

function initMap() {
  var map = new google.maps.Map(
      document.getElementById('map'), {
        center: center_,
        zoom: 2,
        gestureHandling: 'greedy'
      });

  var centerControlDiv  = document.createElement('div');
  var heatMapControlDiv = document.createElement('div');
  var markerControlDiv  = document.createElement('div');
  var centerControl     = new CenterControl(centerControlDiv, map);
  var heatMapControl    = new HeatMapControl(heatMapControlDiv, map);
  var markerControl     = new MarkerControl(markerControlDiv, map);

  centerControlDiv.index  = 1; //index will determine where the control is put in the control block array
  heatMapControlDiv.index = 3;
  markerControlDiv.index  = 4;
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv); //center of screen
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(heatMapControlDiv); //top left 3rd position
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(markerControlDiv); //top right fourth position
}
