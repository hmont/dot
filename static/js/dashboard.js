import { showAlert } from "./main.js";

let whoaModalContainer = document.querySelector('#whoa-modal-container');
let whoaModal = document.querySelector('#whoa-modal');

let displayNameInput = document.querySelector('#display-name');
let usernameInput = document.querySelector('#username');
let bioInput = document.querySelector('#bio');
let profileVisiblityCheckbox = document.querySelector('#profile-visibility');

let currentPasswordInput = document.querySelector('#current-password');
let newPasswordInput = document.querySelector('#new-password');
let confirmPasswordInput = document.querySelector('#confirm-password');

function confirmDeleteAccount() {
    document.body.style.overflow = 'hidden';

    whoaModal.classList.remove('hidden');
    whoaModalContainer.classList.remove('hidden');
    whoaModal.classList.add('modal-slide-in');

    setTimeout(() => {
        whoaModal.classList.remove('modal-slide-in');
    }, 300);
}

function closeWhoaModal() {
    document.body.style.overflow = '';

    whoaModal.classList.add('modal-slide-out');

    setTimeout(() => {
        whoaModal.classList.remove('modal-slide-out');
        whoaModalContainer.classList.add('hidden');
        whoaModal.classList.add('hidden');
    }, 300);
}

async function savePrivacySettings() {
    let isPrivate = profileVisiblityCheckbox.checked;

    const response = await fetch(`/api/preferences/update`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            is_private: isPrivate
        })
    });

    const responseData = await response.json();

    if (responseData.success) {
        var type = 'success';
    } else {
        var type = 'error';
    }

    showAlert(type, responseData.message);
}

async function updatePassword() {
    let currentPassword = currentPasswordInput.value;
    let newPassword = newPasswordInput.value;
    let confirmPassword = confirmPasswordInput.value;

    const response = await fetch(`/api/preferences/update_password`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            current_password: currentPassword,
            new_password: newPassword,
            confirm_password: confirmPassword
        })
    });

    const responseData = await response.json();

    if (responseData.success) {
        var type = 'success';
    } else {
        var type = 'error';
    }

    showAlert(type, responseData.message);
}

async function saveProfileSettings() {
    let displayName = displayNameInput.value;
    let bio = bioInput.value;

    const response = await fetch(`/api/preferences/update_profile_settings`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            display_name: displayName,
            bio: bio
        })
    });

    const responseData = await response.json();

    if (responseData.success) {
        var type = 'success';
    } else {
        var type = 'error';
    }

    showAlert(type, responseData.message);
}

async function fetchProfileSettings() {
    const profileSettings = await fetch(`/api/preferences/fetch_profile_settings`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    return await profileSettings.json();
}

async function fetchPreferences() {
    const preferences = await fetch(`/api/preferences/fetch`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    return await preferences.json();
}

document.addEventListener("DOMContentLoaded", async event => {
    const preferences = await fetchPreferences();
    const profileSettings = await fetchProfileSettings();

    profileVisiblityCheckbox.checked = preferences.is_private;

    usernameInput.value = `@${profileSettings.username}`;
    bioInput.value = profileSettings.bio;
    displayNameInput.value = profileSettings.display_name;
});

window.confirmDeleteAccount = confirmDeleteAccount;
window.closeWhoaModal = closeWhoaModal;
window.savePrivacySettings = savePrivacySettings;
window.saveProfileSettings = saveProfileSettings;
window.fetchPreferences = fetchPreferences;
window.updatePassword = updatePassword;