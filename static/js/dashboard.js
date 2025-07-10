let whoaModalContainer = document.querySelector('#whoa-modal-container');
let whoaModal = document.querySelector('#whoa-modal');
let count = 0;

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

    //whoaModal.classList.add('hidden');
    //whoaModalContainer.classList.add('hidden');

    whoaModal.classList.add('modal-slide-out');


    setTimeout(() => {
        whoaModal.classList.remove('modal-slide-out');
        whoaModalContainer.classList.add('hidden');
        whoaModal.classList.add('hidden');
    }, 300);
}

function onScroll(event) {

}

window.confirmDeleteAccount = confirmDeleteAccount;
window.closeWhoaModal = closeWhoaModal;
window.onScroll = onScroll;