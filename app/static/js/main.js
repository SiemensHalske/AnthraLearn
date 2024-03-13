// Einfache Funktion zum Umschalten der Sichtbarkeit des Dropdown-Menüs
function toggleDropdown() {
  const dropdownContent = document.querySelector(".dropdown-content");
  dropdownContent.style.display =
    dropdownContent.style.display === "block" ? "none" : "block";
}

// Schließt das Dropdown-Menü, wenn außerhalb geklickt wird
window.onclick = function (event) {
  if (!event.target.matches(".user-profile a")) {
    const dropdowns = document.getElementsByClassName("dropdown-content");
    Array.from(dropdowns).forEach((dropdown) => {
      if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
      }
    });
  }
};

// Verarbeitet Ankerlink-Klicks für interne Umleitungen
$(document).ready(function () {
  $("a[href^='#']").click(function (event) {
    event.preventDefault();
    const page = $(this).attr("href").substring(1) || "home";
    window.location = "/redirect/" + page;
  });
});

// Versucht, mit dem gegebenen Token eine Anfrage zu senden, und erneuert es bei Bedarf
async function fetchWithToken(url, options = {}) {
  try {
    let response = await fetch(url, { ...options, credentials: "include" });

    if (response.status === 401) {
      console.log("Token abgelaufen, versuche zu erneuern...");
      const refreshed = await refreshAccessToken();

      if (refreshed) {
        console.log("Token wurde erneuert, wiederhole Anfrage...");
        response = await fetch(url, { ...options, credentials: "include" });
      }
    }

    return response;
  } catch (error) {
    console.error("Fehler:", error);
    throw new Error("Problem bei der Anfrage oder beim Token-Refresh.");
  }
}

// Erneuert das Access-Token
async function refreshAccessToken() {
  const response = await fetch("/token/refresh", {
    method: "POST",
    credentials: "include",
  });

  if (!response.ok) {
    console.error("Token-Refresh fehlgeschlagen");
    return false;
  }

  console.log("Token erfolgreich erneuert");
  return true;
}

// Beispiel für die Verwendung von fetchWithToken
async function loadData() {
  try {
    const response = await fetchWithToken("deine-api-url");
    if (!response.ok) {
      throw new Error("Netzwerkantwort war nicht ok.");
    }
    const data = await response.json();
    console.log("Daten erhalten:", data);
    // Verarbeite die Daten hier
  } catch (error) {
    console.error("Fehler beim Laden der Daten:", error);
    // Behandle den Fehler, z.B. Benutzer ausloggen oder zur Anmelde-Seite umleiten
  }
}

// Aufruf der loadData Funktion als Beispiel
// loadData();
