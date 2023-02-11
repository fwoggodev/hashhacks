
document.addEventListener("DOMContentLoaded", function() {
  const submitButton = document.getElementById("submit-button");
const textInput = document.getElementById("text-input");
const result = document.getElementById("result");

submitButton.addEventListener("click", function() {
  const text = textInput.value;

  fetch("http://127.0.0.1:9999/journal", {
    method: "POST",
    body: JSON.stringify({
      text: text,
      name: "Development"
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  })
    .then(response => response.json())
    .then(json => {
      result.innerHTML = json.id;
    });
});

});

