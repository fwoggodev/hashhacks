let data = [
    {
      "text": "Hello World\nHappy today\nhappy day today\nasdsadsd ",
      "date_time": "2023-02-11 16:52:51.779204",
      "emotion": "Positive",
      "Name": "Development"
    }
  ];

  for (let i = 0; i < data.length; i++) {
    let date = new Date(data[i].date_time);
    let dateString = date.getDate();
    let day = date.toLocaleString("default", { weekday: "long" });
    let emotion = data[i].emotion;

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

    card.appendChild(dateElement);
    card.appendChild(emotionElement);
    dayContainer.appendChild(card);

    document.querySelector(".calendar").appendChild(dayContainer);
  }