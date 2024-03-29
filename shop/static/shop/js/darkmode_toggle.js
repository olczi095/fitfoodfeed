function toggleNavbarClasses(elements, classes) {
    elements.forEach(element => {
        classes.forEach(className => {
            element.classList.toggle(className);
        });
    });
}

function setStyleMode(mode) {
    let moonButton = document.getElementById('moon-button');
    let sunButton = document.getElementById('sun-button');
    let lowerNavbarShop = document.getElementById('lower-navbar-shop');
    let upperNavbarShop = document.getElementById('upper-navbar-shop');
    let cartButton = document.getElementById('btn-cart');
    let readMoreButton = document.getElementById('readMoreBtn');
    let relatedProductSection = document.getElementById('related-products-section');

    if (relatedProductSection) {
        relatedProductSection.classList.toggle('bg-dark');
        relatedProductSection.classList.toggle('bg-light');
    }

    if (lowerNavbarShop && upperNavbarShop) {
        toggleNavbarClasses([lowerNavbarShop, upperNavbarShop], ['navbar-dark', 'navbar-light', 'bg-dark', 'bg-light']);
    }

    if (cartButton) {
        toggleNavbarClasses([cartButton], ['btn-outline-dark', 'btn-outline-light']);
    }
    if (readMoreButton) {
        toggleNavbarClasses([readMoreButton], ['btn-outline-dark', 'btn-outline-light']);
    }

    if (moonButton && sunButton) {
        moonButton.style.display = sunButton.style.display === 'none' ? 'none' : 'block';
        sunButton.style.display = sunButton.style.display === 'none' ? 'block' : 'none';
    }

    document.body.classList.toggle('dark-mode');
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
        });
    }

    if (storedMode && storedMode === 'dark') {
        setStyleMode(storedMode);
    }
});