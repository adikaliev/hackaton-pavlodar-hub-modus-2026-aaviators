// Small progressive enhancements. Every page works without this file; it only removes clicks.
(function () {
  "use strict";

  // Role switcher (demo): choosing a person reloads the app as that person.
  var persona = document.getElementById("persona");
  if (persona) {
    persona.addEventListener("change", function () {
      window.location = window.SWITCH_URL + "?id=" + encodeURIComponent(persona.value);
    });
  }

  // Confirmation for destructive demo controls.
  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!window.confirm(form.dataset.confirm)) event.preventDefault();
    });
  });

  // Blocks that are shown only while a checkbox or radio is selected: data-show-when="#id".
  function syncToggles() {
    document.querySelectorAll("[data-show-when]").forEach(function (block) {
      var control = document.querySelector(block.dataset.showWhen);
      block.classList.toggle("hidden", !(control && control.checked));
    });
  }
  document.addEventListener("change", syncToggles);
  syncToggles();

  // Profile: while the Telegram link is on screen, check every few seconds whether the phone has linked,
  // so a QR code scanned from a computer screen turns into "linked" without a manual reload.
  var telegramWait = document.querySelector("[data-telegram-wait]");
  if (telegramWait) {
    var checks = 0;
    var poll = window.setInterval(function () {
      if (document.hidden) return;
      if (++checks > 200) { window.clearInterval(poll); return; }  // stop after about ten minutes
      fetch(telegramWait.dataset.telegramWait, { credentials: "same-origin" })
        .then(function (response) { return response.ok ? response.json() : null; })
        .then(function (data) { if (data && data.linked) window.location.reload(); })
        .catch(function () { /* the button and a manual reload still work */ });
    }, 3000);
  }

  // Submission form: suggest a category and show similar requests while the author types.
  var text = document.getElementById("appeal-text");
  var hints = document.getElementById("hints");
  var category = document.getElementById("category");
  var suggestion = document.getElementById("category-suggestion");
  if (text && hints && category) {
    var timer = null;
    var chosenByHand = Boolean(category.value);
    category.addEventListener("change", function () { chosenByHand = true; suggestion.classList.add("hidden"); });

    var ask = function () {
      if (text.value.trim().length < 20) { hints.innerHTML = ""; return; }
      fetch(window.HINTS_URL + "?q=" + encodeURIComponent(text.value), { credentials: "same-origin" })
        .then(function (response) { return response.ok ? response.json() : null; })
        .then(function (data) {
          if (!data) return;
          hints.innerHTML = data.html;
          if (data.category_id && !chosenByHand && String(category.value) !== String(data.category_id)) {
            suggestion.classList.remove("hidden");
            suggestion.querySelector("b").textContent = data.category_name;
            suggestion.querySelector("button").onclick = function () {
              category.value = data.category_id;
              suggestion.classList.add("hidden");
            };
          } else {
            suggestion.classList.add("hidden");
          }
        })
        .catch(function () { /* hints are optional */ });
    };
    text.addEventListener("input", function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(ask, 450);
    });
  }
})();
