/* ============================================================
   Mallard — investor assistant
   ------------------------------------------------------------
   A click-to-expand chat launcher in the bottom right.

   WHY THIS IS NOT WIRED TO AN LLM BY DEFAULT
   This site advertises a Reg D 506(c) offering, so anything the
   widget says is a representation to a prospective investor. A
   free-form model can invent a return, imply a guarantee, or give
   tax advice in the sponsor's voice — none of which Mallard can
   stand behind, least of all with no completed deals.

   So answers come from a fixed knowledge base written from the
   site's own FAQ, strategy and terms. Every reply is short, in
   Mallard's voice, and lands on the same next step: book the call.
   Anything it cannot answer confidently is handed to Seth rather
   than guessed at.

   TO CONNECT A REAL MODEL LATER
   Set window.MALLARD_AGENT_ENDPOINT to a URL that accepts
   { message, history } and returns { reply }. The key must live on
   the server — never in this file. The knowledge base below then
   becomes the system prompt / retrieval context, and the same
   guardrails must be enforced server-side.
   ============================================================ */
(function () {
  'use strict';

  var CALL_URL = 'contact.html';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Knowledge base -------------------------------------------------
     `k` are scored keywords. `a` is the answer. `cta` is the soft close —
     varied on purpose, because the same sentence every time reads like a
     robot and stops being persuasive after the second reply. */
  var KB = [
    { id: 'what', k: ['what do you do','what is mallard','who are you','about mallard','what is this','explain'],
      a: 'Mallard Legacy Partners buys apartment communities in the Carolinas, improves how they are run, and holds them five to seven years. Investors own a share of the property itself — you receive the rent, the tax depreciation and the loan paydown without managing anything.',
      cta: 'Want the short version from Seth directly?' },

    { id: 'minimum', k: ['minimum','how much','least','smallest','entry','buy in','start with'],
      a: 'The minimum is <strong>$100,000</strong> per offering. We hold that line so the investor group stays small enough that everyone gets real attention.',
      cta: 'If that fits your range, a fifteen-minute call is the next step.' },

    { id: 'returns', k: ['return','returns','kind of return','what return','irr','multiple','profit','make','yield','roi','how much will i'],
      a: 'We underwrite to a <strong>15–17% target IRR</strong> and a <strong>1.8–2.2x equity multiple</strong> over the hold. Those are targets we underwrite toward — not guarantees, not projections, and not based on past results, because Mallard has not completed a deal yet.',
      cta: 'The calculator on the Strategy page shows what that looks like on your number. Happy to walk through the assumptions on a call.' },

    { id: 'track', k: ['track record','done this before','experience','past deals','history','how many deals','portfolio','previous'],
      a: 'Straight answer: we do not have one. Mallard has not closed an acquisition, has no assets under management and has never paid a distribution. Every figure on this site is a target or a stated commitment, never a result.',
      cta: 'What we do have is a narrow buy box, conservative structure and Seth’s own money in every deal. He would rather explain that himself — shall I point you to his calendar?' },

    { id: 'seth', k: ['seth','who runs','founder','manager','team','background','qualified','sponsor'],
      a: 'Seth Phillips, Founder and Managing Partner. He has been on job sites since he was twelve, spent four years as an industrial mechanic and two as a service engineer on anesthesia equipment, and has been around real estate for ten years — the last two focused entirely on multifamily.',
      cta: 'He takes every intro call personally. There is no sales team to get past.' },

    { id: 'markets', k: ['where','market','markets','which market','location','city','cities','area','region','state','carolina','greenville','charlotte','columbia','geography'],
      a: 'Three markets only: <strong>Greenville and Columbia, South Carolina, and Charlotte, North Carolina</strong>. We will not buy outside them — operating close to home means we can inspect properties in person and actually know the submarkets.',
      cta: 'Seth can talk through why those three, if it is useful.' },

    { id: 'hold', k: ['how long','hold','liquid','get my money','withdraw','exit','lock up','timeline','tied up'],
      a: 'Five to seven years, and you should treat it as illiquid. There is no redemption window and no secondary market. This is the real cost of private real estate — returns come from executing a business plan through a full cycle.',
      cta: 'If you might need the money sooner, say so on the call and Seth will tell you honestly not to invest.' },

    { id: 'fees', k: ['fee','how do you get paid','promote','waterfall','split','preferred','compensation','charge'],
      a: 'An acquisition fee at closing, an asset management fee on collected revenue, a disposition fee at sale, and a promote that only starts after investors get their capital back plus a preferred return. The exact terms are set per property and disclosed in full before you commit.',
      cta: 'Seth will walk you line by line through the structure — worth doing on a call.' },

    { id: 'accredited', k: ['accredited','eligible','qualify','can i invest','who can invest','506','requirements'],
      a: 'Offerings are open to accredited investors only. Most qualify on income — $200,000 individually or $300,000 jointly for the last two years — or on net worth above $1 million excluding your home. Because we use Rule 506(c), a third party verifies it; you never send financial documents to us.',
      cta: 'Not sure whether you qualify? That is a normal first-call question.' },

    { id: 'distributions', k: ['distribution','cash flow','paid','quarterly','income','when do i get','payout'],
      a: 'Distributions are paid quarterly, beginning the first full quarter after a property stabilises. Properties in heavy renovation may have a reduced or deferred first distribution — always disclosed before you commit a dollar.',
      cta: 'Seth can show you how the cash flow and sale proceeds split on a real model.' },

    { id: 'tax', k: ['tax','taxes','depreciation','k 1','k1','schedule k','cost segregation','write off','shelter','deduction'],
      a: 'You receive a Schedule K-1 reflecting your share of depreciation, including accelerated depreciation from a cost segregation study. For many investors that paper loss offsets most of the cash received in the early years. We target K-1 delivery by April 15.',
      cta: 'We are not tax advisors — take it to your CPA. Seth is happy to talk through the mechanics first.' },

    { id: 'ira', k: ['ira','401k','retirement','self directed','sdira','solo'],
      a: 'Yes — self-directed IRA and solo 401(k) capital is accepted through any major custodian. One caveat worth knowing: leveraged real estate inside an IRA can generate UBTI, which changes the maths for some investors.',
      cta: 'Worth raising with your tax advisor, and with Seth on a call.' },

    { id: 'risk', k: ['risk','lose','downside','wrong','danger','safe','guarantee','worst case'],
      a: 'You can lose money, including all of it. Real estate is leveraged, illiquid, and exposed to interest rates, insurance costs, local employment and our own judgement — and we are a first-time sponsor, which is a genuine risk you should price.',
      cta: 'We would rather you heard the honest version now than in year three. Seth will go through it properly on a call.' },

    { id: 'deal', k: ['current deal','offering','offerings','current offering','available','available now','open offering','invest today','under contract','any deals','right now'],
      a: 'No offering is open today. Seth is actively sourcing in the three target markets and is not going to buy something just to have something to sell.',
      cta: 'The people who already know us see the first deal first — an intro call is how you get on that list.' },

    { id: 'debt', k: ['debt','leverage','loan','ltv','financing','mortgage','borrow'],
      a: 'Fixed-rate debt at no more than <strong>75% of the purchase price</strong>, with a term extending beyond the planned hold, plus twelve months of operating reserves funded at closing. Both exist so we are never a forced seller.',
      cta: 'Seth can explain how that changes the risk profile.' },

    { id: 'property', k: ['kind of property','type of property','property type','units','buildings','apartment','asset','class b','vintage'],
      a: 'Existing apartment communities of 150 to 350 units, built between 1980 and 2006, occupied by working households — not new luxury product. That size supports a full-time on-site team while staying below where institutional buyers compete.',
      cta: 'The Strategy page has the full buy box. Seth can talk through a live example.' },

    { id: 'start', k: ['how do i start','next step','next steps','get started','getting started','sign up','join','process','begin','first step'],
      a: 'It starts with a fifteen-minute call — no deck, no pressure. Seth asks about your goals and tax position, you ask whatever you want, and if it is a poor fit he will say so on that call rather than three emails later.',
      cta: 'Shall I take you to the scheduling page?' },

    { id: 'contact', k: ['contact','email','phone','call','reach','speak','talk','schedule','book'],
      a: 'Easiest is to book the intro call. You can also reach Seth at <a href="mailto:sbphillips88@gmail.com">sbphillips88@gmail.com</a> or <a href="tel:+18287133597">(828) 713-3597</a>.',
      cta: 'Fifteen minutes, straight to Seth.' }
  ];

  var GREETING = 'Hi — I can answer questions about how Mallard invests, the terms, or what happens on a first call. What would you like to know?';
  var CHIPS = ['What are the target returns?', 'What is the minimum?', 'Do you have a track record?', 'How do I get started?'];

  var FALLBACK = {
    a: 'I would rather not guess at that one. Seth answers his own email and takes every intro call himself, so the fastest accurate answer is straight from him.',
    cta: 'Fifteen minutes, no obligation.'
  };

  /* ---- Matching -------------------------------------------------------
     Keyword scoring, not fuzzy inference. Longer keyword phrases score
     higher so "how much will i make" beats a bare "how much". Below the
     threshold we hand off rather than answer something approximate. */
  function normalise(s) {
    return ' ' + String(s).toLowerCase()
      .replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim() + ' ';
  }

  // Pre-normalise the keywords once. A keyword containing punctuation (k-1)
  // could otherwise never match a query that has had punctuation stripped.
  KB.forEach(function (entry) {
    entry.nk = entry.k.map(function (kw) { return normalise(kw).trim(); });
  });

  function findAnswer(text) {
    var q = normalise(text);
    var best = null, bestScore = 0;
    KB.forEach(function (entry) {
      var score = 0;
      entry.nk.forEach(function (kw) {
        if (q.indexOf(' ' + kw + ' ') !== -1) score += kw.split(' ').length * 3;
        else if (q.indexOf(kw) !== -1) score += kw.split(' ').length * 2;
      });
      if (score > bestScore) { bestScore = score; best = entry; }
    });
    return bestScore >= 2 ? best : FALLBACK;
  }

  /* ---- Build ---------------------------------------------------------- */
  function init() {
    if (document.querySelector('[data-agent]')) return;

    var root = document.createElement('div');
    root.className = 'agent';
    root.setAttribute('data-agent', '');
    root.innerHTML =
      '<button class="agent__launcher" type="button" data-agent-toggle' +
      ' aria-expanded="false" aria-controls="agentPanel"' +
      ' aria-label="Ask Mallard a question">' +
        '<span class="agent__ripple" aria-hidden="true"></span>' +
        '<span class="agent__ripple agent__ripple--2" aria-hidden="true"></span>' +
        '<img class="agent__duck" src="assets/img/mallard-mark-light.png" alt="" width="132" height="126">' +
        '<span class="agent__badge" aria-hidden="true">Ask</span>' +
      '</button>' +
      '<div class="agent__panel" id="agentPanel" data-agent-panel role="dialog"' +
      ' aria-label="Ask Mallard" aria-modal="false" hidden>' +
        '<header class="agent__head">' +
          '<img src="assets/img/mallard-mark-light.png" alt="" width="132" height="126">' +
          '<div class="agent__headText"><b>Ask Mallard</b><span>Answers in seconds</span></div>' +
          '<button class="agent__close" type="button" data-agent-close aria-label="Close chat">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"' +
            ' stroke-width="1.6" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>' +
          '</button>' +
        '</header>' +
        '<div class="agent__log" data-agent-log role="log" aria-live="polite" aria-atomic="false"></div>' +
        '<div class="agent__chips" data-agent-chips></div>' +
        '<form class="agent__form" data-agent-form>' +
          '<label class="sr-only" for="agentInput">Type your question</label>' +
          '<input id="agentInput" type="text" autocomplete="off" placeholder="Ask a question…" data-agent-input>' +
          '<button type="submit" aria-label="Send">' +
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor"' +
            ' stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M4 12h15M13 6l6 6-6 6"/></svg>' +
          '</button>' +
        '</form>' +
        '<a class="agent__cta" href="' + CALL_URL + '">Schedule a 15-minute call</a>' +
        '<p class="agent__legal">General information only — not investment, tax or legal advice, ' +
        'and not an offer to sell securities.</p>' +
      '</div>';
    document.body.appendChild(root);

    var toggle = root.querySelector('[data-agent-toggle]');
    var panel = root.querySelector('[data-agent-panel]');
    var log = root.querySelector('[data-agent-log]');
    var chips = root.querySelector('[data-agent-chips]');
    var form = root.querySelector('[data-agent-form]');
    var input = root.querySelector('[data-agent-input]');
    var seeded = false;

    function bubble(who, html) {
      var row = document.createElement('div');
      row.className = 'agent__msg agent__msg--' + who;
      row.innerHTML = '<div class="agent__bubble">' + html + '</div>';
      log.appendChild(row);
      log.scrollTop = log.scrollHeight;
      return row;
    }

    function typing() {
      var row = document.createElement('div');
      row.className = 'agent__msg agent__msg--bot agent__msg--typing';
      row.innerHTML = '<div class="agent__bubble"><i></i><i></i><i></i></div>';
      log.appendChild(row);
      log.scrollTop = log.scrollHeight;
      return row;
    }

    function renderChips(list) {
      chips.innerHTML = '';
      list.forEach(function (text) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'agent__chip';
        b.textContent = text;
        b.addEventListener('click', function () { send(text); });
        chips.appendChild(b);
      });
    }

    function answer(text) {
      var hit = findAnswer(text);
      var wait = reduce ? 120 : 480;
      var t = typing();
      window.setTimeout(function () {
        t.remove();
        // Answer first, then the nudge as its own line — a soft sell reads
        // as pushy when it is welded onto the end of the sentence.
        bubble('bot', hit.a);
        window.setTimeout(function () {
          bubble('bot', '<span class="agent__nudge">' + hit.cta + '</span>' +
            '<a class="agent__inlineCta" href="' + CALL_URL + '">Book the call →</a>');
        }, reduce ? 60 : 320);
      }, wait);
    }

    function send(text) {
      text = String(text).trim();
      if (!text) return;
      bubble('you', text.replace(/[<>&]/g, function (ch) {
        return { '<': '&lt;', '>': '&gt;', '&': '&amp;' }[ch];
      }));
      input.value = '';
      chips.innerHTML = '';
      answer(text);
    }

    function open() {
      panel.hidden = false;
      // next frame so the transition has a start value to animate from
      window.requestAnimationFrame(function () { root.classList.add('is-open'); });
      toggle.setAttribute('aria-expanded', 'true');
      if (!seeded) {
        seeded = true;
        bubble('bot', GREETING);
        renderChips(CHIPS);
      }
      window.setTimeout(function () { input.focus({ preventScroll: true }); }, reduce ? 0 : 260);
    }

    function close() {
      root.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      window.setTimeout(function () { panel.hidden = true; }, reduce ? 0 : 240);
      toggle.focus({ preventScroll: true });
    }

    toggle.addEventListener('click', function () {
      if (toggle.getAttribute('aria-expanded') === 'true') close(); else open();
    });
    root.querySelector('[data-agent-close]').addEventListener('click', close);
    form.addEventListener('submit', function (e) { e.preventDefault(); send(input.value); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') close();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
