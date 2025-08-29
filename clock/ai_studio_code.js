// Start the clock
let lastTime = new Date();
setInterval(updateClock, 1000);

function updateClock() {
  const currentTime = new Date();
  const hours = currentTime.getHours();
  const minutes = currentTime.getMinutes();
  const seconds = currentTime.getSeconds();
  
  const lastHours = lastTime.getHours();
  const lastMinutes = lastTime.getMinutes();
  const lastSeconds = lastTime.getSeconds();

  flipTimeSlot(document.querySelector(".hours"), hours, lastHours);
  flipTimeSlot(document.querySelector(".minutes"), minutes, lastMinutes);
  flipTimeSlot(document.querySelector(".seconds"), seconds, lastSeconds);

  lastTime = currentTime;
}

function flipTimeSlot(container, newTime, lastTime) {
  const newTimeStr = String(newTime).padStart(2, "0");
  const lastTimeStr = String(lastTime).padStart(2, "0");

  const tensDigitCard = container.querySelector("[data-digit-tens]");
  if (newTimeStr[0] !== lastTimeStr[0]) {
    flip(tensDigitCard, newTimeStr[0]);
  }

  const onesDigitCard = container.querySelector("[data-digit-ones]");
  if (newTimeStr[1] !== lastTimeStr[1]) {
    flip(onesDigitCard, newTimeStr[1]);
  }
}

function flip(flipCard, newNumber) {
  const currentNumber = flipCard.getAttribute('data-current-number') || '0';
  flipCard.setAttribute('data-current-number', newNumber);
  flipCard.setAttribute('data-next-number', newNumber);

  // Prevent re-animating if the number is already correct
  if (currentNumber === newNumber) return;

  flipCard.addEventListener("transitionend", () => {
    flipCard.classList.remove("flip");
  }, { once: true });

  flipCard.classList.add("flip");
}

// Initialize the clock on load
updateClock();