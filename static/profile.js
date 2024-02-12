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
            body: JSON.stringify({ uuid: this.uuid, text: textareaValue, title: titleValue }), 
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
            window.location.reload()
        })
        .catch(error => alert('An error occurred. Please try again.'));
    }
}
function deleteNode(node_id) {
    const confirmation = confirm(`Are you sure you want to delete this text?`);
    if (!confirmation) {
        return;
    }
    fetch('/profile/delete_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ node_id: node_id }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        document.getElementById(node_id).parentNode.remove(); // Remove the row from the HTML table upon successful deletion
        return response.json();
    })
    .then(data => {
        alert(data.message || 'Text deleted successfully.');
    })
    .catch(error => {
        console.error(error); 
        alert('An error occurred while deleting the text: ' + error.message);
    });
}

function editNode(node_id) {
    const newText = prompt(`Enter the new text:`);
    if (!newText) {
        return; // If user cancels or enters empty string, do nothing
    }
    fetch('/profile/edit_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ node_id: node_id, new_text: newText }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        document.getElementById(`${node_id}-text`).textContent = newText; // Update the text in the HTML table upon successful edit
        return response.json();
    })
    .then(data => {
        alert(data.message || 'Text edited successfully.');
    })
    .catch(error => {
        console.error(error);
        alert('An error occurred while editing the text: ' + error.message);
    });
}


let formHandler1 = new FormHandler('myModal', () => alert('Text added!'), '');
let formHandler2 = new FormHandler('myModal2', () => alert('Text edited or deleted!'), '');