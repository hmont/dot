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

document.addEventListener("DOMContentLoaded", e => {
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
            showAlert('success', successMessage);
        } else {
            const errorMessage = data.message || data.error || null;
            showAlert('error', errorMessage);
        }
    })
    .catch(error => {
        showAlert('error', error);
    });
}