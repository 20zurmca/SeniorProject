/**
 * getCookie() is used to get the csrftoken for ajax call
*/
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

$(document).on('submit', '#filterForm', function(e){
  e.preventDefault(); //prevent refresh
  selectedColleges = collegeSelector.options.find("selected", "any"); //from selectors.js
  if(selectedColleges.length == 0){
    alert("Select at least one college to query.");
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
        $.each(response['players'], function(key, value){
          player_data += '<tr>';
          player_data += '<td>' + value.rosterYear     + '</td>';
          player_data += '<td>' + value.firstName      + '</td>';
          player_data += '<td>' + value.lastName       + '</td>';
          player_data += '<td>' + value.year           + '</td>';
          player_data += '<td>' + value.position1      + '</td>';
          player_data += '<td>' + "will implement"     + '</td>';
          player_data += '<td>' + "will implement"     + '</td>';
          player_data += '<td>' + value.collegeLeague  + '</td>';
          player_data += '<td>' + value.college        + '</td>';
          player_data += '<td>' + value.homeTown       + '</td>';
          player_data += '<td>' + value.stateOrCountry + '</td>';
          player_data += '<td>' + value.highSchool     + '</td>';
          player_data += '</tr>';
        });
        document.getElementById('resultTableBody').innerHTML = player_data;
      },
      error:function(){
        console.log("Error with form submission");
      }
    });
  }
});
