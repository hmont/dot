var url = document.location.href.split('/');

let displayNameElements = document.querySelectorAll('#display-name');
let usernameElement = document.querySelector('#username');
let bioElement = document.querySelector('#bio');
let timeagoElement = document.querySelector('#joined-time-ago');

let noPosts = document.querySelector("#no-posts");
let postsContainer = document.querySelector('#posts-container');
let loadingScreen = document.querySelector('div#loading-screen');

var globalUser;

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

function timeAgo(d) {
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

document.addEventListener("DOMContentLoaded", async e => {
    const user = await loadUser();

    if (user == null) {
        showAlert('error', 'user not found :(');
        return;
    }

    usernameElement.innerHTML = user.username;

    displayNameElements.forEach(e => {
        e.innerHTML = user.display_name;
    });

    bioElement.innerHTML = user.bio ? user.bio : `<i>user has no biography</i>`;
    timeagoElement.innerHTML = timeAgo(user.created_at);

    globalUser = user;

    loadingScreen.classList.add('hidden');

    await loadPosts();
});

async function loadPosts(page = 1) {
    const response = await fetch(`/api/posts/fetch?p=${page}&s=5&u=${globalUser.id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    data = await response.json();

    if (!data.success) {
        console.log('An error occurred while fetching posts.', data.message);
        return;
    }

    if (data.posts.length > 0) {
        noPosts.hidden = true;
    }

    for (const post of data.posts) {
        const username = globalUser.username;
        const display_name = globalUser.display_name;
        const date = post.created_at;
        const content = decodeURIComponent(post.content);

        const postHTML = `
            <div class="bg-white rounded-lg shadow-sm border p-6 text-gray-500">
                <div id="post grid grid-cols-5 inline-block text-left">
                    <h2 class="text-gray-900 text-2xl font-bold align-middle inline-block hover:underline"><a href="/users/${username}">${display_name}</a></h2>
                    <span class="ml-2 text-gray-500 text-md align-middle hover:underline"><a href="/users/${username}">@${username}</a></span>
                    <span title="${date}" class="ml-2 text-gray-500 text-md align-middle">${(new Date(date)).toDateString()}</span>
                    <p>${content}</p>
                </div>
            </div>
        `

        postsContainer.insertAdjacentHTML('beforeend', postHTML);
    }
}

async function loadUser() {
    const pathParts = url.filter(part => part !== '');
    const usersIndex = pathParts.findIndex(part => part === 'users');

    if (usersIndex === -1 || usersIndex + 1 >= pathParts.length) {
        return null;
    }

    const username = pathParts[usersIndex + 1].split('?')[0];

    const result = await fetch(`/api/users/fetch?name=${username}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    json = await result.json();

    return json.user;
}