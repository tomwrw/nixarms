// The Nix Arms - progressive enhancement only. Every control works as a plain link without JavaScript.
(function () {
  "use strict";

  // Header: on phones, collapse the links behind a toggle button.
  // CSS only collapses them once this has run (.nav--js), so without JavaScript every link stays visible.
  var nav = document.querySelector("[data-nav]");
  var toggle = nav && nav.querySelector("[data-nav-toggle]");
  if (nav && toggle) {
    nav.classList.add("nav--js");
    toggle.hidden = false;
    var setOpen = function (open) {
      nav.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close site navigation" : "Open site navigation");
    };
    toggle.addEventListener("click", function () {
      setOpen(!nav.classList.contains("is-open"));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
    // Close after following a same-page link (e.g. "Pull up a stool" on the homepage).
    nav.querySelectorAll(".nav-links a").forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
  }

  // Links given role="button" should also respond to Space, as real buttons do.
  var spaceClicks = function (el) {
    el.addEventListener("keydown", function (e) {
      if (e.key === " ") {
        e.preventDefault();
        el.click();
      }
    });
  };

  // Path picker: pills become tabs that swap the panel in place.
  document.querySelectorAll("[data-picker]").forEach(function (picker) {
    var pills = picker.querySelectorAll(".pill[data-panel]");
    pills.forEach(function (pill) {
      pill.setAttribute("role", "button");
      spaceClicks(pill);
      pill.setAttribute("aria-pressed", pill.classList.contains("is-active") ? "true" : "false");
      pill.addEventListener("click", function (e) {
        e.preventDefault();
        pills.forEach(function (p) {
          var on = p === pill;
          p.classList.toggle("is-active", on);
          p.setAttribute("aria-pressed", on ? "true" : "false");
          var panel = document.getElementById(p.dataset.panel);
          if (panel) panel.hidden = !on;
        });
      });
    });
  });

  // Regulars filter: chips filter the grid in place.
  document.querySelectorAll("[data-filter]").forEach(function (bar) {
    var grid = document.querySelector("[data-filter-grid]");
    var count = bar.querySelector("[data-count]");
    if (!grid) return;
    var chips = bar.querySelectorAll(".pill[data-tag]");
    var cards = grid.querySelectorAll("[data-tags]");
    chips.forEach(function (chip) {
      chip.setAttribute("role", "button");
      spaceClicks(chip);
      chip.setAttribute("aria-pressed", chip.classList.contains("is-active") ? "true" : "false");
      chip.addEventListener("click", function (e) {
        e.preventDefault();
        var tag = chip.dataset.tag;
        var shown = 0;
        chips.forEach(function (c) {
          var on = c === chip;
          c.classList.toggle("is-active", on);
          c.setAttribute("aria-pressed", on ? "true" : "false");
        });
        cards.forEach(function (card) {
          var match = tag === "all" || card.dataset.tags.split(" ").indexOf(tag) !== -1;
          card.hidden = !match;
          if (match) shown++;
        });
        if (count) count.textContent = "Showing " + shown + (shown === 1 ? " config" : " configs");
      });
    });
  });

  // One for the road: show a random tip; "Another round" pours a different one.
  // Without JavaScript the first tip shows and the button stays hidden.
  document.querySelectorAll("[data-tips]").forEach(function (board) {
    var tips = board.querySelectorAll("[data-tip]");
    var next = board.querySelector("[data-tip-next]");
    if (tips.length < 2) return;
    var current = 0;
    function show(i) {
      tips.forEach(function (t, j) { t.hidden = j !== i; });
      current = i;
    }
    function pick() {
      var i = Math.floor(Math.random() * (tips.length - 1));
      return i >= current ? i + 1 : i; // never the same tip twice in a row
    }
    show(Math.floor(Math.random() * tips.length));
    if (next) {
      next.hidden = false;
      next.addEventListener("click", function () { show(pick()); });
    }
  });

  // Copy buttons on code blocks.
  document.querySelectorAll(".prose .highlight, .chalkboard .highlight").forEach(function (block) {
    if (!navigator.clipboard) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", function () {
      var code = block.querySelector("code");
      navigator.clipboard.writeText(code ? code.innerText : "").then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy"; }, 1600);
      });
    });
    block.classList.add("has-copy");
    block.appendChild(btn);
  });
})();
