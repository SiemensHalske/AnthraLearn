function toggleDropdown() {
  document.querySelector(".dropdown-content").style.display = "block";
}
// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
  if (!event.target.matches(".user-profile a")) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.style.display === "block") {
        openDropdown.style.display = "none";
      }
    }
  }
};
