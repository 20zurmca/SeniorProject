var center_ = {lat: 32.560742, lng: -3.9314364}; //somewhere near the Mediterranean Sea
var map;
var markers = [];
var heatMapData = [];
var heatMap;
var markerCluster;
var firstLoad = true;
var groupedLatLngData = {};
var changeTableOnZoom = false;
var dataTable;
var infowindow;
var clickCounts = [0, 0]; //count clicks for heatmap and marker cluster

function loadData(map, playerData){
  if (firstLoad) {
    infowindow = new google.maps.InfoWindow({
      content: "temp"
    });
  } else {
    infowindow.close();
  }

  if(clickCounts[0] % 2){ //turn heatmap off if on
    document.getElementById('heatMapControl').click();
    document.getElementById('heatMapControl').style.fontWeight = "normal";
  }

  if(clickCounts[1] % 2){ //set markers off
    document.getElementById('markerControl').click();
  }

  clickCounts = [0, 0];
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers.length = 0;; //to be filled based on query
  heatMapData.length = 0;; //data for heatmap
  if(!firstLoad){
    markerCluster.setMap(null);
    markerCluster.clearMarkers();
  }

  groupedLatLngData = {};
  //grouping response data by lat and lng
  for(var i = 0; i < playerData.length; i++){
    lat = playerData[i]['latitude'];
    lng = playerData[i]['longitude'];
    key = String(lat) + lng;
    player = {};
    player['roster_year'] = playerData[i]['roster_year'];
    player['first_name'] = playerData[i]['first_name'];
    player['last_name'] = playerData[i]['last_name'];
    player['position'] = playerData[i]['position'];
    player['heights'] = playerData[i]['heights'];
    player['weights'] = playerData[i]['weights'];
    player['home_town'] = playerData[i]['home_town'];
    player['state_or_country'] = playerData[i]['state_or_country'];
    player['high_school'] = playerData[i]['high_school'];
    player['alternative_school'] = playerData[i]['alternative_school'];
    player['college'] = playerData[i]['college'];
    player['college_league'] = playerData[i]['college_league'];
    player['bio_link'] = playerData[i]['bio_link'];
    player['starter_count'] = playerData[i]['starter_count'];
    player['accolade_count'] = playerData[i]['accolade_count'];

    if(!groupedLatLngData[key]){ //new key found (new lat lng pair)
      groupedLatLngData[key] = {};
      groupedLatLngData[key]['playerCount'] = 1;
      groupedLatLngData[key]['lat']                = playerData[i]['latitude'];
      groupedLatLngData[key]['lng']                = playerData[i]['longitude'];
      groupedLatLngData[key]['hs']                 = playerData[i]['high_school'];
      if (playerData[i]['highschoolcity'] != null) {
        groupedLatLngData[key]['hsCity']             = playerData[i]['highschoolcity'].toLowerCase();
      }
      groupedLatLngData[key]['hsStateOrProvince']  = playerData[i]['highschoolstateorcountry'];
      groupedLatLngData[key]['hsStateOrProvince']  = playerData[i]['highschoolstateorprovince'];
      groupedLatLngData[key]['hsCountry']          = playerData[i]['highschoolcountry'].toLowerCase();
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
      let latitude = groupedLatLngData[highSchool]['lat'];
      let longitude = groupedLatLngData[highSchool]['lng']
      let pos = {lat: latitude, lng: longitude};
      let marker = new google.maps.Marker({
        position: pos,
        map: map,
        title: groupedLatLngData[highSchool]['hs'], //high school name
        label: {
          text: String(groupedLatLngData[highSchool]['playerCount']),
          fontWeight: "bold",
          color: "black"
        },
        number: groupedLatLngData[highSchool]['playerCount'],
        icon: {
          url: "http://maps.google.com/mapfiles/kml/shapes/schools.png",
          scaledSize: new google.maps.Size(35, 35),
          labelOrigin: { x: 16, y: 26}
        },
        animation: google.maps.Animation.DROP
      });

      heatMapData.push({location: new google.maps.LatLng(latitude, longitude), weight: groupedLatLngData[highSchool]['playerCount']});

      var stateOrProvince = groupedLatLngData[highSchool]['hsStateOrProvince'];
      var country = "";

      if (stateOrProvince == null) {
        stateOrProvince = "";
        country = ", " + groupedLatLngData[highSchool]['hsCountry'];
      } else {
        stateOrProvince = ", " + stateOrProvince;
      }

      //building info window
      let contentString = '<div id="content">'+
           '<div id="siteNotice">'+
           '</div>'+
           '<h1 id="firstHeading" class="firstHeading">'+ groupedLatLngData[highSchool]['hs'] +'</h1>'+
           '<div id="bodyContent">'+
           '<p style="text-transform:capitalize">'+groupedLatLngData[highSchool]['hsCity'] +
           stateOrProvince + country + '</p>' + 
           '<p style="text-transform:capitalize">'+ "Student Count: " + groupedLatLngData[highSchool]['playerCount'] +
           '</div>'+
           '</div>';


      marker.addListener('click', function() {
        if (infowindow) {
          infowindow.close();
        }

        infowindow.setContent(contentString);// = contentString;

        infowindow.setPosition(new google.maps.LatLng(latitude, longitude));
        currentInfoWindow = infowindow;

        dt.destroy();
        infowindow.open(map);
        let table = document.getElementById('resultTableBody');
        let player_data = '';
        let key = String(latitude) + longitude;
        //table changes to marker-specific data on click
        for(let i = 0; i < groupedLatLngData[key]['players'].length; i++){
          let association = _findAssociativeIndices(groupedLatLngData[key]['players'][i]['roster_year']);
          let currentBioLink = _getCurrentDataElement(groupedLatLngData[key]['players'][i]['bio_link'], association);
          player_data += '<tr onclick = goToRosterPage("'.concat(currentBioLink).concat('")>');
          player_data += '<td>' + _sortAggregateData(groupedLatLngData[key]['players'][i]['roster_year'])                                 + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['first_name']                                                      + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['last_name']                                                       + '</td>';
          player_data += '<td>' + _getCurrentDataElement(groupedLatLngData[key]['players'][i]['position'], association)                   + '</td>';
          player_data += '<td>' + convertToInches(_getCurrentDataElement(groupedLatLngData[key]['players'][i]['heights'], association))   + '</td>';
          player_data += '<td>' + _getCurrentDataElement(groupedLatLngData[key]['players'][i]['weights'], association)                    + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['starter_count']                                                   + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['accolade_count']                                                  + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['college_league']                                                  + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['college']                                                         + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['home_town']                                                       + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['state_or_country']                                                + '</td>';
          player_data += '<td>' + groupedLatLngData[key]['players'][i]['high_school']                                                     + '</td>';
          player_data += '</tr>';
        }
        table.innerHTML = player_data;
        changeTableOnZoom = true;
        dt = $('#resultTable').DataTable({
          "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
          "scrollX": true
        });
        document.getElementById('resultTable').style.width = '98%';
      });

      markers.push(marker);
    }


    let mcOptions = {
      //styles: clusterStyles,
      gridSize: 45,
      minimumClusterSize: 2,
      imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
    };

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
     $('.loader').hide();
     if(playerData.length!=0) {
     document.location.href = "#map";
     document.getElementById('zoomControl').click();
     } else {
       alert("Query Returned No Results");
     }
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
   controlUI.addEventListener('click', function() {
     if(!controlUI.disabled){
       clickCounts[0] = clickCounts[0] + 1;
       if(clickCounts[0] % 2) {
         controlText.style.fontWeight = "bold";
         heatMap.setMap(map);
         document.querySelector("#map > div > div > div:nth-child(14) > div:nth-child(2) > div:nth-child(1)").click(); //go to satellite mode
         if(!(clickCounts[1] % 2)){ //turn off markers
           document.getElementById('markerControl').click();
         }
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
   controlText.innerHTML          = 'Reset Table';
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
      let table = document.getElementById('resultTableBody');
      let player_data = '';
      //table changes to marker-specific data on click
      if(changeTableOnZoom){
        dt.destroy();
        for(var hs in groupedLatLngData){
          for(let i = 0; i < groupedLatLngData[hs]['players'].length; i++){
            let association = _findAssociativeIndices(groupedLatLngData[hs]['players'][i]['roster_year']);
            let currentBioLink = _getCurrentDataElement(groupedLatLngData[hs]['players'][i]['bio_link'], association);
            player_data += '<tr onclick = goToRosterPage("'.concat(currentBioLink).concat('")>');
            player_data += '<td>' + _sortAggregateData(groupedLatLngData[hs]['players'][i]['roster_year'])                                + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['first_name']                                                     + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['last_name']                                                      + '</td>';
            player_data += '<td>' + _getCurrentDataElement(groupedLatLngData[hs]['players'][i]['position'], association)                  + '</td>';
            player_data += '<td>' + convertToInches(_getCurrentDataElement(groupedLatLngData[hs]['players'][i]['heights'], association))  + '</td>';
            player_data += '<td>' +  _getCurrentDataElement(groupedLatLngData[hs]['players'][i]['weights'], association)                  + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['starter_count']                                                  + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['accolade_count']                                                 + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['college_league']                                                 + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['college']                                                        + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['home_town']                                                      + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['state_or_country']                                               + '</td>';
            player_data += '<td>' + groupedLatLngData[hs]['players'][i]['high_school']                                                    + '</td>';
            player_data += '</tr>';
          }
        }
        table.innerHTML = player_data;
        dt = $('#resultTable').DataTable({
          "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
          "scrollX": true
        });
        changeTableOnZoom = false;
      }
    }
    infowindow.close();
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

  controlUI.addEventListener('click', function() {
    if(!controlUI.disabled){
      clickCounts[1] = clickCounts[1] + 1;

    if(clickCounts[1] % 2 ) {
      controlText.style.fontWeight = "normal";

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
          var mcOptions = {
            gridSize: 45,
            minimumClusterSize: 2,
            imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
          };


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
