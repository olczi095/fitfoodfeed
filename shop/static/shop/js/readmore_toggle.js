const readMoreBtn = document.getElementById('readMoreBtn');
const fullDescription = document.getElementById('fullDescription');

readMoreBtn.addEventListener('click', function () {
    if (fullDescription.style.display === 'none' || fullDescription.style.display === '') {
        fullDescription.style.display = 'block';
        readMoreBtn.textContent = 'Read less';
    } else {
        fullDescription.style.display = 'none';
        readMoreBtn.textContent = 'Read more';
    }
});