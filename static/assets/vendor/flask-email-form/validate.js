/**
* flask Email Form Validation - v3.6
* URL: https://bootstrapmade.com/flask-email-form/
* Author: BootstrapMade.com
*/
(function () {
  "use strict";

  let forms = document.querySelectorAll('.flask-email-form');

  forms.forEach( function(e) {
    e.addEventListener('submit', function(event) {
      event.preventDefault();

      let thisForm = this;

      let action = thisForm.getAttribute('action');
      let recaptchaSiteKey = thisForm.querySelector('.g-recaptcha').getAttribute('data-sitekey');
      let recaptchaResponse = grecaptcha.getResponse();

      if (!action) {
        displayError(thisForm, 'The form action property is not set!');
        return;
      }
      thisForm.querySelector('.loading').classList.add('d-block');
      thisForm.querySelector('.error-message').classList.remove('d-block');
      thisForm.querySelector('.sent-message').classList.remove('d-block');

      let formData = new FormData(thisForm);

      if (recaptchaSiteKey) {
        if (!recaptchaResponse) {
          displayError(thisForm, 'Please complete the reCAPTCHA!');
          return;
        }
        formData.append('recaptcha-response', recaptchaResponse);
      }

      flask_email_form_submit(thisForm, action, formData);
    });
  });

  function flask_email_form_submit(thisForm, action, formData) {
    let recaptchaSecretKey = RECAPTCHA_SECRET_KEY; // get the secret key from the environment variable

    fetch(action, {
      method: 'POST',
      body: formData,
      headers: {'X-Requested-With': 'XMLHttpRequest', 'X-Recaptcha-Secret': recaptchaSecretKey}
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(`${response.status} ${response.statusText} ${response.url}`);
      }
    })
    .then(data => {
      thisForm.querySelector('.loading').classList.remove('d-block');
      if (data.success) {
        thisForm.querySelector('.sent-message').classList.add('d-block');
        thisForm.reset();
        setTimeout(function(){
          thisForm.querySelector('.sent-message').classList.remove('d-block');
        }, 3000);
      } else {
        throw new Error(data.message + action);
      }
    })
    .catch((error) => {
      displayError(thisForm, error);
    });
  }

  function displayError(thisForm, error) {
    thisForm.querySelector('.loading').classList.remove('d-block');
    thisForm.querySelector('.error-message').innerHTML = error;
    thisForm.querySelector('.error-message').classList.add('d-block');
    setTimeout(function(){
      thisForm.querySelector('.error-message').classList.remove('d-block');
    }, 3000);
  }

})();
