document.querySelector('.delete-comment-container').addEventListener('click', function() {
    let commentCounter = document.querySelector('.comment-counter');
    if (parseInt(commentCounter.innerHTML) >= 1) {
        commentCounter.innerHTML = parseInt(commentCounter.innerHTML, 10) - 1;
    } else {
        commentCounter.innerHTML = 0;
    }
});
