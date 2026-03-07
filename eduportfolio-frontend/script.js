document.getElementById("loginForm").addEventListener("submit", function(e) {
e.preventDefault();

const formData = new FormData();
formData.append("email", document.getElementById("email").value);
formData.append("password", document.getElementById("password").value);

fetch("https://eduportfolio-manager-8.onrender.com/login", {
method: "POST",
body: formData
})
.then(response => response.text())
.then(data => {
window.location = "dashboard.html";
});
});