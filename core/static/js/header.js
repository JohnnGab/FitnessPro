document.addEventListener("DOMContentLoaded", function() {
    const signinButton = document.querySelector(".sign-in")
    const authenticationLink = document.querySelector(".authentication")
  
    async function checkUserAuthentication() {
        try {
          const response = await fetch(checkAuthUrl, { method: 'GET' });
          const data = await response.json();
          signinButton.remove();
          if (data.isAuthenticated) {
            authenticationLink.appendChild(createAuthenticatedUserElement(data.userName));
          } else {
            authenticationLink.appendChild(createSigninButtonElement());
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }
  
    function createAuthenticatedUserElement(userName) {
        const containerDiv = document.createElement('div');
        const userNameSpan = document.createElement('span');
        const logoutButton = document.createElement('button');
  
        userNameSpan.textContent = `Hi ${userName}`;
        logoutButton.textContent = 'Logout';
        logoutButton.classList.add('logout-button');
        
        logoutButton.addEventListener('click', handleLogout);
  
        containerDiv.appendChild(userNameSpan);
        containerDiv.appendChild(logoutButton);
  
        return containerDiv;
    }
  
    function createSigninButtonElement() {
        const signinButtonCreate = document.createElement('button');
        signinButtonCreate.textContent = 'Sign-in';
        signinButtonCreate.classList.add('sign-in');
    // window.location.href = '/'
        return signinButtonCreate;
    }
  
    async function handleLogout() {
        try {
          const userNameSpan = document.querySelector('.authentication span');
          const logoutButton = document.querySelector('.logout-button');

          const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
      
          const response = await fetch(logoutUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-Requested-With': 'XMLHttpRequest', 
              'X-CSRFToken': csrfToken
            },
          });
      
          const data = await response.json();
      
          if (data.status === 'success') {
            if (userNameSpan) {
              userNameSpan.remove();
            }
            if (logoutButton) {
              logoutButton.remove();
            }
          }
        } catch (error) {
          console.error('Logout Error:', error);
        }
      }
  
    checkUserAuthentication();
  });