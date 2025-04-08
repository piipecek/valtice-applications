let bylo_15_button = document.getElementById('bylo_15');
let nebylo_15_button = document.getElementById('nebylo_15');
let under_15_pokracovat = document.getElementById('under_15_pokracovat');

let age_rozcestnik = document.getElementById('age_rozcestnik');
let under_15 = document.getElementById('under_15');
let registrace = document.getElementById('registrace');
let registrace_nebylo_15 = document.getElementById('registrace_nebylo_15');
let jak_vypada_heslo = document.getElementById('jak_vypada_heslo');

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
        alert("Please fill in the e-mail of the responsible person.");
        return;
    } else {
        under_15.hidden = true;
        registrace_nebylo_15.hidden = false;
        jak_vypada_heslo.hidden = false;
    }
})