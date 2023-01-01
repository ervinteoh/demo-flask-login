function inputNotEmpty(element) {
  element.removeAttribute("active");
  if (element.value !== "") element.setAttribute("active", "");
}

document.querySelectorAll(".form-control > input").forEach((element) => {
  element.addEventListener("change", () => inputNotEmpty(element));
});

window.onload = (e) => {
  document
    .querySelectorAll(".form-control > input")
    .forEach((element) => inputNotEmpty(element));
};

const onLogin = () => {
  let remember = document.getElementById("remember").checked;
  let username = document.getElementById("username").value;

  if (remember) window.localStorage.setItem("login-username", username);
  else window.localStorage.removeItem("login-username");
}

if (document.getElementById("page-login")) {
  let username = window.localStorage.getItem("login-username");
  if (username) {
    document.getElementById("remember").checked = true;
    document.querySelector("#loginForm #username").value = username;
  }
  document.getElementById("loginForm").addEventListener("submit", onLogin)
}
