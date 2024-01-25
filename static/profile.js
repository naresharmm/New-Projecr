class FormHandler {
    constructor(formId, submitCallback, uuid) { 
        this.formId = formId;
        this.submitCallback = submitCallback;
        this.uuid = uuid;
        
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
            console.log("aaaa", response)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("data", data.texts)
            const myListForm = document.getElementById(this.formId); console.log("FFF")
            const textContainer = myListForm.querySelector('.modal-content textarea');
            // textContainer.value = data.texts.map(text => text.title + ': ' + text.text).join('\n');
            console.log("data", myListForm)
            console.log("data", textContainer)
            
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

function deleteNode(uuid) {
    const confirmation = confirm('Are you sure you want to delete this text?');

    if (!confirmation) {
        return;
    }

    fetch('/delete_text', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({ uuid: uuid }), 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message || 'Text deleted successfully.');
        formHandler2.closeForm();
    })
    .catch(error => alert('Error'));
}

let formHandler1 = new FormHandler('myModal', () => alert('Text added!'), '');
let formHandler2 = new FormHandler('myModal2', () => alert('Text edited or deleted!'), '');
