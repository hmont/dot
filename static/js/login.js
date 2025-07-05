function showAlert(type, message = null) {
    const alertContainer = document.getElementById('alert');
    const successAlert = document.getElementById('alert-success');
    const errorAlert = document.getElementById('alert-error');
    const successMessage = document.getElementById('alert-success-message');
    const errorMessage = document.getElementById('alert-error-message');

    alertContainer.classList.remove('alert-bounce-in', 'alert-fade-out');

    alertContainer.classList.add('hidden');
    successAlert.classList.add('hidden');
    errorAlert.classList.add('hidden');

    setTimeout(() => {
        if (type === 'success') {
            alertContainer.classList.remove('hidden');
            successAlert.classList.remove('hidden');
            alertContainer.classList.add('alert-bounce-in');

            successMessage.textContent = message;
        } else if (type === 'error') {
            alertContainer.classList.remove('hidden');
            errorAlert.classList.remove('hidden');
            alertContainer.classList.add('alert-bounce-in');

            errorMessage.textContent = message;
        }
    }, 10);

    setTimeout(() => {
        alertContainer.classList.remove('alert-bounce-in');
        alertContainer.classList.add('alert-fade-out');

        setTimeout(() => {
            alertContainer.classList.add('hidden');
            alertContainer.classList.remove('alert-fade-out');
        }, 300);
    }, 5000);
}

function login() {
    let usernameInput = document.querySelector("input#username-input");
    let passwordInput = document.querySelector("input#password-input");

    fetch('/api/auth/login', {
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

            setTimeout(() => {
                window.location.href = '/feed';
            }, 2000);
        } else {
            const errorMessage = data.message || data.error || null;
            showAlert('error', errorMessage);
        }
    })
    .catch(error => {
        showAlert('error', error);
    });
}