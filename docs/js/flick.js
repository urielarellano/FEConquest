waitForElement("#full-stats", (stats) => {
  let startX = 0;
  let currentX = 0;
  let isDragging = false;

  stats.addEventListener("mousedown", startDrag);
  stats.addEventListener("touchstart", startDrag);

  function startDrag(e) {
    console.log("Drag started");
    isDragging = true;
    startX = e.type === "touchstart" ? e.touches[0].clientX : e.clientX;

    window.addEventListener("mousemove", onDrag);
    window.addEventListener("mouseup", endDrag);
    window.addEventListener("touchmove", onDrag);
    window.addEventListener("touchend", endDrag);
  }

  function onDrag(e) {
    if (!isDragging) return;
    const clientX = e.type === "touchmove" ? e.touches[0].clientX : e.clientX;
    currentX = clientX - startX;

    console.log("Dragging, offset:", currentX);

    stats.style.left = `calc(50% + ${currentX}px)`;
  }

  function endDrag() {
    console.log("Drag ended");
    isDragging = false;

    const threshold = window.innerWidth / 4;

    if (currentX > threshold) {
      console.log("Flicked right");
      stats.style.left = "150%";
    } else if (currentX < -threshold) {
      console.log("Flicked left");
      stats.style.left = "-150%";
    } else {
      console.log("Snap back");
      stats.style.left = "50%";
    }

    currentX = 0;

    window.removeEventListener("mousemove", onDrag);
    window.removeEventListener("mouseup", endDrag);
    window.removeEventListener("touchmove", onDrag);
    window.removeEventListener("touchend", endDrag);
  }
});
