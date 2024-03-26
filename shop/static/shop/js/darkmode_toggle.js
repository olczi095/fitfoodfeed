function toggleNavbarClasses(elements, classes) {
    elements.forEach(element => {
        classes.forEach(className => {
            element.classList.toggle(className);
        });
    });
}

function setStyleMode(mode) {
    document.body.classList.toggle('dark-mode');
    let moonButton = document.getElementById('moon-button');
    let sunButton = document.getElementById('sun-button');
    let lowerNavbarShop = document.getElementById('lower-navbar-shop');
    let upperNavbarShop = document.getElementById('upper-navbar-shop');
    let cartButton = document.getElementById('btn-cart');
    let readMoreButton = document.getElementById('readMoreBtn');
    let relatedProductSection = document.getElementById('related-products-section');

    relatedProductSection.classList.toggle('bg-dark');
    relatedProductSection.classList.toggle('bg-light');

    toggleNavbarClasses([lowerNavbarShop, upperNavbarShop], ['navbar-dark', 'navbar-light', 'bg-dark', 'bg-light']);
    toggleNavbarClasses([cartButton, readMoreButton], ['btn-outline-dark', 'btn-outline-light']);

    moonButton.style.display = sunButton.style.display === 'none' ? 'none' : 'block';
    sunButton.style.display = sunButton.style.display === 'none' ? 'block' : 'none';

    localStorage.setItem('style-mode', mode);
}


document.addEventListener('DOMContentLoaded', function () {
    const styleModeToggle = document.getElementById('style-mode-toggle');
    const storedMode = localStorage.getItem('style-mode');

    if (styleModeToggle) {
        styleModeToggle.addEventListener('click', function () {
            const currentStyleMode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
            const newMode = currentStyleMode === 'dark' ? 'light' : 'dark';  // style mode after toggle by the setStyleMode function

            setStyleMode(newMode);
            changeButtonColor();
        });
    }

    if (storedMode && storedMode === 'dark') {
        setStyleMode(storedMode);
    }
});