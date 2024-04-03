const deleteCommentButtons = document.querySelectorAll('.delete-comment-button');

deleteCommentButtons.forEach(deleteCommentButton => {
    deleteCommentButton.addEventListener('click', async (e) => {
        e.preventDefault();

        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const confirmDeleting = confirm('Are you sure you want to delete this comment?');

        if (confirmDeleting) {
            const url = deleteCommentButton.getAttribute('data-href');
            try {
                await fetch(url, {
                    method: 'DELETE',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRFToken': token
                    }
                });

                const commentId = deleteCommentButton.getAttribute('data-comment-id');
                const commentToDelete = document.getElementById(`comment-${commentId}`);
                commentToDelete.remove();
            }
            catch (error) {
                console.error(error);
            }
        }
    });
});