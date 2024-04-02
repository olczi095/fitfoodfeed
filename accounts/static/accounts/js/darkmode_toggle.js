function toggleNavbarClasses(elements, darkMode) {
    const darkClasses = ['navbar-dark', 'bg-dark'];
    elements.forEach(element => {
        darkClasses.forEach(className => {
            if (darkMode) {
                element.classList.remove(className);
            } else {
                element.classList.add(className);
            }
        });
    });
}

function setNewStyleMode(newStyleMode) {
    const isDarkMode = newStyleMode !== 'dark';
    const moonButton = document.querySelector('.toggle-moon-button');
    const sunButton = document.querySelector('.toggle-sun-button');
    const navbarAccounts = document.getElementById('navbarAccounts');

    document.body.classList.toggle('dark-mode');
    moonButton.style.display = sunButton.style.display === 'none' ? 'none' : 'block';
    sunButton.style.display = sunButton.style.display === 'none' ? 'block' : 'none';
    toggleNavbarClasses([navbarAccounts], isDarkMode);

    localStorage.setItem('style-mode', newStyleMode);
}

function setStoredStyleMode() {
    const storedMode = localStorage.getItem('style-mode');
    if (storedMode && storedMode === 'dark') {
        setStyleMode(storedMode);
    }
};

setStoredStyleMode();

document.getElementById('styleModeToggle').addEventListener('click', function () {
    const currentStyleMode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    const desiredStyleMode = currentStyleMode === 'dark' ? 'light' : 'dark';  // style mode after toggle by the setStyleMode function

    setNewStyleMode(desiredStyleMode);
});