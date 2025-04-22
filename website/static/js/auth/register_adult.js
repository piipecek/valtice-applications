let create_account_button = document.getElementById('create_account_button');
let form = document.getElementById('form');

form.addEventListener('submit', function(event) {
    if (form.checkValidity()) {
        create_account_button.disabled = true;
    }
})