const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

const months = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

const monthAndYear = document.getElementById("monthAndYear");
const calendar = document.getElementById("calendar").querySelector("tbody");

document.getElementById("prev").addEventListener("click", () => navigate(-1));
document.getElementById("next").addEventListener("click", () => navigate(1));

function navigate(n) {
  currentMonth += n;
  if (currentMonth < 0 || currentMonth > 11) {
    currentYear += Math.floor(currentMonth / 12);
    currentMonth = (currentMonth + 12) % 12;
  }
  showCalendar(currentMonth, currentYear);
}

function showCalendar(month, year) {
  const firstDay = new Date(year, month).getDay();
  calendar.innerHTML = "";

  monthAndYear.textContent = `${months[month]} ${year}`;

  let date = 1;
  let currentDayCell = null; // Variable to hold the cell of the current day

  for (let i = 0; i < 6; i++) {
    let row = document.createElement("tr");
    for (let j = 0; j < 7; j++) {
      if (i === 0 && j < firstDay) {
        row.insertCell().appendChild(document.createTextNode(""));
      } else if (date > new Date(year, month + 1, 0).getDate()) {
        break;
      } else {
        let cell = row.insertCell();
        cell.textContent = date;
        if (date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
          cell.classList.add("selected");
          currentDayCell = cell; // Store reference to the cell of the current day
        }
        cell.addEventListener("click", () => selectDate(cell));
        date++;
      }
    }
    calendar.appendChild(row);
  }

  // Automatically select the current day if it's visible in the current month view
  if (currentDayCell) {
    selectDate(currentDayCell);
  }
}

function selectDate(cell) {
  if (document.querySelector(".selected")) {
    document.querySelector(".selected").classList.remove("selected");
  }
  cell.classList.add("selected");

  const selectedDate = new Date(currentYear, currentMonth, parseInt(cell.textContent));
  const formattedDate = `${selectedDate.getFullYear()}-${(selectedDate.getMonth() + 1).toString().padStart(2, '0')}-${selectedDate.getDate().toString().padStart(2, '0')}`;

  // Make AJAX request to fetch exercises for the selected date
  const urlWithParams = fetchSchedulesUrl + '?date=' + encodeURIComponent(formattedDate);

  fetch(urlWithParams)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      displayExercises(data);
    })
    .catch(error => console.error('Error fetching exercises:', error));
}

function displayExercises(exercises) {
  const exerciseList = document.getElementById('exercise-list');
  exerciseList.innerHTML = ''; // Clear previous exercises

  // Helper function to create and append the appropriate button
  function createButton(exercise, listItem) {
    if (exercise.available === 0) {
      listItem.classList.add('full');
      const waitlistButton = document.createElement('button');
      waitlistButton.textContent = 'Join waitlist';
      waitlistButton.className = 'waitlist-button';
      listItem.appendChild(waitlistButton);
    } else {
      const bookButton = document.createElement('button');
      bookButton.textContent = 'Book';
      bookButton.className = 'book-button';
      listItem.appendChild(bookButton);
      bookButton.dataset.scheduleId = exercise.id;
      bookButton.addEventListener('click', () => bookClass(bookButton.dataset.scheduleId))
    }
  }

  function bookClass(scheduleId) {
    const selectedCell = document.querySelector(".selected");
    const selectedDate = new Date(currentYear, currentMonth, parseInt(selectedCell.textContent));
    const formattedDate = `${selectedDate.getFullYear()}-${(selectedDate.getMonth() + 1).toString().padStart(2, '0')}-${selectedDate.getDate().toString().padStart(2, '0')}`;
  
    // Prepare form data
    // Prepare JSON data
    const data = {
      class_schedule: scheduleId,
      date: formattedDate
  };

  fetch(bookClassUrl, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') // Make sure to include the CSRF token
      }
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      if (data.status === 'success') {
        alert('Class booked successfully!');
        // Optionally, update the UI to reflect the booking
        selectDate(selectedCell);
      } else {
        alert(data.message || 'Failed to book the class.');
      }
    })
    .catch(error => console.error('Error booking class:', error));
  }
  
  // Function to get CSRF token
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
  
  

  for (let i = 0; i < exercises.length; i++) {
    const exercise = exercises[i];

    const listItem = document.createElement('div');
    listItem.className = 'exercise-item';

    const className = document.createElement('div');
    className.className = 'class-name';
    className.textContent = exercise.classes__class_name;
    listItem.appendChild(className);

    const time = document.createElement('div');
    time.className = 'class-time';
    time.textContent = new Date('1970-01-01T' + exercise.time + 'Z').toLocaleTimeString('en-US', { timeZone: 'UTC', hour: '2-digit', minute: '2-digit' });
    listItem.appendChild(time);

    const duration = document.createElement('div');
    duration.className = 'duration';
    duration.textContent = exercise.duration;
    listItem.appendChild(duration);

    const availability = document.createElement('div');
    availability.className = 'class-availability';
    availability.textContent = `${exercise.available}/${exercise.capacity} available`;
    listItem.appendChild(availability);

    // Call the helper function to create and append the button
    createButton(exercise, listItem);

    exerciseList.appendChild(listItem);
  }
}


showCalendar(currentMonth, currentYear);
