function toggleForm(formId) {
    document.getElementById('registrationForm').style.display = 'none';
    document.getElementById('loginForm').style.display = 'none';

    document.getElementById(formId).style.display = 'block';
}

function handleClick(action) {
    console.log('Clicked:', action);

    if (action === 'register') {
        window.location.href = 'profile.html';
    } else if (action === 'login') {
        window.location.href = 'profile.html';
    }
}