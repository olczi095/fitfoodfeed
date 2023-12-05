document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.comment-reply-button').forEach(commentReplyButton => {
            commentReplyButton.addEventListener('click', function() {
                toggleCommentFormReply(this);
                toggleReplyButtonColor(this);
        });
    });
});

function toggleCommentFormReply(replyButton) {
    let replyForm = replyButton.nextElementSibling;

    if (replyForm.style.display === 'none' || replyForm.style.display === '') {
        replyForm.style.display = 'block';
    } else {
        replyForm.style.display = 'none';
    }
}

function toggleReplyButtonColor(replyButton) {
    if (replyButton) {
        if (!replyButton.classList.contains('comment-reply-button-blue')) {
            replyButton.classList.add('comment-reply-button-blue');
        } else {
            replyButton.classList.remove('comment-reply-button-blue');
        }
    }
}