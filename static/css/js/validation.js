function validateForm() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    if (email == "" || password == "") {
        alert("Email and Password cannot be empty!");
        return false;
    }

    return true;
}