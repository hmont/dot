import { showAlert } from "./main.js";

async function logout() {
    const response = await fetch('/api/auth/logout', {
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

window.logout = logout;