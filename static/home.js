function toggleForm(formId) {
    document.getElementById('registrationForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById(formId).style.display = 'block';
}

document.getElementById('registrationForm').addEventListener('submit', 
    function (event) {
    event.preventDefault();

    fetch('/register', {
        method: 'POST',
        body: new FormData(document.getElementById('registrationForm'))
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        if (response.redirected) {
            console.log("Redirecting to profile page");
            window.location.href = '/profile';
            return; 
        }
    })
    .catch(error => {
        console.error('Error during fetch:', error);
    });
});

document.getElementById('loginFormId').addEventListener('submit', 
    function (event) {
    event.preventDefault();

    let username = document.getElementById('username2');
    let password = document.getElementById('password2');

    if (username === '' || password === '') {
        alert('Username and password are required.');
        return;
    }

    window.location.href = '/profile';
});
