function toggleForm(formId) {
    document.getElementById('registrationForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById(formId).style.display = 'block';
}

document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();

    let action = 'register'; 
    let actionSec = 'login'

    if (action === 'register' || actionSec === 'login') {
        fetch('/register', {
            method: 'POST',
            body: new FormData(document.querySelector('form'))
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            if (response.redirected) {
                console.log("Redirecting to home page");
                window.location.href = '/profile';
                return; 
            }
        })
        .catch(error => {
            console.error('Error during fetch:', error);
          
        });
    }
});
