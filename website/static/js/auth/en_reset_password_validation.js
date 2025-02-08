const password = document.getElementById("password")
const password_confirm = document.getElementById("password_confirm")
const button = document.getElementById("btn")
const form = document.getElementById("form")

button.addEventListener("click", validate_form)

function validate_form() {
    if (form.reportValidity()) {
        if (password.value.length < 7) {
            alert("Password must be at least 8 characters long")
        } else {
            if (password.value == password_confirm.value) {
                form.submit()
            } else {
                alert("Passwords do not match, please verify it.")
            }
        }
    }
}