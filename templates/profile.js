function openForm() {
    document.getElementById('myModal').style.display = 'flex';
}

function closeForm() {
    document.getElementById('myModal').style.display = 'none';
}

function submitForm() {
    alert('Form submitted!');
    console.log("Form submitted")
    closeForm();
}