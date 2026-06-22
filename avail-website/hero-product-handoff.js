(function () {
  var DESKTOP_MQ = window.matchMedia('(min-width: 1025px)');
  var REDUCED_MQ = window.matchMedia('(prefers-reduced-motion: reduce)');

  var root;
  var expander;
  var panelImg;
  var handoffSource;
  var productSection;
  var productPanel;
  var productContent;

  var enabled = false;
  var rafId = null;
  var metrics = null;
  var lockedStart = null;
  var restStart = null;
  var HANDOFF_IDLE_SCROLL = 16;

  function isAtHeroRest() {
    return window.scrollY <= HANDOFF_IDLE_SCROLL;
  }

  function captureRestStart() {
    if (!handoffSource || !isAtHeroRest()) return;
    restStart = rectToObject(handoffSource.getBoundingClientRect());
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
  }

  function rectToObject(rect) {
    return {
      top: rect.top,
      left: rect.left,
      width: rect.width,
      height: rect.height
    };
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function applyRect(el, rect) {
    el.style.top = rect.top + 'px';
    el.style.left = rect.left + 'px';
    el.style.width = rect.width + 'px';
    el.style.height = rect.height + 'px';
  }

  function docRect(el) {
    var rect = el.getBoundingClientRect();
    return {
      top: rect.top + window.scrollY,
      left: rect.left + window.scrollX,
      width: rect.width,
      height: rect.height
    };
  }

  function viewportRect(doc) {
    return {
      top: doc.top - window.scrollY,
      left: doc.left - window.scrollX,
      width: doc.width,
      height: doc.height
    };
  }

  function lerpRect(source, target, t) {
    return {
      top: lerp(source.top, target.top, t),
      left: lerp(source.left, target.left, t),
      width: lerp(source.width, target.width, t),
      height: lerp(source.height, target.height, t)
    };
  }

  function getPanelTarget() {
    return rectToObject(productPanel.getBoundingClientRect());
  }

  function measure() {
    if (!enabled || !handoffSource || !productPanel || !productSection) return;

    var productTop = productSection.offsetTop;

    metrics = {
      startScroll: HANDOFF_IDLE_SCROLL,
      endScroll: productTop,
      targetPanel: docRect(productPanel)
    };

    updateScrollPadding();
  }

  function updateScrollPadding() {
    if (!enabled || !root || !metrics) {
      if (root) root.style.paddingBottom = '';
      return;
    }

    var maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    var deficit = Math.max(0, Math.ceil(metrics.endScroll - maxScroll));
    root.style.paddingBottom = deficit > 0 ? deficit + 'px' : '';
  }

  function getProgress() {
    if (!metrics || isAtHeroRest()) return 0;
    var range = metrics.endScroll - metrics.startScroll;
    if (range <= 0) return 0;
    return clamp((window.scrollY - metrics.startScroll) / range, 0, 1);
  }

  function resetToHeroRest() {
    lockedStart = null;
    root.classList.remove('is-expanding', 'is-handoff-complete');
    productSection.classList.add('is-handoff-pending');
    expander.classList.remove('is-visible');
    handoffSource.classList.remove('is-handoff-hidden');
    resetHandoffStyles();
    window.AvailHeroRoll && window.AvailHeroRoll.resume();
  }

  function resetHandoffStyles() {
    if (expander) {
      expander.style.top = '';
      expander.style.left = '';
      expander.style.width = '';
      expander.style.height = '';
      expander.style.opacity = '';
    }
    if (panelImg) panelImg.style.opacity = '';
    if (productContent) {
      productContent.style.opacity = '';
      productContent.style.transform = '';
    }
  }

  function update() {
    rafId = null;
    if (!enabled || !metrics) return;

    var progress = getProgress();
    var eased = easeOutCubic(progress);

    root.style.setProperty('--handoff-progress', String(progress));

    if (isAtHeroRest()) {
      root.style.setProperty('--handoff-progress', '0');
      resetToHeroRest();
      return;
    }

    if (progress >= 1) {
      var justCompleted = !root.classList.contains('is-handoff-complete');
      var panelTarget = getPanelTarget();
      lockedStart = null;
      root.classList.remove('is-expanding');
      root.classList.add('is-handoff-complete');
      applyRect(expander, panelTarget);
      productSection.classList.remove('is-handoff-pending');
      expander.classList.remove('is-visible');
      handoffSource.classList.add('is-handoff-hidden');
      resetHandoffStyles();
      if (justCompleted && metrics && window.scrollY > metrics.endScroll + 1) {
        window.scrollTo(0, metrics.endScroll);
      }
      return;
    }

    root.classList.add('is-expanding');
    root.classList.remove('is-handoff-complete');
    productSection.classList.add('is-handoff-pending');
    if (!lockedStart) {
      lockedStart = restStart || rectToObject(handoffSource.getBoundingClientRect());
    }

    expander.classList.add('is-visible');
    handoffSource.classList.add('is-handoff-hidden');
    window.AvailHeroRoll && window.AvailHeroRoll.pause();
    if (panelImg) panelImg.style.opacity = '1';

    var source = lockedStart;
    var panelTarget = getPanelTarget();
    var frame = lerpRect(source, panelTarget, eased);

    applyRect(expander, frame);

    var contentProgress = easeOutCubic(clamp((progress - 0.5) / 0.5, 0, 1));
    productContent.style.opacity = String(contentProgress);
    productContent.style.transform = 'translateY(' + (16 * (1 - contentProgress)) + 'px)';
  }

  function requestUpdate() {
    if (isAtHeroRest()) captureRestStart();
    if (rafId !== null) return;
    rafId = window.requestAnimationFrame(update);
  }

  function onScrollEnd() {
    if (!enabled || !metrics) return;

    if (rafId !== null) {
      window.cancelAnimationFrame(rafId);
      rafId = null;
    }
    update();

    if (root.classList.contains('is-handoff-complete')) {
      if (window.scrollY > metrics.endScroll + 1 && window.scrollY < metrics.endScroll + 80) {
        window.scrollTo(0, metrics.endScroll);
      }
    }
  }

  function enable() {
    if (enabled) return;
    enabled = true;
    root.classList.add('is-handoff-enabled');
    measure();
    captureRestStart();
    requestUpdate();
    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('scrollend', onScrollEnd);
    window.addEventListener('resize', onResize);
  }

  function disable() {
    if (!enabled) return;
    enabled = false;
    root.classList.remove('is-handoff-enabled', 'is-expanding', 'is-handoff-complete');
    productSection.classList.remove('is-handoff-pending');
    root.style.paddingBottom = '';
    expander.classList.remove('is-visible');
    handoffSource.classList.remove('is-handoff-hidden');
    resetHandoffStyles();
    window.removeEventListener('scroll', requestUpdate);
    window.removeEventListener('scrollend', onScrollEnd);
    window.removeEventListener('resize', onResize);
    if (rafId !== null) {
      window.cancelAnimationFrame(rafId);
      rafId = null;
    }
  }

  function onResize() {
    measure();
    captureRestStart();
    requestUpdate();
  }

  function onMediaChange() {
    if (DESKTOP_MQ.matches && !REDUCED_MQ.matches) {
      enable();
    } else {
      disable();
    }
  }

  function init() {
    root = document.getElementById('hero-handoff');
    expander = document.getElementById('hero-handoff-expander');
    panelImg = document.getElementById('hero-handoff-panel-img');
    handoffSource = document.querySelector('[data-handoff-source]');
    productSection = document.querySelector('#hero-handoff .product--nexus');
    productPanel = document.querySelector('#hero-handoff [data-handoff-panel]');
    productContent = document.querySelector('#hero-handoff [data-handoff-content]');

    if (!root || !expander || !handoffSource || !productPanel) return;

    if (typeof DESKTOP_MQ.addEventListener === 'function') {
      DESKTOP_MQ.addEventListener('change', onMediaChange);
      REDUCED_MQ.addEventListener('change', onMediaChange);
    } else if (typeof DESKTOP_MQ.addListener === 'function') {
      DESKTOP_MQ.addListener(onMediaChange);
      REDUCED_MQ.addListener(onMediaChange);
    }

    onMediaChange();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
