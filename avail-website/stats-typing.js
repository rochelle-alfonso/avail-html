(function (global) {
  var section;
  var cards = [];
  var triggered = false;
  var observer;

  var CHAR_MS = 75;
  var CARD_STAGGER_MS = 280;

  function prefersReducedMotion() {
    return global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function prepareCards() {
    cards = Array.prototype.slice.call(section.querySelectorAll('.stats__card')).map(function (card) {
      var valueEl = card.querySelector('.stats__value');
      var labelEl = card.querySelector('.stats__label');
      var valueText = valueEl ? (valueEl.getAttribute('data-value') || valueEl.textContent.trim()) : '';
      var labelText = labelEl ? (labelEl.getAttribute('data-value') || labelEl.textContent.trim()) : '';

      if (valueEl) {
        valueEl.setAttribute('data-value', valueText);
        valueEl.textContent = '';
      }
      if (labelEl) {
        labelEl.setAttribute('data-value', labelText);
        labelEl.textContent = '';
      }

      return { valueEl: valueEl, labelEl: labelEl, valueText: valueText, labelText: labelText };
    });
  }

  function typeText(el, text, typingClass, done) {
    if (!el || !text) {
      if (done) done();
      return;
    }

    el.textContent = '';
    el.classList.add(typingClass);
    var index = 0;

    function tick() {
      if (index >= text.length) {
        el.classList.remove(typingClass);
        if (done) done();
        return;
      }
      el.textContent += text.charAt(index);
      index += 1;
      global.setTimeout(tick, CHAR_MS);
    }

    tick();
  }

  function revealAll() {
    cards.forEach(function (card) {
      if (card.valueEl) card.valueEl.textContent = card.valueText;
      if (card.labelEl) card.labelEl.textContent = card.labelText;
    });
    section.classList.add('is-typed');
  }

  function animateAll() {
    if (triggered) return;
    triggered = true;
    if (observer) observer.disconnect();

    section.classList.add('is-typing');

    if (prefersReducedMotion()) {
      revealAll();
      section.classList.remove('is-typing');
      section.classList.add('is-typed');
      return;
    }

    cards.forEach(function (card, cardIndex) {
      global.setTimeout(function () {
        typeText(card.valueEl, card.valueText, 'stats__value--typing', function () {
          typeText(card.labelEl, card.labelText, 'stats__label--typing', function () {
            if (cardIndex === cards.length - 1) {
              section.classList.remove('is-typing');
              section.classList.add('is-typed');
            }
          });
        });
      }, cardIndex * CARD_STAGGER_MS);
    });
  }

  function init() {
    section = document.querySelector('.stats');
    if (!section) return;

    prepareCards();

    if (prefersReducedMotion()) {
      revealAll();
      return;
    }

    observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) animateAll();
        });
      },
      { threshold: 0.35, rootMargin: '0px 0px -8% 0px' }
    );

    observer.observe(section);

    var rect = section.getBoundingClientRect();
    if (rect.top < global.innerHeight * 0.85 && rect.bottom > 0) {
      animateAll();
    }
  }

  global.AvailStatsTyping = { init: init };
})(window);
