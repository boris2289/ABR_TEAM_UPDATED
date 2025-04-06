function scroll_to_end(){

  document.addEventListener("DOMContentLoaded", function() {

    const resolutionButtons = document.querySelectorAll(".resolution_button button");

    if (resolutionButtons.length > 0) {
      const next_step=document.getElementById('next')
      next_step.scrollIntoView({behavior:'smooth'});
    }
  });
}
let luck=false
function start_point() {
        document.getElementById("start").scrollIntoView({ behavior: 'smooth' });
    }

function empty_alert_show() {
      alert("Input link")
}
function age_alert_show() {
  alert("This video is age restricted")
}
function congr(){
    alert('Downloading..')
}