let postsContainer = document.querySelector('#posts-container');

let noPosts = document.querySelector("#no-posts")

async function loadPosts(page = 1, page_size = 5, user_id) {
    const response = await fetch(`/api/posts/fetch?p=${page}&s=${page_size}&u=${user_id}`, {
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
        const poster = await getUser(post.poster);

        const username = poster.username;
        const display_name = poster.display_name;
        const date = post.created_at;
        const content = post.content;

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