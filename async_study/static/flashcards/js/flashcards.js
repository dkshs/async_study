function showAnswer(id) {
  const button = document.getElementById(`answer-btn-${id}`);
  const answer = document.getElementById(`answer-${id}`);
  if (answer.classList.contains("hidden")) {
    answer.classList.remove("animate-disappear");
    answer.classList.add("animate-appear");
    answer.classList.remove("hidden");
    button.innerHTML = "Hide Answer";
  } else {
    answer.classList.remove("animate-appear");
    answer.classList.add("animate-disappear");
    button.innerHTML = `
      <i class="ph-bold ph-spinner animate-spin mr-1"></i>
      Hiding...
    `;
    setTimeout(() => {
      answer.classList.add("hidden");
      button.innerHTML = "Show Answer";
    }, 500);
  }
}
