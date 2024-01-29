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
            const container = document.getElementById('tableContainer');
            container.innerHTML = ''; 
            data.texts.forEach(text => {
                const table = document.createElement('table');
                table.className = 'text-table';
            
                const row = table.insertRow();
                const textCell = row.insertCell(0);
                textCell.textContent = text;
            
                const editButton = document.createElement('button');
                editButton.innerHTML = '<i class="fas fa-pencil-alt"></i> ';
                editButton.classList.add('edit-button'); 
                editButton.onclick = function() { editNode(text);location.reload(); };
                row.insertCell(1).appendChild(editButton);
            
                const deleteButton = document.createElement('button');
                deleteButton.innerHTML = '<i class="fas fa-times"></i>';
                deleteButton.classList.add('delete-button'); 
                deleteButton.onclick = function() { deleteNodes(text);location.reload(); };
                row.insertCell(2).appendChild(deleteButton);
                            
                container.appendChild(table);
                
            });
            
        })
        .catch(error => {
            alert('An error occurred while fetching saved texts: ' + error.message);
        });
    }
    
}
function deleteNodes(title) {
    const confirmation = confirm(`Are you sure you want to delete the text with title: ${title}?`);
    if (!confirmation) {
        return;
    }
    fetch('/profile/delete_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: title }), 
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
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
function editNode(oldTitle) {
    const newTitle = prompt(`Enter the new title for the text: ${oldTitle}`);
    if (newTitle) {
        fetch('/profile/edit_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ old_title: oldTitle, new_title: newTitle }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
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
}
let formHandler1 = new FormHandler('myModal', () => alert('Text added!'), '');
let formHandler2 = new FormHandler('myModal2', () => alert('Text edited or deleted!'), '');