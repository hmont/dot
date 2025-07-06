const placeholders = [
    "something little that made today better...",
    "currently obsessed with...",
    "a simple joy lately...",
    "woke up feeling...",
    "a win from this week...",
    "smiled today because...",
    "my comfort food is...",
    "been rewatching...",
    "a place i'd love to visit...",
    "a goal i'm proud of...",
    "today i'm grateful for...",
    "i feel most at peace when...",
    "the weather's been perfect for..."
]

let currentIndex = 0;

let contentInput = document.querySelector("#post-content");
let charCount = document.querySelector("#char-count");

let postsContainer = document.querySelector('#posts-container');

document.addEventListener("DOMContentLoaded", e => {
    fetchPosts();

    contentInput.placeholder = placeholders[currentIndex];

    setInterval(() => {
        contentInput.placeholder = placeholders[currentIndex];
        currentIndex = (currentIndex + 1) % placeholders.length;
    }, 3000)
});

contentInput.oninput = e => {
    let value = contentInput.value;

    const newLength = contentInput.value.length;

    if (newLength > 0) {
        document.querySelector("#post-btn").disabled = false;
    }
    else {
        document.querySelector("#post-btn").disabled = true;
    }

    if (newLength >= 100) {
        charCount.classList.add("text-red-500");
    }
    else {
        charCount.classList.remove("text-red-500");
    }

    charCount.innerText = newLength.toString() + "/120"
}

async function getUser(user_id) {
    try {
        const response = await fetch(`/api/users/fetch?u=${user_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const userData = await response.json();

        if (userData.success) {
            return userData.user;
        }

        return null;
    } catch (error) {
        console.error('Error fetching user data:', error);
        return null;
    }
}

function createPost() {
    fetch('/api/posts/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            content: contentInput.value
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const successMessage = data.message || null;
            console.log('success', successMessage);
        } else {
            const errorMessage = data.message || data.error || null;
            console.log('error', errorMessage);
        }
    })
    .catch(error => {
        console.log('error', error);
    });
}

async function fetchPosts() {
    const response = await fetch('/api/posts/fetch?p=0&s=10', {
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

    postsContainer.innerHTML = '';

    data.posts.forEach(async post => {
        const poster = await getUser(post.poster);

        const username = poster.username;
        const display_name = poster.display_name;
        const date = post.created_at;
        const content = post.content;

        const postHTML = `
            <div class="bg-white rounded-lg shadow-sm border p-6 text-gray-500">
                <div id="post grid grid-cols-5 inline-block text-left">
                    <h2 class="text-gray-900 text-2xl font-bold align-middle inline-block">${display_name}</h2>
                    <span class="ml-2 text-gray-500 text-md align-middle">@${username}</span>
                    <span class="ml-2 text-gray-500 text-md align-middle">${(new Date(date)).toDateString()}</span>
                    <p>${content}</p>
                </div>
            </div>
        `

        postsContainer.insertAdjacentHTML('afterbegin', postHTML);
    });
}