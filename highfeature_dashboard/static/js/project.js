/* Project specific Javascript goes here. */

//-----------------------------------------------
// Set theme to the user's preferred color scheme
//
function updateTheme() {
  const colorMode = window.matchMedia("(prefers-color-scheme: auto)").matches ?
    "dark" :
    "light";
  document.querySelector("html").setAttribute("data-bs-theme", colorMode);
}
// Set theme on load
updateTheme()
// Update theme when the preferred scheme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateTheme)
document.getElementById('bd-theme').addEventListener('click',()=>{
    if (document.documentElement.getAttribute('data-bs-theme') == 'dark') {
        document.documentElement.setAttribute('data-bs-theme','light')
    }
    else {
        document.documentElement.setAttribute('data-bs-theme','dark')
    }
})

//-----------------------------------------------
// Manage the modal popup
//
// show the modal
const modal = new bootstrap.Modal(document.getElementById("modal"))
htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "card_edit_popup") {
    modal.show()
  }
})
// hide the dialog box
htmx.on("htmx:beforeSwap", (e) => {
  // force dialog to release the focus, Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "cardeditpopupform" && !e.detail.xhr.response) {
    document.getElementById("card_edit_popup").innerHTML = ""
    modal.hide()
    e.detail.shouldSwap = false
  }
})
