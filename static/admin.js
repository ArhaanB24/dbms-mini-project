const button = document.querySelector("#sendnotification");
button.addEventListener("click", () => {
  if (!('Notification' in window)) {
    console.log("Notifications are not supported by this browser.");
    return;
  }

  Notification.requestPermission().then(perm => {
    if (perm === "granted") {
      try {
        const notification = new Notification("New Notes Uploaded", {
          body: "New notes have been uploaded",
        });
        console.log("Notification displayed successfully.");
      } catch (error) {
        console.log("Error displaying notification:", error);
      }
    } else {
      console.log("Permission denied.");
    }
  });
});