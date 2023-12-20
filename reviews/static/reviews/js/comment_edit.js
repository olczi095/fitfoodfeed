function toggleCommentFormEdit(commentId) {
    let editForm = document.getElementById(`commentFormEdit${commentId}`);
  
    if (editForm.style.display === 'none' || editForm.style.display === '') {
        editForm.style.display = 'block';
    } else {
        editForm.style.display = 'none';
    }
  }
  
function toggleCommentButtonActive(button) {
    button.classList.toggle('active');
}

document.querySelectorAll('.edit-comment-button').forEach(function(button) {
    button.addEventListener('click', function() {
        let commentId = this.getAttribute('data-comment-id');
        toggleCommentFormEdit(commentId);
        toggleCommentButtonActive(this);
    });
});

document.querySelectorAll('.delete-comment-button').forEach(function(button) {
    button.addEventListener('click', function() {
        toggleCommentButtonActive(this);
    });
});