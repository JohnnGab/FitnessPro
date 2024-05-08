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
        }
        cell.addEventListener("click", () => selectDate(cell));
        date++;
      }
    }
    calendar.appendChild(row);
  }
}

function selectDate(cell) {
  document.querySelector(".selected").classList.remove("selected");
  cell.classList.add("selected");
}

showCalendar(currentMonth, currentYear);