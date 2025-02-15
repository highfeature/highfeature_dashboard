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
const modal = new bootstrap.Modal(document.getElementById("modal"))
htmx.on("htmx:afterSwap", (e) => {
  // Response targeting #dialog => show the modal
  if (e.detail.target.id == "card_edit_popup") {
    modal.show()
  }
})
htmx.on("htmx:beforeSwap", (e) => {
  // Empty response targeting #dialog => hide the modal
  if (e.detail.target.id == "card_edit_popup" && !e.detail.xhr.response) {
    modal.hide()
    e.detail.shouldSwap = false
  }
})
htmx.on("hidden.bs.modal", () => {
  document.getElementById("card_edit_popup").innerHTML = ""
})
