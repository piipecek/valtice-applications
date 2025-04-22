let create_account_button = document.getElementById('create_account_button');
let create_account_button_2 = document.getElementById('create_account_button_2');
let form = document.getElementById('form');
let email_odpovedne = document.getElementById('email_odpovedne');
let registrace_details = document.getElementById('registrace_details');
let child_select = document.getElementById('child_select');
let vytvorit_ucet_div = document.getElementById('vytvorit_ucet_div');

child_select.addEventListener('change', function() {
    if (child_select.value === 'ano') {
        registrace_details.hidden = false;
        vytvorit_ucet_div.hidden = true;
    } else {
        vytvorit_ucet_div.hidden = false;
        registrace_details.hidden = true;
    }
})


form.addEventListener('submit', function(event) {
    if (form.checkValidity()) {
        create_account_button.disabled = true;
        create_account_button_2.disabled = true;
    }
})
