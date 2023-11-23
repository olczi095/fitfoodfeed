function toggleReplyButtonColor(replyButton) {
    if (replyButton) {
        if (!replyButton.classList.contains('comment-reply-label-blue')) {
            replyButton.classList.add('comment-reply-label-blue');
        } else {
            replyButton.classList.remove('comment-reply-label-blue');
        }
    }
}