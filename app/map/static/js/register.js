/**
 * Sanitize user input to prevent XSS attacks.
 * @param {string} input - The user input to sanitize.
 * @returns {string} - The sanitized input.
 */
function sanitizeInput(input) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;',
    };
    const reg = /[&<>"'/]/gi;
    return input.replace(reg, (match) => map[match]);
}

/**
 * Validate email format.
 * @param {string} email - The email to validate.
 * @returns {boolean} - True if the email is valid, false otherwise.
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

// This script handles the registration form submission and sends the registration request to the server. If the registration is successful, the user is shown a success message and redirected to the login page. If the registration fails, an error message is displayed to the user.
document.getElementById('register-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const username = sanitizeInput(document.getElementById('id_username').value);
    const email = sanitizeInput(document.getElementById('id_email').value);
    const password = sanitizeInput(document.getElementById('id_password').value);

    if (!validateEmail(email)) {
        document.getElementById('error-message').innerText = 'Invalid email address';
        document.getElementById('error-message').style.display = 'block';
        return;
    }

    /**
     * Extracts the CSRF token from the browser's cookies.
     *
     * The function splits the document's cookies by '; ' to get an array of individual cookies,
     * then finds the cookie that starts with 'csrftoken=' and extracts its value.
     *
     * @constant {string|undefined} csrfToken - The CSRF token extracted from the cookies, or undefined if not found.
     */
    const csrfToken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1];
    fetch('/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ username, email, password }),
    })
        .then((response) => {
            if (response.ok) {
                // Registration successful message
                document.getElementById('success-message').innerText = 'Registration successful, redirecting to login page...';
                document.getElementById('success-message').style.display = 'block';
                setTimeout(() => {
                    window.location.href = '/login/';
                }, 1000);
            } else {
                return response.json().then((data) => {
                    throw new Error(data.error || 'Registration failed');
                });
            }
        })
        .catch((error) => {
            document.getElementById('error-message').innerText = error.message;
            document.getElementById('error-message').style.display = 'block';
        });
});
