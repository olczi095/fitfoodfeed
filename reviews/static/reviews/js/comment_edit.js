function toggleCommentFormEdit(editButton) {
    let editForm = editButton.nextElementSibling;

    if (editForm.style.display === 'none' || editForm.style.display === '') {
        editForm.style.display = 'block';
    } else {
        editForm.style.display = 'none';
    }
}

document.querySelectorAll('.edit-comment-button').forEach(function(button) {
    button.addEventListener('click', function() {
        toggleCommentFormEdit(this);
    });
});