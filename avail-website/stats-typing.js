(function (global) {
  var section;
  var cards = [];
  var triggered = false;
  var observer;

  var LOADER_MS = 900;
  var CARD_STAGGER_MS = 220;

  function prefersReducedMotion() {
    return global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function prepareCards() {
    cards = Array.prototype.slice.call(section.querySelectorAll('.stats__card')).map(function (card) {
      var valueEl = card.querySelector('.stats__value');
      var labelEl = card.querySelector('.stats__label');
      var valueText = valueEl ? (valueEl.getAttribute('data-value') || '').trim() : '';
      var labelText = labelEl ? (labelEl.getAttribute('data-value') || '').trim() : '';

      card.classList.add('is-loading');

      return {
        card: card,
        valueEl: valueEl,
        labelEl: labelEl,
        valueText: valueText,
        labelText: labelText
      };
    });
  }

  function revealCard(cardData) {
    if (cardData.valueEl) cardData.valueEl.textContent = cardData.valueText;
    if (cardData.labelEl) cardData.labelEl.textContent = cardData.labelText;
    cardData.card.classList.remove('is-loading');
    cardData.card.classList.add('is-loaded');
  }

  function revealAll() {
    cards.forEach(revealCard);
    section.classList.add('is-loaded');
  }

  function animateAll() {
    if (triggered) return;
    triggered = true;
    if (observer) observer.disconnect();

    if (prefersReducedMotion()) {
      revealAll();
      return;
    }

    cards.forEach(function (cardData, index) {
      global.setTimeout(function () {
        revealCard(cardData);
        if (index === cards.length - 1) {
          section.classList.add('is-loaded');
        }
      }, LOADER_MS + index * CARD_STAGGER_MS);
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
