// Ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    fetchSchedules();
});

// Function to fetch schedules from the server
function fetchSchedules() {
    fetch(userReservationsUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Add CSRF token if needed for security
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        displaySchedules(data);
    })
    .catch(error => console.error('Error fetching schedules:', error));
}

// Function to display schedules in the #exercise-list div
function displaySchedules(schedules) {
    const exerciseList = document.getElementById('exercise-list');
    exerciseList.innerHTML = ''; // Clear existing content

    if (schedules.length === 0) {
        exerciseList.innerHTML = '<p>No schedules found.</p>';
        return;
    }

    schedules.forEach(schedule => {
        const scheduleItem = document.createElement('div');
        scheduleItem.classList.add('schedule-item');
        scheduleItem.innerHTML = `
            <p>${schedule.date}: ${schedule.activity}</p>
            <button class="delete-btn" data-id="${schedule.id}">Delete</button>
        `;
        exerciseList.appendChild(scheduleItem);
    });

    // Add event listeners to delete buttons
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const scheduleId = this.getAttribute('data-id');
            deleteSchedule(scheduleId);
        });
    });
}

// Function to delete a schedule
function deleteSchedule(scheduleId) {
    fetch(`${deleteReservationUrl}/${scheduleId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Add CSRF token if needed for security
        }
    })
    .then(response => {
        if (response.ok) {
            fetchSchedules(); // Refresh the schedules list after deletion
        } else {
            console.error('Error deleting schedule:', response.statusText);
        }
    })
    .catch(error => console.error('Error deleting schedule:', error));
}

// Function to get the value of a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
