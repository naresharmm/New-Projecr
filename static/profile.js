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
      .then(response => response.json())
      .then(data => {
        const myListForm = document.getElementById('myModal2');
        const textContainer = myListForm.querySelector('.modal-content textarea');
        
    
        textContainer.value = '';

        data.texts.forEach(text => {
          textContainer.value += text + '\n';
        });
      })
      .catch(error => alert('An error occurred while fetching saved texts.'));
  }
}

let formHandler1 = new FormHandler('myModal', () =>
  alert('First form submitted!'));
let formHandler2 = new FormHandler('myModal2', () =>
  alert('Second form submitted!'));
