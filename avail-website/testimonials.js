(function (global) {
  var root;
  var viewport;
  var track;
  var logosContainer;
  var origSlides = [];
  var allSlides = [];
  var logos = [];
  var progressFill;
  var total = 0;

  var pos = 0; // actual track index currently shown (0..total, where `total` is the loop clone)
  var minOffset = 0; // px offset that centers the first card
  var step = 0; // card width + gap
  var animating = false;
  var autoplayTimer = null;
  var paused = false;
  var prefersReducedMotion = false;
  var scrollSyncTimer = null;
  var isAutoScrolling = false;
  var autoScrollTimer = null;

  var DURATION = 600; // ms, must match the CSS transition below
  var AUTOPLAY_MS = 5000;

  function buildClones() {
    // One trailing clone of the full set lets us advance past the last card and
    // snap back to the first without a visible jump.
    origSlides.forEach(function (slide) {
      var clone = slide.cloneNode(true);
      clone.removeAttribute('id');
      clone.setAttribute('aria-hidden', 'true');
      clone.classList.add('is-clone');
      clone.removeAttribute('data-index');
      track.appendChild(clone);
    });
    allSlides = Array.prototype.slice.call(track.querySelectorAll('.testimonials__slide'));
  }

  function measure() {
    if (total < 1) return;
    var first = origSlides[0];
    var slideWidth = first.offsetWidth;
    step = total > 1 ? origSlides[1].offsetLeft - first.offsetLeft : slideWidth;
    minOffset = first.offsetLeft - (viewport.clientWidth - slideWidth) / 2;
  }

  function isMobile() {
    return global.matchMedia && global.matchMedia('(max-width: 460px)').matches;
  }

  function translateTo(i, animate) {
    track.style.transition = animate ? 'transform ' + DURATION + 'ms ease' : 'none';
    track.style.transform = 'translateX(' + -(minOffset + i * step) + 'px)';
  }

  function updateProgress(index) {
    if (!progressFill) return;
    progressFill.style.transform = isMobile() ? 'translateX(0)' : 'translateX(' + index * 100 + '%)';
  }

  function updateLogos(index) {
    logos.forEach(function (logo, i) {
      var isActive = i === index;
      logo.classList.toggle('is-active', isActive);
      logo.setAttribute('aria-selected', String(isActive));
      logo.setAttribute('tabindex', isActive ? '0' : '-1');
    });
  }

  function updateActiveSlide(index) {
    allSlides.forEach(function (slide, j) {
      slide.classList.toggle('is-active', j % total === index);
    });
  }

  function setActive(index, scrollLogo) {
    updateActiveSlide(index);
    updateLogos(index);
    updateProgress(index);
    if (scrollLogo) scrollActiveLogoIntoView(index);
  }

  function next() {
    if (animating) return;
    var target = pos + 1;
    animating = true;
    translateTo(target, true);
    setActive(target % total, true);
    global.setTimeout(function () {
      if (target >= total) {
        pos = 0;
        translateTo(0, false);
      } else {
        pos = target;
      }
      animating = false;
    }, DURATION);
  }

  function goTo(index, scrollLogo) {
    if (animating || index === pos % total) {
      setActive(index, scrollLogo);
      return;
    }
    animating = true;

    // Going backward from the first card: hop to the trailing clone instantly,
    // then animate into the target so the motion direction reads correctly.
    if (index < pos) {
      translateTo(total, false);
      // force reflow so the next transition runs from the clone position
      void track.offsetWidth;
      pos = total;
    }

    translateTo(index, true);
    setActive(index, scrollLogo);
    global.setTimeout(function () {
      pos = index;
      animating = false;
    }, DURATION);
  }

  function scrollActiveLogoIntoView(index) {
    var logo = logos[index];
    if (!logo || !logosContainer) return;
    if (logosContainer.scrollWidth <= logosContainer.clientWidth + 1) return;
    var targetLeft = logo.offsetLeft - (logosContainer.clientWidth - logo.clientWidth) / 2;

    isAutoScrolling = true;
    if (autoScrollTimer) clearTimeout(autoScrollTimer);
    autoScrollTimer = setTimeout(function () {
      isAutoScrolling = false;
    }, 500);

    logosContainer.scrollTo({ left: targetLeft, behavior: 'smooth' });
  }

  function onLogosScroll() {
    if (isAutoScrolling) return;
    if (!logosContainer || logosContainer.scrollWidth <= logosContainer.clientWidth + 1) return;
    if (scrollSyncTimer) clearTimeout(scrollSyncTimer);
    scrollSyncTimer = setTimeout(function () {
      var center = logosContainer.scrollLeft + logosContainer.clientWidth / 2;
      var closest = 0;
      var minDist = Infinity;
      logos.forEach(function (logo, i) {
        var logoCenter = logo.offsetLeft + logo.clientWidth / 2;
        var dist = Math.abs(logoCenter - center);
        if (dist < minDist) {
          minDist = dist;
          closest = i;
        }
      });
      goTo(closest, false);
      restartAutoplay();
    }, 90);
  }

  function startAutoplay() {
    if (prefersReducedMotion || total < 2 || paused) return;
    stopAutoplay();
    autoplayTimer = global.setInterval(next, AUTOPLAY_MS);
  }

  function stopAutoplay() {
    if (autoplayTimer) {
      global.clearInterval(autoplayTimer);
      autoplayTimer = null;
    }
  }

  function restartAutoplay() {
    stopAutoplay();
    startAutoplay();
  }

  function onLogoClick(event) {
    var button = event.currentTarget;
    var index = Number(button.getAttribute('data-index'));
    if (Number.isNaN(index)) return;
    goTo(index, true);
    restartAutoplay();
  }

  function onKeyDown(event) {
    if (!root || !root.contains(event.target)) return;
    var index = pos % total;
    var nextIndex = index;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') {
      nextIndex = (index + 1) % total;
    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') {
      nextIndex = (index - 1 + total) % total;
    } else {
      return;
    }
    event.preventDefault();
    goTo(nextIndex, true);
    restartAutoplay();
    if (logos[nextIndex]) logos[nextIndex].focus();
  }

  function onResize() {
    measure();
    translateTo(pos, false);
  }

  function init() {
    root = document.querySelector('.testimonials');
    if (!root) return;

    viewport = root.querySelector('.testimonials__viewport');
    track = root.querySelector('.testimonials__track');
    origSlides = Array.prototype.slice.call(root.querySelectorAll('.testimonials__slide'));
    logos = Array.prototype.slice.call(root.querySelectorAll('.testimonials__logo'));
    progressFill = root.querySelector('.testimonials__progress-fill');
    logosContainer = root.querySelector('.testimonials__logos');
    total = origSlides.length;

    if (!viewport || !track || total < 1) return;

    origSlides.forEach(function (slide) {
      slide.removeAttribute('hidden');
      slide.removeAttribute('aria-hidden');
    });

    buildClones();
    measure();
    translateTo(0, false);

    logos.forEach(function (logo) {
      logo.addEventListener('click', onLogoClick);
    });

    if (logosContainer) {
      logosContainer.addEventListener('scroll', onLogosScroll, { passive: true });
    }

    root.addEventListener('keydown', onKeyDown);

    global.addEventListener('resize', onResize);

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        stopAutoplay();
      } else {
        startAutoplay();
      }
    });

    var motionQuery = global.matchMedia && global.matchMedia('(prefers-reduced-motion: reduce)');
    prefersReducedMotion = !!(motionQuery && motionQuery.matches);
    if (motionQuery && motionQuery.addEventListener) {
      motionQuery.addEventListener('change', function (event) {
        prefersReducedMotion = event.matches;
        if (prefersReducedMotion) {
          stopAutoplay();
        } else {
          startAutoplay();
        }
      });
    }

    setActive(0, false);
    startAutoplay();
  }

  global.AvailTestimonials = {
    init: init,
    goTo: function (index) {
      goTo(index, true);
      restartAutoplay();
    }
  };
})(window);
