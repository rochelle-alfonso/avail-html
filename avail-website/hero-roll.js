(function (global) {
  var slides = [];
  var current = 0;
  var timer = null;
  var paused = false;
  var holdMs = 1500;

  function tick() {
    if (paused || slides.length < 2) return;
    slides[current].classList.remove('is-active');
    current = (current + 1) % slides.length;
    slides[current].classList.add('is-active');
  }

  function init() {
    slides = Array.prototype.slice.call(document.querySelectorAll('.hero-roll__slide'));
    if (slides.length < 2) return;
    if (global.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    timer = global.setInterval(tick, holdMs);
  }

  global.AvailHeroRoll = {
    init: init,
    pause: function () {
      paused = true;
    },
    resume: function () {
      paused = false;
    },
    getActiveSlide: function () {
      return slides[current] || null;
    },
    getActiveImage: function () {
      var slide = slides[current];
      return slide ? slide.querySelector('img') : null;
    }
  };
})(window);
