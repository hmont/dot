import { showAlert } from "./main.js";

let whoaModalContainer = document.querySelector('#whoa-modal-container');
let whoaModal = document.querySelector('#whoa-modal');

let displayNameInput = document.querySelector('#display-name');
let usernameInput = document.querySelector('#username');
let bioInput = document.querySelector('#bio');
let profileVisiblityCheckbox = document.querySelector('#profile-visibility');

let bioCount = document.querySelector('#bio-count');

let currentPasswordInput = document.querySelector('#current-password');
let newPasswordInput = document.querySelector('#new-password');
let confirmPasswordInput = document.querySelector('#confirm-password');

let deletePasswordInput = document.querySelector('#delete-password-input');

let profilePictureUpload = document.querySelector('#profile-picture-upload');
let profilePicturePreview = document.querySelector('#profile-picture-preview');
let savePictureButton = document.querySelector('#save-picture-btn');

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

bioInput.addEventListener('input', () => {
    const newLength = bioInput.value.length;

    bioCount.textContent = `${newLength}/150`;

    if (newLength >= 110) {
        bioCount.classList.add('text-red-500');
    } else {
        bioCount.classList.remove('text-red-500');
    }
});

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

function previewProfilePicture(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            profilePicturePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);

        savePictureButton.disabled = false;
        savePictureButton.classList.remove('bg-gray-400', 'cursor-not-allowed');
        savePictureButton.classList.add('bg-red-500', 'hover:bg-red-600');
    }
}

async function uploadProfilePicture() {
    const file = profilePictureUpload.files[0];

    const formData = new FormData();
    formData.append('file', file);

    if (!file) {
        showAlert('error', 'you must select a picture first');
        return;
    }

    const response = await fetch('/api/preferences/update_profile_picture', {
        method: 'POST',
        body: formData
    });

    const responseData = await response.json();

    const type = responseData.success ? 'success' : 'error';

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

async function proceedToDelete() {
    await fetch(`/api/account/delete`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            password: deletePasswordInput.value
        })
    }).then(response => {
        return response.json();
    }).then(data => {
        let type = data.success ? 'success' : 'error';

        showAlert(type, data.message);

        if (data.success) {
            setTimeout(() => {
                window.location.href = '/'
            }, 3000);
        }
    });
}

document.addEventListener("DOMContentLoaded", async event => {
    const preferences = await fetchPreferences();
    const profileSettings = await fetchProfileSettings();

    profileVisiblityCheckbox.checked = preferences.is_private;

    usernameInput.value = `@${profileSettings.username}`;
    displayNameInput.value = profileSettings.display_name;
    bioInput.value = profileSettings.bio;

    bioInput.dispatchEvent(new Event('input'));
    bioCount.textContent = `${bioInput.value.length}/150`
    displayNameInput.innerHTML = profileSettings.display_name;

    profilePicturePreview.src = profileSettings.avatar_url ? `/static/img/avatar/${profileSettings.avatar_url}` : '/static/img/default-avatar.png';
});

window.confirmDeleteAccount = confirmDeleteAccount;
window.closeWhoaModal = closeWhoaModal;
window.savePrivacySettings = savePrivacySettings;
window.saveProfileSettings = saveProfileSettings;
window.fetchPreferences = fetchPreferences;
window.updatePassword = updatePassword;
window.proceedToDelete = proceedToDelete;
window.previewProfilePicture = previewProfilePicture;
window.uploadProfilePicture = uploadProfilePicture;