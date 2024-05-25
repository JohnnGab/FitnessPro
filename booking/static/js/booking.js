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
  let currentDayCell = null;

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
          currentDayCell = cell;
        }
        cell.addEventListener("click", () => {
          const selectedDate = new Date(currentYear, currentMonth, parseInt(cell.textContent));
          if (selectedDate >= today) {
            selectDate(cell);
          }
        });
        date++;
      }
    }
    calendar.appendChild(row);
  }
  
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

  const urlWithParams = fetchSchedulesUrl + '?date=' + encodeURIComponent(formattedDate);

  fetch(urlWithParams)
    .then(response => response.json())
    .then(data => {
      displayExercises(data);
    })
    .catch(error => console.error('Error fetching exercises:', error));
}

function displayExercises(exercises) {
  const exerciseList = document.getElementById('exercise-list');
  exerciseList.innerHTML = '';

  exercises.forEach(exercise => {
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

    createButton(exercise, listItem);
    exerciseList.appendChild(listItem);
  });
}

function createButton(exercise, listItem) {
  const bookButton = document.createElement('button');
  bookButton.dataset.scheduleId = exercise.id;
  console.log(exercise.reservation_id)
  if (exercise.reservation_id) {
    bookButton.textContent = 'Cancel Booking';
    bookButton.className = 'booked-button';
    bookButton.addEventListener('click', () => cancelBooking(exercise.reservation_id, bookButton));
  } else {
    bookButton.textContent = exercise.available === 0 ? 'Join waitlist' : 'Book';
    bookButton.className = exercise.available === 0 ? 'waitlist-button' : 'book-button';
    bookButton.addEventListener('click', () => bookClass(exercise.id, bookButton));
  }
  listItem.appendChild(bookButton);
}

  function bookClass(scheduleId, bookButton) {
    const selectedCell = document.querySelector(".selected");
    const selectedDate = new Date(currentYear, currentMonth, parseInt(selectedCell.textContent));
    const formattedDate = `${selectedDate.getFullYear()}-${(selectedDate.getMonth() + 1).toString().padStart(2, '0')}-${selectedDate.getDate().toString().padStart(2, '0')}`;
    
    // Prepare JSON data
    const data = {
      class_schedule: scheduleId,
      date: formattedDate
  };

  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  fetch(bookClassUrl, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
      }
  })
  .then(response => {
    if (response.redirected) { 
      window.location.href = response.url;
      return;
    } 
    return response.json();
  })
  .then(data => {
    if (data && data.status === 'success') {
      selectDate(document.querySelector(".selected"));
      } else {
      alert(data.message || 'Failed to book the class.');
      }
    })
    .catch(error => console.error('Error booking class:', error));
  }

  function cancelBooking(reservationId, bookButton) {

  const deleteReservationUrlWithParams = deleteReservationUrl + '?id=' + encodeURIComponent(reservationId);
  const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  fetch(deleteReservationUrlWithParams, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        selectDate(document.querySelector(".selected"));
      } else {
        alert(data.message || 'Failed to delete the reservation.');
      }
    })
    .catch(error => console.error('Error deleting reservation:', error));
}

showCalendar(currentMonth, currentYear);