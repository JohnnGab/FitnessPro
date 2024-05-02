function displayError(inputElement, message) {
  const formField = inputElement.parentNode;
  let errorDiv = formField.querySelector(".error-message");
  if (!errorDiv) {
      errorDiv = document.createElement("div");
      errorDiv.classList.add("error-message"); // Ensure this class is styled in CSS
      formField.appendChild(errorDiv);
  } else {
      errorDiv.textContent = ""; // Clear previous message
  }
  errorDiv.textContent = message;
}

// Function to handle form submission
const signIn = async () => {
    // Get user input
    const emailElement = document.getElementById('email');
    const passwordElement = document.getElementById('password');
    const password = passwordElement.value;
    const email = emailElement.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (!emailRegex.test(email)) {
        displayError(emailElement, "Please enter a valid email address.");
        return
    }

      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
    try {
      const response = await fetch(signinUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken
        },
        body: formData
      });
      
  
      // if (!response.ok) {
      //   throw new Error('Network error');
      // }
  
      const responseData = await response.json();
  
      if (responseData.success) {
        // Redirect user if login is successful
        window.location.href = responseData.redirect_url;
      } else {
        displayError(passwordElement, responseData.error_message);
      }

    } catch (error) {
      console.error('Fetch Error:', error);
    }
  };
  
  // Wait for the DOM content to be fully loaded
  document.addEventListener("DOMContentLoaded", function () {
    // Event listener for form submission
    document.querySelector('form').addEventListener('submit', async function (event) {
      event.preventDefault(); // Prevent default form submission
      await signIn(); // Call signIn function
    });
  });
  