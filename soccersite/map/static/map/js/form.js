/**
 * getCookie() is used to get the csrftoken for ajax call
*/
var dt;

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

/**
 * _findLatestIndex(roster_year) returns the maped indices of ordered roster_years to the non-ordered
 * roster_years list for a player
 * for a player
 * @param roster_year the string of roster years from the db
 * @return list: list position of the roster years from oldest to most recent
*/
 function _findAssociativeIndices(roster_year){
   let association = []
   let rosterYearArr = roster_year
   let sortedYearArr = roster_year.sort();
   let year = '';
   for(var i = 0; i < roster_year.length; i++){
     association.push(rosterYearArr.indexOf(sortedYearArr[i]));
   }
   return association; //max year's index is at the last index of association array
 }

 /**
  * _sortAggregateData sorts an array aggregate type from our db
  * @param data the ArrayAggregate
  */
 function _sortAggregateData(data){
   return data.sort();
 }

 /**
  * _getCurrentDataElement(data, currentIndex) gets most current entry of an
  * an array aggregate type by using the currentIndex acquired from _findLatestIndex(roster_year).
  * If the most current entry is null, then return the max element to display
  * @param data the ArrayAggregate data
  * @param association the index association arrray of the roster_year
 */
 function _getCurrentDataElement(data, association){
   let d = data;
   if(d[association[association.length-1]]){ //if there is an entry correlating to max roster_year
     return d[association[association.length-1]];
   } else {
     for(var i = association.length - 2; i >= 0; i--){ //find most recent association
       if(d[association[i]]){
         return d[association[i]];
       }
     }
   }
   return ''; //all null in the data
 }

$(document).on('submit', '#filterForm', function(e){
  e.preventDefault(); //prevent refresh
  selectedColleges           = collegeSelector.options.find("selected", "any"); //from selectors.js
  selectedPositions          = positionSelector.options.find("selected", "any");
  selectedStarterYears       = starterSelector.options.find("selected", "any");
  selectedAllConferenceYears =  allConferenceSelector.options.find("selected", "any");
  let selectedSomething      = (selectedColleges.length > 0 || selectedPositions.length > 0 ||
                                selectedStarterYears.length > 0 || selectedAllConferenceYears.length > 0);
  if(!selectedSomething){
    alert("Select at least one drop down to query.");
  } else {
    $.ajaxSetup({
           headers: { "X-CSRFToken": getCookie("csrftoken") }
       });
    $.ajax({
      type: 'POST',
      url: window.location,
      data: { json_data: JSON.stringify({
        collegeLeagues:$('#collegeLeagueSelector').val(),
        colleges:$('#collegeSelector').val(),
        positions:$('#positionSelector').val(),
        starterYears:$('#starterSelector').val(),
        allConferenceYears:$('#allConferenceSelector').val()
      })},
      success:function(response){
        loadData(map, response['players']); //loading data in map.js
        var player_data = '';
        if(dt){
          dt.destroy();
        }

        $.each(response['players'], function(key, value){
          let association = _findAssociativeIndices(value.roster_year);
          player_data += '<tr>';
          player_data += '<td>' + _sortAggregateData(value.roster_year)                + '</td>';
          player_data += '<td>' + value.first_name                                     + '</td>';
          player_data += '<td>' + value.last_name                                      + '</td>';
          player_data += '<td>' + _getCurrentDataElement(value.position, association)  + '</td>';
          player_data += '<td>' + _getCurrentDataElement(value.heights, association)   + '</td>';
          player_data += '<td>' + _getCurrentDataElement(value.weights, association)   + '</td>';
          player_data += '<td>' + value.starter_count                                  + '</td>';
          player_data += '<td>' + value.accolade_count                                 + '</td>';
          player_data += '<td>' + value.college_league                                 + '</td>';
          player_data += '<td>' + value.college                                        + '</td>';
          player_data += '<td>' + value.home_town                                      + '</td>';
          player_data += '<td>' + value.state_or_country                               + '</td>';
          player_data += '<td>' + value.high_school                                    + '</td>';
          player_data += '</tr>';
        });
        document.getElementById('resultTableBody').innerHTML = player_data;
        dt = $('#resultTable').DataTable({
          "lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
          "scrollX": true
        });
      },
      error:function(){
        console.log("Error with form submission");
      }
    });
  }
});
