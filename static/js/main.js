export function showAlert(type, message = null) {
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

export function timeAgo(d) {
  const date = new Date(d);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);

  const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });

  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
    { label: 'second', seconds: 1 }
  ];

  for (const interval of intervals) {
    const delta = Math.floor(seconds / interval.seconds);
    if (Math.abs(delta) >= 1) {
      return rtf.format(-delta, interval.label);
    }
  }

  return 'just now';
}