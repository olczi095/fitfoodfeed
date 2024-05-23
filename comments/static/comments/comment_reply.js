function toggleCommentFormReply(replyButton) {
    const replyForm = replyButton.nextElementSibling;

    if (replyForm) {
        replyForm.style.display = replyForm.style.display === 'none' || replyForm.style.display === '' ? 'block' : 'none';
    }
}

function toggleReplyButtonColor(replyButton) {
    replyButton.classList.toggle('comment-reply-button-blue');
}

document.querySelectorAll('.comment-reply-button').forEach(function (button) {
    button.addEventListener('click', function () {
        toggleCommentFormReply(this);
        toggleReplyButtonColor(this);
    });
});
