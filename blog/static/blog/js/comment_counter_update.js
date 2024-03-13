function updateCommentCounter(commentCounterElement) {
    let commentCounter = parseInt(commentCounterElement.textContent);
    if (commentCounter > 0) {
        commentCounterElement.textContent = commentCounter - 1;
    } else {
        commentCounterElement.textContent = 0;
    }
}

document.querySelectorAll('.delete-comment-button').forEach(function(deleteBtn) {
    deleteBtn.addEventListener('click', function() {
        let commentCounterElement = document.querySelector('.comment-counter');
        updateCommentCounter(commentCounterElement);
    });
});
