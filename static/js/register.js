import { showAlert } from "./main.js";

function register() {
    let usernameInput = document.querySelector("input#username-input");
    let passwordInput = document.querySelector("input#password-input");

    fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: usernameInput.value,
            password: passwordInput.value
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const successMessage = data.message || null;
            showAlert('success', successMessage);
            usernameInput.value = '';
            passwordInput.value = '';
        } else {
            const errorMessage = data.message || data.error || null;
            showAlert('error', errorMessage);
        }
    })
    .catch(error => {
        showAlert('error', error);
    });
}

window.register = register;