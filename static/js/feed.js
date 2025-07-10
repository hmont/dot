import { showAlert } from "./main.js";

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

let noPosts = document.querySelector("#no-posts");

function onContentInput(e) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();

        createPost();
    }

    console.log(e.key);
}

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

async function createPost() {
    const response = await fetch('/api/posts/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            content: contentInput.value
        })
    });

    const data = await response.json();

    if (!data.success) {
        showAlert('error', data.message);
        return;
    }

    contentInput.value = '';
    charCount.value = '0/120';
    charCount.classList.remove("text-red-500");

    showAlert('success', 'post created!');
}

async function fetchPosts(page = 1, page_size = 5) {
    const response = await fetch(`/api/posts/fetch?p=${page}&s=${page_size}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    const data = await response.json();

    if (!data.success) {
        console.log('An error occurred while fetching posts.', data.message);
        return;
    }

    if (data.posts.length > 0) {
        noPosts.hidden = true;
    }

    for (const post of data.posts) {
        const poster = await getUser(post.poster);

        const username = poster.username;
        const display_name = poster.display_name;
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

        // console.log(content);


        postsContainer.insertAdjacentHTML('beforeend', postHTML);
    }
}

window.createPost = createPost;
window.fetchPosts = fetchPosts;
window.onContentInput = onContentInput;