function updateCommentCounter(commentCounterElement) {
    const commentCounter = parseInt(commentCounterElement.textContent);
    commentCounterElement.textContent = commentCounter > 0 ? commentCounter - 1 : 0;
}

document.querySelectorAll('.delete-comment-button').forEach(function (deleteBtn) {
    deleteBtn.addEventListener('click', function () {
        let commentCounterElement = document.querySelector('.comment-counter');
        updateCommentCounter(commentCounterElement);
    });
});
