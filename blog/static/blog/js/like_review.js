const likeForm = document.querySelector('.like-form');

if (likeForm) {
    likeForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const reviewId = document.querySelector('button[name="like-btn"]').value;
        const url = this.getAttribute('action');
        const data = JSON.stringify({ 'reviewId': reviewId });

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': token
                },
                body: data
            });

            if (!response.ok) {
                throw new Error('Response was not ok.');
            } else {

                const responseData = await response.json();

                const likeStatsDisplay = document.querySelector('.likes-button h5');
                likeStatsDisplay.textContent = responseData.likes_stats_display;

                const likeBtn = document.querySelector('button[name="like-btn"]');
                likeBtn.classList.toggle('unlike');
            }
        } catch (error) {
            console.error(error);
        }
    });
};