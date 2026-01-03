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
        alertContainer.classList.remove('hidden');
        alertContainer.classList.add('alert-bounce-in');

        if (type === 'success') {
            successAlert.classList.remove('hidden');
            successMessage.textContent = message;
        } else if (type === 'error') {
            errorAlert.classList.remove('hidden');
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

function parseDate(d) {
    if (d instanceof Date) return d;

    if (typeof d === 'string') {
        const hasTz = /[zZ]|[+-]\d{2}:?\d{2}$/.test(d);
        const isoNoTz = /^\d{4}-\d{2}-\d{2}T/.test(d) && !hasTz;
        const parsed = isoNoTz ? new Date(`${d}Z`) : new Date(d);

        if (!Number.isNaN(parsed.getTime())) return parsed;
    }

    return new Date(d);
}

export function timeAgo(d, nowOverride = null) {
    const date = parseDate(d);
    const now = nowOverride ? parseDate(nowOverride) : new Date();
    let diffSeconds = (date - now) / 1000; // positive = future, negative = past

    // Treat small future skews (e.g., clock or timezone drift) as past events
    if (diffSeconds > 0 && diffSeconds < 4 * 3600) {
        diffSeconds = -diffSeconds;
    }

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
        if (Math.abs(diffSeconds) >= interval.seconds) {
            const delta = Math.round(diffSeconds / interval.seconds);
            return rtf.format(delta, interval.label);
        }
    }

    return 'just now';
}