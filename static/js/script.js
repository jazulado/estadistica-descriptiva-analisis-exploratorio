document.getElementById("btn-moon").onclick = function () {
    halfmoon.toggleDarkMode()
    localStorage.setItem('darkModeOn', halfmoon.darkModeOn);
}

if (localStorage.getItem('darkModeOn') == "yes") {
    halfmoon.toggleDarkMode()
}