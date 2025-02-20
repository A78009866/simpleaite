// CSRF Token, taken help from SO
function getCookie(name) {
    if (!document.cookie) {
    return null;
    }
    const token = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

    if (token.length === 0) {
    return null;
    }
    return decodeURIComponent(token[0].split('=')[1]);
}

// Submits the new post form and then loads the All Posts page
document.addEventListener('DOMContentLoaded', function() {
    // Check to see form is on the page
    const newpost = document.getElementById('new-post');
    if (newpost != null){
        //Form submit functionality
        document.getElementById('new-post').onsubmit = () => {

            // Get the post data to be sent
            const body = document.getElementById('post-body').value;
    
            // POST the post
            fetch('/posts', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    body: body
                })
            })
            .then(response => response.json())
            .then(result => {
                // Print result for testing purpose
                console.log(result);
            })
            .then(location.reload());
        };
    }
});

document.addEventListener('DOMContentLoaded', function() {

    // Edit button functionality
    document.querySelectorAll('.edit-button').forEach(button => {
        button.onclick = () => {

            // GET the related post
            fetch(`/posts/${button.id}`)
            .then(response => response.json())
            .then(post => {
                // Populate the textarea with old post body
                document.getElementById(`new-body-${button.id}`).innerHTML = post.body
            });
            
            // Hide the edit button
            document.getElementById(`${button.id}`).style.display = 'none';

            // Show the save button
            document.getElementById(`save-${button.id}`).style.display = 'block';

            // Hide the old post content
            document.getElementById(`post-content-${button.id}`).style.display = 'none';

            // Show the textarea
            document.getElementById(`post-edit-${button.id}`).style.display = 'block';
        }
    }) 

    // Save button functionality
    document.querySelectorAll('.save-button').forEach(button => {
        button.onclick = () => {

            const body = document.getElementById(`new-body-${button.dataset.post}`).value

            // PUT the new body into the post
            fetch(`update_post/${button.dataset.post}`, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    body: body
                })
            })
            .then(() => location.reload())
            

        }
    })
});
