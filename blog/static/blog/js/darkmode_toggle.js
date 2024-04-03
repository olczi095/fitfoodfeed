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
    const upperNavbar = document.getElementById('upperNavbar');
    const lowerNavbar = document.getElementById('lowerNavbar');

    if (upperNavbar && lowerNavbar) {
        toggleNavbarClasses([upperNavbar, lowerNavbar], ['navbar-dark', 'navbar-light', 'bg-dark', 'bg-light']);
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

const styleModeToggle = document.getElementById('styleModeToggle');

setStoredStyleMode();

if (styleModeToggle) {
    styleModeToggle.addEventListener('click', function () {
        const currentStyleMode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
        const desiredStyleMode = currentStyleMode === 'dark' ? 'light' : 'dark';  // style mode after toggle by the setStyleMode function

        setStyleMode(desiredStyleMode);
    });
}