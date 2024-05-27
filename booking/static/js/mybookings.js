// Ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    fetchSchedules();
});

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

// Function to fetch schedules from the server
function fetchSchedules() {
    fetch(userReservationsUrl, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
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
            <p>${schedule.date}: ${schedule.class_name}</p>
            <button class="delete-btn" data-id="${schedule.reservation_id}">Delete</button>
        `;
        exerciseList.appendChild(scheduleItem);
    });

    // Add event listeners to delete buttons
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const reservationId = this.getAttribute('data-id');
            deleteReservation(reservationId);
        });
    });
}

// Function to delete a schedule
function deleteReservation(reservationId) {
    fetch(`${deleteReservationUrl}?id=${reservationId}`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
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