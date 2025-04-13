let create_account_button = document.getElementById('create_account_button');
let form = document.getElementById('form');
let continue_button = document.getElementById('continue_button');
let email_odpovedne = document.getElementById('email_odpovedne');
let registrace_details = document.getElementById('registrace_details');

continue_button.addEventListener('click', function() {
    let emailValue = email_odpovedne.value;

    fetch('/guest_api/email_odpovedne', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: emailValue })
    })
    .then(async response => {
        if (response.ok) {
            return response.json();
        } else {
            const errorData = await response.json();
            throw new Error(errorData.message_en);
        }
    })
    .then(data => {
        registrace_details.hidden = false;
        continue_button.hidden = true;
    })
    .catch(error => {
        alert(error.message);
    });
});



function disableButtonAfterClick(button) {
    button.addEventListener('click', function(event) {
        if (!button.disabled) {
            button.disabled = true;
            form.submit();
        }
    });
}

disableButtonAfterClick(create_account_button);