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

async function logout() {
    response = await fetch('/api/auth/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    let json = await response.json();

    showAlert('success', json.message);

    setTimeout(() => {
        window.location.href = '/login';
    }, 2000);
}