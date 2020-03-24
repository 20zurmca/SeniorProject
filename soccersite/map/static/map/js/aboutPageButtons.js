function admin(){
  window.location.href = 'http://127.0.0.1:8000/admin/'
}

function homePage(){
  window.location.href = 'http://127.0.0.1:8000/'
}

function cameronLinkedIn(){
  window.open("https://www.linkedin.com/in/cameron-zurmuhl/", target="_blank");
}

document.getElementById("returnButton").addEventListener("click", homePage, false);
document.getElementById("adminButton").addEventListener("click", admin, false);
document.getElementById("camProfile").addEventListener("click", cameronLinkedIn, false);
