/**
 * Toggles the Bootstrap theme of the webpage between light and dark modes.
 * 
 * This function changes the theme by updating the `data-bs-theme` attribute
 * on the body and navbar elements. It also updates the theme icon to reflect
 * the current theme and saves the new theme preference to localStorage.
 * 
 * @function
 */
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    // Determine the new theme based on the current theme
    const newTheme = body.getAttribute('data-bs-theme') === 'light' ? 'dark' : 'light';

    // Set the new theme on the body and navbar
    body.setAttribute('data-bs-theme', newTheme);
    document.getElementById('navbar').setAttribute('data-bs-theme', newTheme);

    // Update the theme icon based on the new theme
    themeIcon.classList.toggle('bi-sun', newTheme === 'light');
    themeIcon.classList.toggle('bi-moon', newTheme === 'dark');
    // Save the new theme to localStorage
    localStorage.setItem('theme', newTheme);
}

// Add event listener to the theme toggle button
document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

// Set the theme on page load based on saved theme in localStorage
document.addEventListener('DOMContentLoaded', function () {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-bs-theme', savedTheme);
    document.getElementById('navbar').setAttribute('data-bs-theme', savedTheme);

    // Set the theme icon based on the saved theme
    const themeIcon = document.getElementById('theme-icon');
    themeIcon.classList.add(savedTheme === 'light' ? 'bi-sun' : 'bi-moon');
});
