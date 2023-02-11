let calendarContainer = document.querySelector(".calendar");

let data =
[
    {
        "text": "hAPPY DAY",
        "date_time": "2023-02-10 16:52:51.779204",
        "emotion": "Positive",
        "Name": "Development"
    },
    {
      "text": "Did you know that today is a happy day?",
      "date_time": "2023-02-9 16:52:51.779204",
      "emotion": "Positive",
      "Name": "Development"
  },
  {
    "text": "Sexy Day",
    "date_time": "2023-02-8 16:52:51.779204",
    "emotion": "Positive",
    "Name": "Development"
},
{
  "text": "Sad Day",
  "date_time": "2023-02-7 16:52:51.779204",
  "emotion": "Negative",
  "Name": "Development"
},
];

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