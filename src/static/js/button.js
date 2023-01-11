document.querySelectorAll("button[data-bs-dismiss]").forEach((element) => {
  const dismiss = element.getAttribute("data-bs-dismiss");
  if (element.parentElement.classList.contains(dismiss)) {
    element.addEventListener("click", () => {
      element.parentElement.remove();
    });
  }
});
