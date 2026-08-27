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
      a: 'We buy apartment communities in the Carolinas, run them better, and hold five to seven years. You own a share of the building itself \u2014 rent, depreciation and loan paydown all flow to you. None of the management does.',
      cta: 'Seth can give you the two-minute version.' },

    { id: 'minimum', k: ['minimum','how much','least','smallest','entry','buy in','start with'],
      a: '<strong>$100,000</strong> per offering. We keep it there deliberately \u2014 a smaller investor group means you get Seth on the phone, not an associate.',
      cta: 'Does that sit in your range?' },

    { id: 'returns', k: ['return','returns','kind of return','what return','irr','multiple','profit','make','yield','roi','how much will i'],
      a: 'We underwrite to a <strong>15\u201317% IRR</strong> and <strong>1.8\u20132.2x</strong> over the hold.<br><br>Worth being precise: those are thresholds a deal has to clear before we bring it to you. Not guarantees, and not past performance \u2014 we have not closed a deal yet.',
      cta: 'The Strategy page runs those against your number. Seth will happily pull the assumptions apart with you.' },

    { id: 'track', k: ['track record','done this before','experience','past deals','history','how many deals','portfolio','previous'],
      a: 'None. No acquisitions closed, nothing under management, no distributions paid.<br><br>You would be underwriting the operator and the discipline, not a results page. If that sits outside your risk tolerance, this is a reasonable place to stop.',
      cta: 'If it does not, the conversation is worth fifteen minutes.' },

    { id: 'seth', k: ['seth','who runs','founder','manager','team','background','qualified','sponsor'],
      a: 'Seth Phillips runs it. On job sites from twelve, four years an industrial mechanic, two as a service engineer on anesthesia equipment, ten years around real estate and the last two in multifamily full time.<br><br>He reads buildings as systems rather than spreadsheets \u2014 a different instinct from a finance background, and a useful one when you are the person who has to spot what breaks.',
      cta: 'He takes every intro call himself.' },

    { id: 'markets', k: ['where','market','markets','which market','location','city','cities','area','region','state','carolina','greenville','charlotte','columbia','geography'],
      a: '<strong>Greenville and Columbia, South Carolina, and Charlotte, North Carolina.</strong> Nowhere else.<br><br>Close enough to walk every property before we bid, and to know which submarkets are actually adding jobs.',
      cta: 'Happy to talk through why those three.' },

    { id: 'hold', k: ['how long','hold','liquid','get my money','withdraw','exit','lock up','timeline','tied up'],
      a: 'Five to seven years, and genuinely illiquid \u2014 no redemption window, no secondary market.<br><br>That is the trade. The return comes from executing a business plan through a full cycle, which you cannot do with capital that might be recalled.',
      cta: 'If there is any chance you need it sooner, say so early and Seth will tell you straight.' },

    { id: 'fees', k: ['fee','how do you get paid','promote','waterfall','split','preferred','compensation','charge'],
      a: 'An acquisition fee at close, an asset management fee on collected revenue, a disposition fee at sale, and a promote that only starts once you have your capital back plus a preferred return.<br><br>Exact terms are set per property and disclosed in full before you commit a dollar.',
      cta: 'Seth will walk the waterfall with you line by line.' },

    { id: 'accredited', k: ['accredited','eligible','qualify','can i invest','who can invest','506','requirements'],
      a: 'Accredited investors only \u2014 income of $200K individually or $300K jointly for the past two years, or net worth above $1M excluding your home.<br><br>We run under Rule 506(c), so a third party verifies it. Your financials never come to us.',
      cta: 'If you are unsure which test you meet, that is a normal first-call question.' },

    { id: 'distributions', k: ['distribution','cash flow','paid','quarterly','income','when do i get','payout'],
      a: 'Quarterly, starting the first full quarter after a property stabilises.<br><br>Anything in heavy renovation may run a reduced or deferred first distribution \u2014 disclosed up front, never a surprise.',
      cta: 'Seth can show you how cash and sale proceeds split on a real model.' },

    { id: 'tax', k: ['tax','taxes','depreciation','k 1','k1','schedule k','cost segregation','write off','shelter','deduction'],
      a: 'You get a K-1 carrying your share of depreciation, accelerated through a cost segregation study.<br><br>For most investors the paper loss offsets the majority of cash received in the early years. We target K-1 delivery by April 15.',
      cta: 'Your CPA should confirm the specifics \u2014 we are not tax advisors. Seth can cover the mechanics first.' },

    { id: 'ira', k: ['ira','401k','retirement','self directed','sdira','solo'],
      a: 'Yes \u2014 self-directed IRA or solo 401(k), through any major custodian.<br><br>One thing to know: leveraged real estate inside an IRA can generate UBTI, which changes the arithmetic. Worth a word with your tax advisor about which pocket to use.',
      cta: 'Seth can flag what to ask them.' },

    { id: 'risk', k: ['risk','lose','downside','wrong','danger','safe','guarantee','worst case'],
      a: 'You can lose the entire investment. It is leveraged, illiquid, and exposed to rates, insurance, local employment and our judgement \u2014 and we are a first-time sponsor, which is a real risk to price rather than wave through.<br><br>What we control: conservative debt, twelve months of reserves at closing, markets we know, and Seth\u2019s own capital in every deal.',
      cta: 'Better you hear the honest version now than in year three.' },

    { id: 'deal', k: ['current deal','offering','offerings','current offering','available','available now','open offering','invest today','under contract','any deals','right now'],
      a: 'Nothing open today. Seth is sourcing in the three target markets and will not buy something simply to have something to raise on.<br><br>The people who already know us see the first deal first.',
      cta: 'An intro call is how you get on that list.' },

    { id: 'debt', k: ['debt','leverage','loan','ltv','financing','mortgage','borrow'],
      a: 'Fixed-rate, no more than <strong>75% LTV</strong>, with a term that outlasts the business plan, plus twelve months of operating reserves funded at closing.<br><br>Both exist so we are never a forced seller in a bad window.',
      cta: 'Seth can explain what that does to the downside.' },

    { id: 'property', k: ['kind of property','type of property','property type','units','buildings','apartment','asset','class b','vintage'],
      a: '150 to 350 units, built 1980 to 2006, occupied by working households \u2014 not new luxury product.<br><br>Large enough to carry a full-time on-site team, small enough that institutional buyers are not bidding against us.',
      cta: 'The Strategy page has the full buy box if you want the detail.' },

    { id: 'start', k: ['how do i start','next step','next steps','get started','getting started','sign up','join','process','begin','first step'],
      a: 'A fifteen-minute call. No deck, no pressure.<br><br>Seth asks what you are solving for and where you sit on tax; you ask whatever you want. If it is a poor fit he will say so on that call rather than three emails later.',
      cta: 'Shall I point you at the scheduling page?' },

    { id: 'contact', k: ['contact','email','call','reach','speak','talk','schedule','book'],
      a: 'The intro call is the fastest route. Otherwise Seth reads his own email: <a href="mailto:seth.phillips@mallardlegacypartners.com">seth.phillips@mallardlegacypartners.com</a>.',
      cta: 'Fifteen minutes, straight to him.' }
  ];

  var GREETING = 'Happy to answer anything \u2014 how we invest, the terms, the risks, or what a first call actually looks like. What would be useful?';
  var CHIPS = ['What returns do you target?', 'What is the minimum?', 'What is your track record?', 'What are the risks?'];

  var FALLBACK = {
    a: 'I would rather give you nothing than something approximate on that one. Seth takes every call himself, so the accurate answer is a short conversation away.',
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
