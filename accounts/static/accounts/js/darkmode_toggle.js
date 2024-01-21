function toggleNavbarClasses(elements, classes) {
    elements.forEach(element => {
        classes.forEach(className => {
            element.classList.toggle(className);
        });
    });
}

function setStyleMode(mode) {
    document.body.classList.toggle('dark-mode');
    let moonButton = document.getElementById('moon-button-accounts');
    let sunButton = document.getElementById('sun-button-accounts');
    let navbarAccounts = document.getElementById('navbar-accounts');

    toggleNavbarClasses([navbarAccounts], ['navbar-dark', 'bg-dark']);
    moonButton.style.display = sunButton.style.display === 'none' ? 'none' : 'block';
    sunButton.style.display = sunButton.style.display === 'none' ? 'block' : 'none';

    localStorage.setItem('style-mode', mode);
}

document.getElementById('style-mode-toggle').addEventListener('click', function() {
    const currentStyleMode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    const newMode = currentStyleMode === 'dark' ? 'light' : 'dark';  // style mode after toggle by the setStyleMode function

    setStyleMode(newMode);
});

document.addEventListener('DOMContentLoaded', function() {
    const storedMode = localStorage.getItem('style-mode');
    if (storedMode && storedMode === 'dark') {
        setStyleMode(storedMode);
    }
});