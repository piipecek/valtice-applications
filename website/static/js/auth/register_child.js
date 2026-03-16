let create_account_button = document.getElementById('create_account_button');
let form = document.getElementById('form');
let email_odpovedne = document.getElementById('email_odpovedne');
let child_select = document.getElementById('child_select');

let registrace_details = document.getElementById('registrace_details');
let vytvorit_ucet_div = document.getElementById('vytvorit_ucet_div');
let heslo_info = document.getElementById('heslo_info');


child_select.addEventListener('change', function() {
    if (child_select.value === 'ano') {
        registrace_details.hidden = false;
        vytvorit_ucet_div.hidden = false;
        heslo_info.hidden = false;
    } else {
        vytvorit_ucet_div.hidden = false;
        registrace_details.hidden = true;
        heslo_info.hidden = true;
    }
})


form.addEventListener('submit', function(event) {
    if (form.checkValidity()) {
        create_account_button.disabled = true;
    }
})
