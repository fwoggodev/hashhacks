let calendarContainer = document.querySelector(".calendar");

fetch('http://127.0.0.1:9999/journalist')
  .then(response => response.json())
  .then(data => {
    for (let i = 0; i < data.length; i++) {
      let date = new Date(data[i].date_time);
      let dateString = date.getDate();
      let day = date.toLocaleString("default", { weekday: "long" });
      let emotion = data[i].emotion;
      let text = data[i].text;

      let dayContainer = document.createElement("div");
      dayContainer.classList.add("day");
      let card = document.createElement("div");
      card.classList.add("entry-card");
      let dateElement = document.createElement("div");
      dateElement.classList.add("date");
      dateElement.innerText = day + " " + dateString;
      let emotionElement = document.createElement("div");
      emotionElement.classList.add("emotion");
      emotionElement.innerText = emotion;
      let textElement = document.createElement("div");
      textElement.classList.add("text");
      textElement.innerText = text;

      card.appendChild(dateElement);
      card.appendChild(emotionElement);
      card.appendChild(textElement);
      dayContainer.appendChild(card);

      card.addEventListener("click", function() {
        textElement.style.display = textElement.style.display === "none" ? "block" : "none";
      });

      calendarContainer.appendChild(dayContainer);
    }
  })
  .catch(error => {
    console.error('Error loading journal data:', error);
  });