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
    const textareaValue = document.querySelector('textarea').value.trim();
    
    if (!textareaValue) {
      alert('Please enter some text before submitting.');
      return;
    }

    fetch('/save_text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ text: textareaValue }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      alert(data.message || 'Form submitted successfully.');
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
        const textContainer = myListForm.querySelector('.modal-content textarea');

        textContainer.value = data.texts.join('\n'); 
      })
      .catch(error => alert('An error occurred while fetching saved texts.'));
  }

  openList() {
    this.fetchAndDisplaySavedTexts();
    document.getElementById(this.formId).style.display = 'flex';
  }
}

function editHandler() {
  const textareaValue = document.querySelector('#myModal2 .modal-content textarea').value.trim();

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
    body: JSON.stringify({ text: textareaValue }),
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

function deleteHandler() {
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
  .catch(error => alert('An error occurred while deleting the text.'));
}

let formHandler1 = new FormHandler('myModal', () =>
  alert('First form submitted!'));
let formHandler2 = new FormHandler('myModal2', () =>
  alert('Second form submitted!'));