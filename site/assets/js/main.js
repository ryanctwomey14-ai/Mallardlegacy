/* Mallard Legacy Partners — interaction layer
   Motion budget: entrance choreography once per page load, scroll reveals,
   and hover feedback. Nothing animates that a visitor triggers dozens of
   times a day. Everything degrades to a static page without JS. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- 1. Hero entrance ----------------------------------------------
     Purpose: state indication — the page has finished loading and is ready.
     Fires once, on load only. Masked lines rise, supporting elements fade. */
  function startHero() {
    document.documentElement.classList.add('is-ready');
  }
  if (document.readyState === 'complete') {
    startHero();
  } else {
    window.addEventListener('load', startHero);
    // Failsafe so content is never trapped behind a stalled font/image load
    setTimeout(startHero, 1200);
  }

  /* ---- 1b. Background video --------------------------------------------
     Purpose: atmosphere. Sources are attached here rather than in the markup
     so narrow viewports and reduced-motion users never fetch the files at
     all. A poster or still sits underneath throughout, so every failure path
     -- no JS, blocked autoplay, 404, unsupported codec -- lands on an image. */
  var bgVideos = document.querySelectorAll('[data-video-mp4]');
  if (bgVideos.length && !reduceMotion && window.matchMedia('(min-width: 900px)').matches) {
    bgVideos.forEach(function (video) {
      [['webm', 'video/webm'], ['mp4', 'video/mp4']].forEach(function (pair) {
        var src = video.getAttribute('data-video-' + pair[0]);
        if (!src) return;
        var s = document.createElement('source');
        s.src = src;
        s.type = pair[1];
        video.appendChild(s);
      });
      // Property as well as attribute: Chrome checks the property when
      // deciding whether an autoplay is permitted.
      // Poster is attached here, not in the markup: as an attribute it is
      // fetched even when no source is ever added, so phones paid for two
      // images they never display.
      if (video.dataset.poster) video.poster = video.dataset.poster;
      video.muted = true;
      video.defaultMuted = true;
      var reveal = function () { video.classList.add('is-playing'); };
      ['playing', 'loadeddata', 'canplay'].forEach(function (evt) {
        video.addEventListener(evt, reveal);
      });
      video.load();
      var attempt = video.play();
      // Autoplay policies reject rather than throw; the image is the fallback.
      if (attempt && typeof attempt.catch === 'function') {
        attempt.catch(function () { video.classList.remove('is-playing'); });
      }
    });
  }

  /* ---- 2. Sticky navigation ------------------------------------------
     Purpose: feedback — the bar earns its background only once it overlaps
     content. rAF-throttled so scrolling stays under the frame budget. */
  var nav = document.querySelector('[data-nav]');
  if (nav) {
    var ticking = false;
    var applyNav = function () {
      nav.classList.toggle('nav--scrolled', window.scrollY > 24);
      ticking = false;
    };
    applyNav();
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(applyNav); }
    }, { passive: true });
  }

  /* ---- 3. Mobile drawer ----------------------------------------------- */
  var toggle = document.querySelector('[data-nav-toggle]');
  var drawer = document.querySelector('[data-drawer]');
  if (toggle && drawer) {
    var setDrawer = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      drawer.dataset.open = String(open);
      document.body.style.overflow = open ? 'hidden' : '';
      if (open) {
        var first = drawer.querySelector('a, button');
        if (first) first.focus({ preventScroll: true });
      }
    };
    toggle.addEventListener('click', function () {
      setDrawer(toggle.getAttribute('aria-expanded') !== 'true');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) setDrawer(false);
    });
    // Escape always exits — never trap someone in an overlay
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.dataset.open === 'true') {
        setDrawer(false);
        toggle.focus();
      }
    });
  }

  /* ---- 4. Scroll reveals ---------------------------------------------
     Purpose: preventing a jarring change — sections settle instead of
     snapping in. Observer unobserves after firing; nothing re-animates
     on the way back up, which would be noise. */
  var revealables = document.querySelectorAll('.reveal, .ripple-rule');
  if (!('IntersectionObserver' in window) || reduceMotion) {
    revealables.forEach(function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    revealables.forEach(function (el) { io.observe(el); });

    // Safety net. Content must never be stranded at opacity:0 because an
    // observer failed to fire — anything at or above the fold is revealed
    // unconditionally after 2.5s, whatever the observer did.
    window.setTimeout(function () {
      revealables.forEach(function (el) {
        if (el.classList.contains('in')) return;
        if (el.getBoundingClientRect().top < window.innerHeight) {
          el.classList.add('in');
          io.unobserve(el);
        }
      });
    }, 2500);
  }

  /* ---- 5. Metric count-up --------------------------------------------
     Purpose: explanation — the numbers are the proof, so they get the
     one moment of attention. Reduced motion gets the final value instantly. */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var format = function (value, decimals) {
      return value.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    };
    var run = function (el) {
      var target = parseFloat(el.dataset.count);
      var decimals = parseInt(el.dataset.decimals || '0', 10);
      if (reduceMotion) { el.textContent = format(target, decimals); return; }
      var duration = 1400, start = null;
      var step = function (ts) {
        if (start === null) start = ts;
        var p = Math.min((ts - start) / duration, 1);
        // ease-out cubic: fast first, settles at the end
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = format(target * eased, decimals);
        if (p < 1) window.requestAnimationFrame(step);
      };
      window.requestAnimationFrame(step);
    };
    if (!('IntersectionObserver' in window)) {
      counters.forEach(run);
    } else {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) { run(entry.target); cio.unobserve(entry.target); }
        });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { cio.observe(el); });
    }
  }

  /* ---- 6. FAQ accordion ----------------------------------------------- */
  document.querySelectorAll('[data-faq]').forEach(function (group) {
    group.querySelectorAll('.faq__q').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        if (group.dataset.faq === 'single') {
          group.querySelectorAll('.faq__q[aria-expanded="true"]').forEach(function (other) {
            if (other !== btn) other.setAttribute('aria-expanded', 'false');
          });
        }
        btn.setAttribute('aria-expanded', String(!open));
      });
    });
  });

  /* ---- 7. Forms -------------------------------------------------------
     Front-end validation and a success state. Wire the fetch() to a real
     endpoint (see README) before launch — nothing is transmitted today. */
  document.querySelectorAll('[data-form]').forEach(function (form) {
    var status = form.querySelector('.form-status');

    var validate = function (input) {
      var field = input.closest('.field');
      if (!field) return true;
      var ok = input.checkValidity();
      field.dataset.invalid = String(!ok);
      var err = field.querySelector('.field__error span');
      if (err && !ok) {
        err.textContent = input.validity.valueMissing
          ? (input.dataset.msgRequired || 'This field is required.')
          : (input.dataset.msgInvalid || 'Check the format of this entry.');
      }
      return ok;
    };

    // Validate on blur, not on keystroke — correcting someone mid-word is hostile
    form.querySelectorAll('input, select, textarea').forEach(function (input) {
      input.addEventListener('blur', function () { validate(input); });
      input.addEventListener('input', function () {
        var field = input.closest('.field');
        if (field && field.dataset.invalid === 'true') validate(input);
      });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var inputs = Array.prototype.slice.call(form.querySelectorAll('input, select, textarea'));
      var invalid = inputs.filter(function (i) { return !validate(i); });
      if (invalid.length) {
        invalid[0].focus();
        invalid[0].scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = 'Sending…'; }

      // Replace with your CRM / form endpoint. See README.md.
      window.setTimeout(function () {
        form.reset();
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
        if (status) {
          status.dataset.state = 'ok';
          status.textContent = form.dataset.success ||
            'Thank you. Seth will personally reply within one business day.';
          status.focus();
        }
      }, 700);
    });
  });

  /* ---- 7b. Return illustration ----------------------------------------
     Applies the published target multiples to an amount the visitor picks and
     draws the band between them across the hold. Deliberately a range, never a
     single line: there is no track record behind these numbers, and a lone
     curve reads as a forecast. */
  var calcInput = document.querySelector('[data-calc-input]');
  var calcRange = document.querySelector('[data-calc-range]');
  var calcChart = document.querySelector('[data-calc-chart]');
  if (calcInput && calcRange) {
    var MIN = 100000, MAX = 1000000;
    var LOW = 1.8, HIGH = 2.2, YEARS = 7;
    // Cash yield assumptions behind the split. Stated in the footnote so the
    // breakdown is never presented as a property-specific figure.
    var CASH_LOW = 0.05, CASH_HIGH = 0.07;
    var out = {};
    document.querySelectorAll('[data-calc]').forEach(function (el) {
      out[el.getAttribute('data-calc')] = el;
    });

    var money = function (n) {
      return '$' + Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    };
    var shortMoney = function (n) {
      if (n >= 1e6) return '$' + (n / 1e6).toFixed(n % 1e6 === 0 ? 0 : 1) + 'M';
      return '$' + Math.round(n / 1000) + 'k';
    };
    var clean = function (s) {
      var n = parseInt(String(s).replace(/[^0-9]/g, ''), 10);
      return isNaN(n) ? MIN : n;
    };

    var W = 720, H = 300, PAD_R = 14, PAD_T = 16, PAD_B = 18;
    var NS = 'http://www.w3.org/2000/svg';

    var drawChart = function (p) {
      if (!calcChart) return;
      // Text and dots inside the SVG are in user units, so a 720-wide viewBox
      // rendered at 254px shrinks an 11px label to under 4px. Scale them back
      // up by the inverse of the render ratio so they stay legible on phones.
      var rendered = calcChart.getBoundingClientRect().width || W;
      var k = W / rendered;
      var labelSize = Math.min(Math.max(11 * k, 11), 30);
      var dotR = Math.min(Math.max(5 * k, 5), 13);
      var PAD_L = Math.max(56, labelSize * 4.6);
      var top = p * HIGH, bottom = p;
      var x = function (t) { return PAD_L + (W - PAD_L - PAD_R) * (t / YEARS); };
      var y = function (v) {
        return PAD_T + (H - PAD_T - PAD_B) * (1 - (v - bottom) / (top - bottom));
      };
      // Compound from the principal to each multiple at the end of the hold.
      var lowAt = function (t) { return p * Math.pow(LOW, t / YEARS); };
      var highAt = function (t) { return p * Math.pow(HIGH, t / YEARS); };

      var pts = [], i;
      for (i = 0; i <= 56; i++) pts.push(i / 8);

      var lowPath = pts.map(function (t, n) {
        return (n ? 'L' : 'M') + x(t).toFixed(1) + ' ' + y(lowAt(t)).toFixed(1);
      }).join('');
      var highPath = pts.map(function (t, n) {
        return (n ? 'L' : 'M') + x(t).toFixed(1) + ' ' + y(highAt(t)).toFixed(1);
      }).join('');
      var bandPath = highPath + pts.slice().reverse().map(function (t) {
        return 'L' + x(t).toFixed(1) + ' ' + y(lowAt(t)).toFixed(1);
      }).join('') + 'Z';

      var ticks = [bottom, bottom + (top - bottom) / 2, top];
      var gridSvg = ticks.map(function (v) {
        return '<line class="calc__grid" x1="' + PAD_L + '" y1="' + y(v).toFixed(1) +
               '" x2="' + (W - PAD_R) + '" y2="' + y(v).toFixed(1) + '"/>' +
               '<text class="calc__ylab" x="' + (PAD_L - 10) + '" y="' +
               (y(v) + labelSize * 0.35).toFixed(1) + '" text-anchor="end" font-size="' +
               labelSize.toFixed(1) + '">' + shortMoney(v) + '</text>';
      }).join('');

      calcChart.innerHTML =
        '<defs><linearGradient id="calcGrad" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="#C9A04B" stop-opacity=".46"/>' +
        '<stop offset="1" stop-color="#C9A04B" stop-opacity=".08"/>' +
        '</linearGradient></defs>' +
        gridSvg +
        '<path class="calc__band" d="' + bandPath + '"/>' +
        '<path class="calc__line calc__line--low" d="' + lowPath + '"/>' +
        '<path class="calc__line" d="' + highPath + '"/>' +
        '<line class="calc__base" x1="' + PAD_L + '" y1="' + y(bottom).toFixed(1) +
          '" x2="' + (W - PAD_R) + '" y2="' + y(bottom).toFixed(1) + '"/>' +
        '<line class="calc__exit" x1="' + x(5).toFixed(1) + '" y1="' + PAD_T +
          '" x2="' + x(5).toFixed(1) + '" y2="' + (H - PAD_B) + '"/>' +
        '<circle class="calc__dot" cx="' + x(YEARS).toFixed(1) + '" cy="' +
          y(highAt(YEARS)).toFixed(1) + '" r="' + dotR.toFixed(1) + '"/>' +
        '<circle class="calc__dot" cx="' + x(YEARS).toFixed(1) + '" cy="' +
          y(lowAt(YEARS)).toFixed(1) + '" r="' + dotR.toFixed(1) + '"/>';
    };

    var set = function (key, value) {
      if (out[key]) out[key].textContent = money(value);
    };

    var render = function (amount) {
      // Cash comes from distributions across the hold; equity is whatever the
      // multiple leaves over once capital and those distributions are removed.
      var lowCash = amount * CASH_LOW * YEARS;
      var highCash = amount * CASH_HIGH * YEARS;
      set('lowTotal', amount * LOW);
      set('highTotal', amount * HIGH);
      set('lowCash', lowCash);
      set('highCash', highCash);
      set('lowEquity', amount * (LOW - 1) - lowCash);
      set('highEquity', amount * (HIGH - 1) - highCash);
      set('lowProfit', amount * (LOW - 1));
      set('highProfit', amount * (HIGH - 1));
      drawChart(amount);
    };

    // Typing is not clamped mid-entry — forcing the value to the minimum on
    // every keystroke makes the field impossible to edit. Clamp on blur.
    calcInput.addEventListener('input', function () {
      var raw = clean(calcInput.value);
      calcInput.value = raw ? raw.toLocaleString('en-US') : '';
      calcRange.value = Math.min(Math.max(raw, MIN), MAX);
      render(raw);
    });
    calcInput.addEventListener('blur', function () {
      var v = Math.min(Math.max(clean(calcInput.value), MIN), MAX);
      calcInput.value = v.toLocaleString('en-US');
      calcRange.value = v;
      render(v);
    });
    calcRange.addEventListener('input', function () {
      var v = parseInt(calcRange.value, 10);
      calcInput.value = v.toLocaleString('en-US');
      render(v);
    });
    render(clean(calcInput.value));

    // Label sizing depends on rendered width, so recompute on resize.
    if ('ResizeObserver' in window && calcChart) {
      var ro = new ResizeObserver(function () { drawChart(clean(calcInput.value)); });
      ro.observe(calcChart);
    }
  }

  /* ---- 8. Current year ------------------------------------------------ */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });
})();
