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
        const textareaValue = 
        document.querySelector('#' + this.formId + ' textarea').value.trim();
        const titleValue = 
        document.querySelector('#' + this.formId + ' input[name="title"]').value.trim();
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
            body: 
            JSON.stringify
            ({ uuid: this.uuid, text: textareaValue, title: titleValue }), 
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

    fetch(`/profile/delete_text/${node_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.message === 'Text deleted successfully') {
            const rowToDelete = document.querySelector(`tr[data-node-id="${node_id}"]`);
            console.log(node_id)
            if (rowToDelete) {
                console.log(rowToDelete)
                rowToDelete.remove();
                alert('Text deleted successfully');
            }
        } else {
            alert(data.message || 'An error occurred while deleting the text.');
        }
    })
    .catch(error => {
        console.error(error);
        alert('An error occurred while deleting the text: ' + error.message);
    });
}



function editNode(node_id) {
    const newText = prompt(`Enter the new text:`);
    if (!newText) {
        return; 
    }
    fetch(`/profile/edit_text/${node_id}`, {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ new_text: newText }),  
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.message === 'Text edited successfully') {
            const textElement = document.querySelector(`tr[data-node-id="${node_id}"] td:nth-child(2)`);
            if (textElement) {
                textElement.textContent = newText;
                alert(data.message);
            } else {
                alert('Row not found');
            }
        } else {
            alert(data.message || 'An error occurred while editing the text.');
        }
    })
    .catch(error => {
        console.error(error);
        alert('An error occurred while editing the text: ' + error.message);
    });

}
let formHandler1 = new FormHandler('myModal', () => alert('Text added!'), '');
let formHandler2 = new FormHandler('myModal2', () => alert('Text edited or deleted!'), '');