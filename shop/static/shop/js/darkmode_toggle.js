function toggleNavbarClasses(elements, classes) {
    elements.forEach(element => {
        classes.forEach(className => {
            element.classList.toggle(className);
        });
    });
}

function setStyleMode(newStyleMode) {
    const moonButton = document.querySelector('.toggle-moon-button');
    const sunButton = document.querySelector('.toggle-sun-button');
    const upperNavbarShop = document.getElementById('upperNavbarShop');
    const lowerNavbarShop = document.getElementById('lowerNavbarShop');
    const cartButton = document.getElementById('btnCart');
    const readMoreButton = document.getElementById('readMoreBtn');
    const relatedProductSection = document.getElementById('relatedProductsSection');

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
    localStorage.setItem('style-mode', newStyleMode);
}

function setStoredStyleMode() {
    const storedMode = localStorage.getItem('style-mode');
    if (storedMode && storedMode === 'dark') {
        setStyleMode(storedMode);
    }
}

setStoredStyleMode();

const styleModeToggle = document.getElementById('style-mode-toggle');

if (styleModeToggle) {
    styleModeToggle.addEventListener('click', function () {
        const currentStyleMode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
        const newMode = currentStyleMode === 'dark' ? 'light' : 'dark';  // style mode after toggle by the setStyleMode function

        setStyleMode(newMode);
    });
};