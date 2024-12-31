// TEST PAGE modal

document.addEventListener("DOMContentLoaded", function () {
    const overlay = document.querySelector(".overlay");
    const dropdown = document.querySelector(".dropdown");
    const selectedOptionsContainer =
      document.querySelector(".selected-options");

    overlay.addEventListener("click", () => {
      overlay.classList.add("hidden");
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        overlay.classList.add("hidden");
      }
    });

    for (let i = 1; i < 10; i++) {
      dropdown.innerHTML += `<div class="option-units">
            <img src="./images/open-tick.svg" alt="tick" /> Unit ${i}
          </div>`;
    }

    const unitOptions = document.querySelectorAll(".option-units");

    unitOptions.forEach((option) => {
      option.addEventListener("click", () => {
        const img = option.querySelector("images");
        const unitText = option.textContent.trim();

        if (!option.classList.contains("done")) {
          option.classList.add("done");
          img.src = "./images/full-tick.svg";

          const selectedOption = document.createElement("span");
          selectedOption.classList.add("selected");
          selectedOption.innerHTML = `${unitText} <span class="close">&#10005;</span>`;
          selectedOptionsContainer.appendChild(selectedOption);

          selectedOption
            .querySelector(".close")
            .addEventListener("click", () => {
              selectedOption.remove();
              option.classList.remove("done");
              img.src = "./images/open-tick.svg";
            });
        } else {
          option.classList.remove("done");
          img.src = "./images/open-tick.svg";
        }
      });
    });
  });