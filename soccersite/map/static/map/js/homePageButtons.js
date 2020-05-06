/*
 homePagebuttons.js provides client-side logic for interacting with buttons on
 the homepage
*/

//blue submit button
function submit() {
  document.getElementById('markerControl').style.fontWeight = "bold";
  document.getElementById('markerControl').disabled = false;
  document.getElementById('zoomControl').disabled = false;
  document.getElementById('heatMapControl').disabled = false;
  if(document.getElementById('noQuerySelected')){
      document.getElementById('noQuerySelected').style.display = "none";
  }
  submitted=true; //declaration found on line 127 in index.html
  $('.loader').show();
}

//helper function for csv download
function parseCell(tableCell){
  var parsedValue = tableCell.textContent;
  parsedValue = parsedValue.replace(/"/g, '""'); //replace all single quote with double quote

  //if value contains comma, new-line or double-quote, enclose in double quotes
  parsedValue = /[",\n]/.test(parsedValue) ? parsedValue.split(',').join(' ') : parsedValue;

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

//add event listeners
document.getElementById("button1").addEventListener("click", submit, false);
document.getElementById("button2").addEventListener("click", csv, false);
