function toggleCommentFormEdit(commentId) {
    const editForm = document.getElementById(`commentFormEdit${commentId}`);

    if (editForm) {
        editForm.style.display === 'none' || editForm.style.display === '' ? editForm.style.display = 'block' : editForm.style.display = 'none';
    }
}

function toggleCommentButtonActive(button) {
    button.classList.toggle('active');
}

document.querySelectorAll('.edit-comment-button').forEach(function (button) {
    button.addEventListener('click', function () {
        const commentId = this.getAttribute('data-comment-id');
        toggleCommentFormEdit(commentId);
        toggleCommentButtonActive(this);
    });
});
