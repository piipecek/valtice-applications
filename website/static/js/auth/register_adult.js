let create_account_button = document.getElementById('create_account_button');
let form = document.getElementById('form');


function disableButtonAfterClick(button) {
    button.addEventListener('click', function(event) {
        if (!button.disabled) {
            button.disabled = true;
            form.submit();
        }
    });
}


disableButtonAfterClick(create_account_button);