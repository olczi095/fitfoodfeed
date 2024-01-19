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
    let upperNavbar = document.getElementById('upper-navbar');
    let lowerNavbar = document.getElementById('lower-navbar');
    let btnNavbarLogout = document.getElementById('btn-navbar-logout');
    let btnNavbarSignUp = document.getElementById('btn-navbar-signup');

    toggleNavbarClasses([upperNavbar, lowerNavbar], ['navbar-dark', 'navbar-light', 'bg-dark', 'bg-light']);
    moonButton.style.display = sunButton.style.display === 'none' ? 'none' : 'block';
    sunButton.style.display = sunButton.style.display === 'none' ? 'block' : 'none';

    if (btnNavbarSignUp) {
        toggleNavbarClasses([btnNavbarSignUp], ['btn-outline-dark', 'btn-outline-light']);
    } else {
        toggleNavbarClasses([btnNavbarLogout], ['btn-outline-dark', 'btn-outline-light']);
    }

    localStorage.setItem('style-mode', mode);
}

document.getElementById('style-mode-toggle').addEventListener('click', function() {
    const currentStyleMode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    const newMode = currentStyleMode === 'dark' ? 'light' : 'dark';  // style mode after toggle by the setStyleMode function

    setStyleMode(newMode);
});

document.addEventListener('DOMContentLoaded', function() {
    const storedMode = localStorage.getItem('style-mode');
    console.log(storedMode);
    if (storedMode && storedMode === 'dark') {
        setStyleMode(storedMode);
    }
});