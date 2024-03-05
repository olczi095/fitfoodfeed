document.addEventListener('DOMContentLoaded', function() {
    const likeForm = document.querySelector('.like-form');
        if (likeForm) {
        likeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value; 
            const reviewId = document.querySelector('button[name="like-btn"]').value;
            const url = this.getAttribute('action'); 
            const data = JSON.stringify({'reviewId': reviewId});

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': token
                },
                body: data
            })
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('Response was not ok.', error)
                } else {
                    return response.json();
                }
            })
            .then(function(data) {
                const likeStatsDisplay = document.querySelector('.likes-button h5');
                const likeBtn = document.querySelector('button[name="like-btn"]');
                likeStatsDisplay.textContent = data.likes_stats_display;
                if (data.liked) {
                    likeBtn.classList.add('unlike');
                } else {
                    likeBtn.classList.remove('unlike');
                }
            })
            .catch(function(error) {
                console.log(error);
            });
        });
    }
});