function submit() {
  location.href = "#map";
}


function admin(){
  window.open('http://127.0.0.1:8000/admin/');
}

function csv(){
  //TODO: flush out csv function to save table to a csv file
}

function about(){
  window.location.href = 'http://127.0.0.1:8000/about'
}


//add event listeners
document.getElementById("button1").addEventListener("click", submit, false);
document.getElementById("button2").addEventListener("click", csv, false);
document.getElementById("button3").addEventListener("click", admin, false);
document.getElementById("button4").addEventListener("click", about, false);
