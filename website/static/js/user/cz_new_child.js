let child_select = document.getElementById('child_select');

let registrace_details = document.getElementById('registrace_details');
let vytvorit_ucet_div = document.getElementById('vytvorit_ucet_div');
let heslo_info = document.getElementById('heslo_info');

child_select.addEventListener('change', function() {
    if (child_select.value === 'ano') {
        registrace_details.hidden = false;
        heslo_info.hidden = false;
        vytvorit_ucet_div.hidden = false;
    } else {
        registrace_details.hidden = true;
        heslo_info.hidden = true;
        vytvorit_ucet_div.hidden = false;
    }
})