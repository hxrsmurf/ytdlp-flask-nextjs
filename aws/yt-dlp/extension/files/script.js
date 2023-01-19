// Zoom constants. Define Max, Min, increment and default values
const ZOOM_INCREMENT = 0.2;
const MAX_ZOOM = 5;
const MIN_ZOOM = 0.3;
const DEFAULT_ZOOM = 1;

function getCurrentWindowTabs() {
  return browser.tabs.query({ currentWindow: true });
}

function queryAPI(url) {
  fetch("https://api-yt.homelabwithkevin.com/?url=" + url)
    .then((data) => {
      console.log(data);
    })
    .catch(() => {
      console.log("Error!");
    });
}

function notification(url) {
  const title = browser.i18n.getMessage("notificationTitle");
  browser.notifications.create({
    type: "basic",
    title: "Saved Url",
    message: url,
  });
}

document.addEventListener("click", (e) => {
  function callOnActiveTab(callback) {
    getCurrentWindowTabs().then((tabs) => {
      for (let tab of tabs) {
        if (tab.active) {
          console.log(tab.url);
          notification(tab.url);
          queryAPI(tab.url);
          callback(tab, tabs);
        }
      }
    });
  }

  if (e.target.id === "save-url") {
    callOnActiveTab((tab, tabs) => {});
  }
  e.preventDefault();
});