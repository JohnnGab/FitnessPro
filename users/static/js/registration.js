document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const emailInput = document.getElementById("email");
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const firstnameInput = document.getElementById("firstname");
  const lastnameInput = document.getElementById("lastname");


  form.addEventListener("submit", function (e) {
    e.preventDefault();
    clearErrors();

    if (firstnameInput.value.trim() === "") {
      displayError(firstnameInput, "Please enter your First Name.");
      return;
    }

    if (lastnameInput.value.trim() === "") {
      displayError(lastnameInput, "Please enter your Last Name.");
      return;
    }

    // Front-end email validation
    if (!emailRegex.test(emailInput.value)) {
      displayError(emailInput, "Please enter a valid email address.");
      return;
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData(form);

    fetch(createAccountUrl, {
      method: "POST",
      body: formData,
      headers: {
        'X-CSRFToken': csrftoken  // Ensure CSRF token is included
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (!data.success) {
          // Handle back-end validation errors
          Object.keys(data.errors).forEach((key) => {
            const inputElement = document.getElementsByName(key)[0];
            data.errors[key].forEach((error) => {
              displayError(inputElement, error);
            });
          });
        } else{
          window.location.href = data.redirect_url;   
        }
      })
      .catch((error) => console.error("Error:", error));
  });

  function displayError(inputElement, message) {
    const errorDiv = document.createElement("div");
    errorDiv.textContent = message;
    errorDiv.classList.add("error-message"); // Make sure to define this class in your CSS
    inputElement.parentNode.appendChild(errorDiv);
  }

  function clearErrors() {
    const errorMessages = document.querySelectorAll(".error-message");
    errorMessages.forEach((error) => error.remove());
  }
});
