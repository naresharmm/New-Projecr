class FormHandler {
  constructor(formId, submitCallback) {
    this.formId = formId;
    this.submitCallback = submitCallback;
  }

  openForm() {
    document.getElementById(this.formId).style.display = 'flex';
  }

  closeForm() {
    document.getElementById(this.formId).style.display = 'none';
  }

  submitForm() {
    alert('Form submitted!');
    console.log('Form submitted');
    this.submitCallback();
    this.closeForm();
  }
}

let formHandler1 = new FormHandler('myModal', () => 
alert('First form submitted!'));
let formHandler2 = new FormHandler('myModal2', () => 
alert('Second form submitted!'));
