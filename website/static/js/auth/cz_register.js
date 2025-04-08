let bylo_15_button = document.getElementById('bylo_15');
let nebylo_15_button = document.getElementById('nebylo_15');
let under_15_pokracovat = document.getElementById('under_15_pokracovat');

let age_rozcestnik = document.getElementById('age_rozcestnik');
let under_15 = document.getElementById('under_15');
let registrace = document.getElementById('registrace');
let registrace_nebylo_15 = document.getElementById('registrace_nebylo_15');
let jak_vypada_heslo = document.getElementById('jak_vypada_heslo');

let create_account_button_1 = document.getElementById('create_account_button_1');
let create_account_button_2 = document.getElementById('create_account_button_2');
form = document.getElementById('form');

let email_odpovedne = document.getElementById('email_odpovedne');

bylo_15_button.addEventListener('click', function() {
    age_rozcestnik.hidden = true;
    registrace.hidden = false;
    jak_vypada_heslo.hidden = false;
})

nebylo_15_button.addEventListener('click', function() {
    age_rozcestnik.hidden = true;
    under_15.hidden = false;
})

under_15_pokracovat.addEventListener('click', function() {
    if (email_odpovedne.value == "") {
        alert("Vyplňte prosím e-mail odpovědné osoby.");
        return;
    } else {
        under_15.hidden = true;
        registrace_nebylo_15.hidden = false;
        jak_vypada_heslo.hidden = false;
    }
})

function disableButtonAfterClick(button) {
    button.addEventListener('click', function(event) {
        if (!button.disabled) {
            button.disabled = true;
            form.submit();
        }
    });
}

disableButtonAfterClick(create_account_button_1);
disableButtonAfterClick(create_account_button_2);