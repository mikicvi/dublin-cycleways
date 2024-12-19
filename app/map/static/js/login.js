// This script handles the login form submission and sends the login request to the server. If the login is successful, the user is redirected to the map page. If the login fails, an error message is displayed to the user.
document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const username = document.getElementById('id_username').value;
    const password = document.getElementById('id_password').value;
    /**
     * Extracts the CSRF token from the browser's cookies.
     *
     * This function searches the document's cookies for a cookie named 'csrftoken'
     * and extracts its value. If the 'csrftoken' cookie is not found, the result will be `undefined`.
     *
     * @constant {string|undefined} csrfToken - The CSRF token extracted from the cookies.
     */
    const csrfToken = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        ?.split('=')[1];
    fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ username, password }),
    })
        .then((response) => {
            if (response.ok) {
                window.location.href = '/map/'; // Redirect to the map
            } else {
                return response.json().then((data) => {
                    throw new Error(data.error || 'Login failed');
                });
            }
        })
        .catch((error) => {
            document.getElementById('error-message').innerText = error.message;
            document.getElementById('error-message').style.display = 'block';
        });
});
