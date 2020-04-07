function submit() {
  selectedColleges           = collegeSelector.options.find("selected", "any"); //from selectors.js
  selectedPositions          = positionSelector.options.find("selected", "any");
  selectedStarterYears       = starterSelector.options.find("selected", "any");
  selectedAllConferenceYears =  allConferenceSelector.options.find("selected", "any");
  let selectedSomething      = (selectedColleges.length > 0 || selectedPositions.length > 0 ||
                                selectedStarterYears.length > 0 || selectedAllConferenceYears.length > 0);
  if(selectedSomething){
      document.getElementById('markerControl').style.fontWeight = "bold";
      document.getElementById('markerControl').disabled = false;
      document.getElementById('zoomControl').disabled = false;
      document.getElementById('heatMapControl').disabled = false;
      if(document.getElementById('noQuerySelected')){
        document.getElementById('noQuerySelected').style.display = "none";
      }
      submitted=true;
      $('.loader').show();
    }
}


function admin(){
  window.open('http://127.0.0.1:8000/admin/');
}

function parseCell(tableCell){
  var parsedValue = tableCell.textContent;
  parsedValue = parsedValue.replace(/"/g, '""'); //replace all single quote with double quote

  //if value contains comma, new-line or double-quote, enclose in double quotes
  parsedValue = /[",\n]/.test(parsedValue) ? '"${parsedValue}"' : parsedValue;

  return parsedValue;
}

function csv(){
  if(!submitted){
    alert("Select data before exporting CSV.");
    return;
  }
  var table = document.getElementById('resultTable');
  var rows  = Array.from(table.querySelectorAll('tr'));

  var longestRow = rows.reduce((l, row) => row.childElementCount > l ? row.childElementCount : l, 0);
  var lines = [];
  var numCols = longestRow;
  for(var row of rows){
    if($(row).is(":hidden")) continue;
    var line = "";

    for(var i = 0; i < numCols; i++){
      if(row.children[i] != undefined){
        line += parseCell(row.children[i]);
      }
      line += (i !== (numCols - 1)) ? "," : "";
    }
    lines.push(line);
  }
  var csvOutput     = lines.join("\n");
  var csvBlob       = new Blob([csvOutput], {type: "text/csv"});
  var blobUrl       = URL.createObjectURL(csvBlob);
  var anchorElement = document.createElement("a");

  anchorElement.href     = blobUrl;
  anchorElement.download = "SoccerQuery.csv";
  anchorElement.click();

  setTimeout(() => {
    URL.revokeObjectURL(blobUrl); //reducing amount of memory used by browser
  }, 500);

}

function about(){
  window.location.href = 'http://127.0.0.1:8000/about'
}


//add event listeners
document.getElementById("button1").addEventListener("click", submit, false);
document.getElementById("button2").addEventListener("click", csv, false);
// document.getElementById("button3").addEventListener("click", admin, false);
// document.getElementById("button4").addEventListener("click", about, false);
