class FormHandler {
    constructor(formId, submitCallback) { 
        this.formId = formId;
        this.submitCallback = submitCallback; 
    }

    openForm() {
        if (this.formId === 'myModal2') {
            this.fetchAndDisplaySavedTexts();
        }
        document.getElementById(this.formId).style.display = 'flex';
    }

    closeForm() {
        document.getElementById(this.formId).style.display = 'none';
    }

    submitForm() {
        const textareaValue = document.querySelector('#' + this.formId + ' textarea').value.trim();
        const titleValue = document.querySelector('#' + this.formId + ' input[name="title"]').value.trim();

        if (!textareaValue || !titleValue) {
            alert('Please enter both title and text.');
            return;
        }

        fetch('/save_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({ user_phone: this.uuid, text: textareaValue, title: titleValue }), // Changed uuid to user_phone
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message || 'Text saved successfully.');
            this.submitCallback && this.submitCallback();
            this.closeForm();
        })
        .catch(error => alert('An error occurred. Please try again.'));
    }

    fetchAndDisplaySavedTexts() {
        fetch('/get_saved_texts')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const myListForm = document.getElementById('myModal2');
            const textList = document.getElementById('textList');
            textList.innerHTML = data.texts.map(text => `<li>${text}</li>`).join('\n');
        })
        .catch(error => alert('An error occurred while fetching saved texts.'));
    }
}




function editNode(uuid) {
    const textareaValue = document.querySelector('#myModal2 textarea').value.trim();

    if (!textareaValue) {
        alert('Please enter some text before editing.');
        return;
    }

    fetch('/edit_text', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({ text: textareaValue, uuid: uuid }), 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message || 'Text edited successfully.');
        formHandler2.closeForm();
    })
    .catch(error => alert('An error occurred while editing the text.'));
}

function deleteAllNodes() {
    const confirmation = confirm('Are you sure you want to delete all texts?');

    if (!confirmation) {
        return;
    }

    fetch('/profile/delete_all_texts', {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message || 'All texts deleted successfully.');
        formHandler2.closeForm();
        fetchAndDisplaySavedTexts();
    })
    .catch(error => alert('Error'));
}


let formHandler1 = new FormHandler('myModal', () => alert('Text added!'), '');
let formHandler2 = new FormHandler('myModal2', () => alert('Text edited or deleted!'), '');
