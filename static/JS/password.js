function showPassword() {
    var passwordField = document.getElementById("password1");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}