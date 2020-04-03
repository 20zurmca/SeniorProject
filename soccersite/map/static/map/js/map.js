var center_ = {lat: 32.560742, lng: -3.9314364} //somewhere near the Mediterranean Sea
var map;
var markers = []
var heatMapData = []
var heatMap;
var markerCluster;
var firstLoad = true;

function loadData(map, playerData){
  for (var i = 0; i < markers.length; i++) {
    console.log("setting marker reference to null");
    markers[i].setMap(null);
  }
  markers = []; //to be filled based on query
  heatMapData = []; //data for heatmap
  if(!firstLoad){
    markerCluster.setMap(null);
    markerCluster.clearMarkers();
  }

  var groupedLatLngData = {};

  //grouping response data by lat and lng
  for(var i = 0; i < playerData.length; i++){
    lat = playerData[i]['latitude'];
    lng = playerData[i]['longitude'];
    key = String(lat) + lng
    player = {}
    player['rosterYear'] = playerData[i]['rosterYear'];
    player['playerNumber'] = playerData[i]['playerNumber'];
    player['firstName'] = playerData[i]['firstName'];
    player['lastName'] = playerData[i]['lastName'];
    player['year'] = playerData[i]['year'];
    player['position1'] = playerData[i]['position1'];
    player['height'] = playerData[i]['height'];
    player['weight'] = playerData[i]['weight'];
    player['homeTown'] = playerData[i]['homeTown'];
    player['stateOrCountry'] = playerData[i]['stateOrCountry'];
    player['highSchool'] = playerData[i]['highSchool'];
    player['alternativeSchool'] = playerData[i]['alternativeSchool'];
    player['college'] = playerData[i]['college'];
    player['collegeLeague'] = playerData[i]['collegeLeague'];
    player['bioLink'] = playerData[i]['bioLink'];
    player['isStarter'] = playerData[i]['isStarter'];
    player['accolade'] = playerData[i]['accolade'];

    if(!groupedLatLngData[key]){ //new key found (new lat lng pair)
      groupedLatLngData[key] = {};
      groupedLatLngData[key]['playerCount'] = 1;
      groupedLatLngData[key]['lat'] = playerData[i]['latitude'];
      groupedLatLngData[key]['lng'] = playerData[i]['longitude'];
      groupedLatLngData[key]['hs']  = playerData[i]['highSchool']
      groupedLatLngData[key]['players'] = [];
      players = groupedLatLngData[key]['players'];
      players.push(player)
    } else {
      groupedLatLngData[key]['playerCount'] = groupedLatLngData[key]['playerCount']  + 1;
      players = groupedLatLngData[key]['players'];
      players.push(player);
    }
  }
  //building heatmap and marker data
    for(var highSchool in groupedLatLngData){
      latitude = groupedLatLngData[highSchool]['lat'];
      longitude = groupedLatLngData[highSchool]['lng']
      var pos = {lat: latitude, lng: longitude};
      let marker = new google.maps.Marker({
        position: pos,
        map: map,
        title: groupedLatLngData[highSchool]['hs'], //high school name
        label: {
          text: String(groupedLatLngData[highSchool]['playerCount']),
          fontWeight: "bold"
        },
        number: groupedLatLngData[highSchool]['playerCount'],
        animation: google.maps.Animation.DROP
      });

      heatMapData.push({location: new google.maps.LatLng(latitude, longitude), weight: groupedLatLngData[highSchool]['playerCount']});

      //builiding info window
      var contentString = '<div id="content">'+
           '<div id="siteNotice">'+
           '</div>'+
           '<h1 id="firstHeading" class="firstHeading">'+ groupedLatLngData[highSchool]['hs'] +'</h1>'+
           '<div id="bodyContent">'+
           '<p>'+

           "Roster Year: " +'</p>'+
           '</div>'+
           '</div>';

       var infowindow = new google.maps.InfoWindow({
         content: contentString
       });

      marker.addListener('click', function() {
        infowindow.open(map, marker);
      });

      markers.push(marker);
    }


    var mcOptions = {
      //styles: clusterStyles, 
      gridSize: 45,
      minimumClusterSize: 2,
      imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
    };
    
    //  markerCluster = new MarkerClusterer(map, markers,
    //   {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

    markerCluster = new MarkerClusterer(map, markers, mcOptions);


    markerCluster.setCalculator(function(markers, numStyles){
      var index = 0;
      var count = 0;
      for (var i = 0; i < markers.length; i++) {
        if (markers[i].number) {
          count += markers[i].number;
        } else {
          count++;
        }
      }
      var dv = markers.length;
      while (dv !== 0) {
        dv = parseInt(dv / 10, 10);
        index++;
      }
  
      index = Math.min(index, numStyles);
      return {
        text: count,
        index: index
      };
    });

     heatMap = new google.maps.visualization.HeatmapLayer({
       data: heatMapData
     });
     firstLoad = false;
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
   controlUI.id                    = 'heatMapControl';
   controlUI.disabled              = true;
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

   var clickCount = 0; //counter for toggling bold text
   controlUI.addEventListener('click', function() {
     if(!controlUI.disabled){
       clickCount++;
       if(clickCount % 2) {
         controlText.style.fontWeight = "bold";
         heatMap.setMap(map);
       } else {
         controlText.style.fontWeight = "normal";
         heatMap.setMap(null);
       }
     }
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
   controlUI.id                    = 'zoomControl';
   controlUI.disabled              = true;
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
   controlText.id                 = 'zoomControlText';
   controlUI.appendChild(controlText);

   controlUI.addEventListener('click', function() {
    if(!controlUI.disabled){
      var bounds = new google.maps.LatLngBounds();
      map.fitBounds(bounds);
          for (var i = 0; i < markers.length; i++) {
            bounds.extend(markers[i].getPosition());
          }
          map.fitBounds(bounds);
    }
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
  controlUI.id                    = 'markerControl';
  controlUI.disabled              = true;
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
  controlText.id                 = 'markerControlText';
  controlUI.appendChild(controlText);

  var clickCount = 0; //counter for toggling bold text
  controlUI.addEventListener('click', function() {
    if(!controlUI.disabled){
      clickCount++;

    if(clickCount % 2 ) {
      controlText.style.fontWeight = "normal";
      firstTime=false;

      for (var i = 0; i < markers.length; i++) {
       markers[i].setMap(null);
      }
      markerCluster.setMap(null);
      markerCluster.clearMarkers();

      } else {
          controlText.style.fontWeight = "bold";
          for (var i = 0; i < markers.length; i++) {
           markers[i].setMap(map);
          }
          markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
      }
    }
   });
}


function initMap() {
   map = new google.maps.Map(
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

  var heatMapControlDiv = document.createElement('div');
  var markerControlDiv  = document.createElement('div');
  var zoomControlDiv    = document.createElement('div');

  var heatMapControl    = new HeatMapControl(heatMapControlDiv, map);
  var markerControl     = new MarkerControl(markerControlDiv, map);
  var zoomControl       = new ZoomControl(zoomControlDiv, map);

  heatMapControlDiv.index = 3;
  markerControlDiv.index  = 4;
  zoomControlDiv.index  = 5;

  map.controls[google.maps.ControlPosition.TOP_LEFT].push(heatMapControlDiv); //top left 3rd position
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(markerControlDiv); //top right fourth position
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(zoomControlDiv); //top left 5th position
}
