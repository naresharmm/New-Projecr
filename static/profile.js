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

function openFormSec() {
    document.getElementById('myModal2').style.display = 'flex';
}

function closeFormSec() {
    document.getElementById('myModal2').style.display = 'none';
}

function submitFormSec() {
    alert('Form submitted!');
    console.log("Form submitted")
    closeFormSec();
}
