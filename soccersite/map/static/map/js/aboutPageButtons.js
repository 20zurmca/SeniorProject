function admin(){
  window.location.href = 'http://127.0.0.1:8000/admin/'
}

function homePage(){
  window.location.href = 'http://127.0.0.1:8000/'
}

function cameronLinkedIn(){
  window.open("https://www.linkedin.com/in/cameron-zurmuhl/", target="_blank");
}

function josephLinkedIn(){
  window.open("https://www.linkedin.com/in/joseph-teddick-670242191/", target="_blank");
}

function mattLinkedIn(){
  window.open("https://www.linkedin.com/in/matthew-gerber", target="_blank");
}

document.getElementById("camProfile").addEventListener("click", cameronLinkedIn, false);
document.getElementById("josephProfile").addEventListener("click", josephLinkedIn, false);
document.getElementById("mattProfile").addEventListener("click", mattLinkedIn, false);
