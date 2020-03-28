var center_ = {lat: 32.560742, lng: -3.9314364} //somewhere near the Mediterranean Sea

var markers = []; //to be filled based on querie

//test data for demo
var data = [
  {'schoolName' : 'Delbarton School',
   'highSchoolLat': 40.78836,
   'highSchoolLng': -74.531258,
   'numPlayers': 2, //number of players for the query
   'players': [
      { 'rosterYear': 2008,
      'playerNumber': 25,
      'firstName': 'Donnie',
      'lastName': 'Surdoval',
      'year': 'Junior',
      'position1': 'Defender',
      'height': "6'0",
      'weight': 170,
      'homeTown': 'Sparta',
      'stateOrCountry': 'NJ',
      'highSchool': 'Delbarton School',
      'college': 'Dartmouth College',
      'collegeLeague': 'IVY',
      'bioLink': "https://dartmouthsports.com/roster.aspx?rp_id=3259",
      'isStarter': 'Y',
      'accolade': 'Honorable Mention'
      },
      { 'rosterYear': 2013,
      'playerNumber': 31,
      'firstName': 'Greg',
      'lastName': 'Seifert',
      'year': 'Freshman',
      'position1': 'Midfielder',
      'height': "6'0",
      'weight': 180,
      'homeTown': 'Woodland Park',
      'stateOrCountry': 'NJ',
      'highSchool': 'Delbarton School',
      'college': 'Princeton University',
      'collegeLeague': 'IVY',
      'bioLink': "https://dartmouthsports.com/roster.aspx?rp_id=3259",
      'isStarter': 'N',
      'accolade': null
      },
   ] //end player list
  }, 
] //end data list

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
 * The ZoomControl adds a control to zoom to fit the pins displayed
 * This constructor takes the control DIV as an argument.
 * @constructor
 */
 function ZoomControl(controlDiv, map) {
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
   controlUI.title                 = 'Click to zoom to map pins';
   controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
   var controlText = document.createElement('div');
   controlText.style.color        = 'rgb(25,25,25)';
   controlText.style.fontFamily   = 'Roboto,Arial,sans-serif';
   controlText.style.fontSize     = '16px';
   controlText.style.lineHeight   = '39px';
   controlText.style.paddingLeft  = '5px';
   controlText.style.paddingRight = '5px';
   controlText.innerHTML          = 'Auto Zoom';
   controlUI.appendChild(controlText);

   controlUI.addEventListener('click', function() {
    var bounds = new google.maps.LatLngBounds();
    map.fitBounds(bounds);
        for (var i = 0; i < markers.length; i++) {
          bounds.extend(markers[i].getPosition());
        }
        map.fitBounds(bounds);
    });
}



/**
 * The MarkerControl adds a control to the map that toggles pins
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
  controlText.style.fontWeight   = "bold";
  controlText.style.fontSize     = '16px';
  controlText.style.lineHeight   = '39px';
  controlText.style.paddingLeft  = '5px';
  controlText.style.paddingRight = '5px';
  controlText.innerHTML          = 'Toggle Markers';
  controlUI.appendChild(controlText);

  var firstTime = true;
  let clickCount = 0; //counter for toggling bold text
  controlUI.addEventListener('click', function() {
     clickCount++;
     if(clickCount % 2 && !firstTime) {
       controlText.style.fontWeight = "bold";
       for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
       }
     } else {
       controlText.style.fontWeight = "normal";
       firstTime=false;
       for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
       }
     }

     //TODO: implement functionality
   });
}


function initMap() {
  var map = new google.maps.Map(
      document.getElementById('map'), {
        center: center_,
        zoom: 2,
        minZoom: 2,
        restriction: {
            latLngBounds: {
                north: 85,
                south: -85,
                west: -180,
                east: 180
            }
        },
        gestureHandling: 'greedy'
      });

  var centerControlDiv  = document.createElement('div');
  var heatMapControlDiv = document.createElement('div');
  var markerControlDiv  = document.createElement('div');
  var zoomControlDiv  = document.createElement('div');

  var centerControl     = new CenterControl(centerControlDiv, map);
  var heatMapControl    = new HeatMapControl(heatMapControlDiv, map);
  var markerControl     = new MarkerControl(markerControlDiv, map);
  var zoomControl     = new ZoomControl(zoomControlDiv, map);

  centerControlDiv.index  = 1; //index will determine where the control is put in the control block array
  heatMapControlDiv.index = 3;
  markerControlDiv.index  = 4;
  zoomControlDiv.index  = 5;


  map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(centerControlDiv); //center of screen
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(heatMapControlDiv); //top left 3rd position
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(markerControlDiv); //top right fourth position
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(zoomControlDiv); //top left 5th position

  for(var i = 0; i < data.length; i++){
    var pos = {lat: data[i]['highSchoolLat'], lng: data[i]['highSchoolLng']};
    var marker = new google.maps.Marker({
      position: pos,
      map: map,
      title: data[i]['schoolName'],
      label: {
        text: String(data[i]['numPlayers']),
        fontWeight: "bold",
        optimized: false
      },
      animation: google.maps.Animation.DROP
    });
    markers[i] = marker;
    var markerCluster = new MarkerClusterer(map, markers,
      {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
    var contentString = '<div id="content">'+
         '<div id="siteNotice">'+
         '</div>'+
         '<h1 id="firstHeading" class="firstHeading">'+ data[i]['schoolName']+'</h1>'+
         '<div id="bodyContent">'+
         '<p></p>'+
         '</div>'+
         '</div>';

     var infowindow = new google.maps.InfoWindow({
       content: contentString
     });

    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
  }
}
