(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Header gets a shadow once the page has scrolled.
  var head = document.getElementById("head");
  function onScroll() { if (head) head.classList.toggle("scrolled", window.scrollY > 8); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Menu: slides in from the right, rows rise in turn, focus stays inside, Esc closes.
  var menu = document.getElementById("menu");
  var burger = document.getElementById("burger");
  var closeBtn = document.getElementById("menuClose");
  function openMenu() {
    menu.hidden = false;
    document.body.classList.add("locked");
    burger.setAttribute("aria-expanded", "true");
    var items = menu.querySelectorAll("[data-i]");
    for (var i = 0; i < items.length; i++) items[i].style.transitionDelay = reduced ? "0ms" : 120 + i * 45 + "ms";
    requestAnimationFrame(function () { requestAnimationFrame(function () { menu.classList.add("open"); closeBtn.focus(); }); });
  }
  function closeMenu(returnFocus) {
    menu.classList.remove("open");
    document.body.classList.remove("locked");
    burger.setAttribute("aria-expanded", "false");
    setTimeout(function () { menu.hidden = true; }, reduced ? 0 : 450);
    if (returnFocus !== false) burger.focus();
  }
  if (menu && burger) {
    burger.addEventListener("click", openMenu);
    closeBtn.addEventListener("click", function () { closeMenu(); });
    menu.addEventListener("click", function (e) {
      if (e.target === menu) closeMenu();
      if (e.target.closest("a")) closeMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (menu.hidden) return;
      if (e.key === "Escape") closeMenu();
      if (e.key === "Tab") {
        var f = menu.querySelectorAll("a[href], button");
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }

  // Sections rise into view; line icons draw; the map pin drops.
  var watched = document.querySelectorAll("[data-reveal], .draw, .map-bar");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add(en.target.classList.contains("draw") ? "is-drawn" : "in-view");
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    watched.forEach(function (el) { io.observe(el); });
  } else {
    watched.forEach(function (el) { el.classList.add("in-view", "is-drawn"); });
  }

  // Current section is underlined in the top bar on the start page.
  var navLinks = document.querySelectorAll('.mainnav a[href^="#"]');
  if (navLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    navLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var a = byId[en.target.id];
        if (a && en.isIntersecting) { navLinks.forEach(function (l) { l.classList.remove("active"); }); a.classList.add("active"); }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(byId).forEach(function (id) { var s = document.getElementById(id); if (s) spy.observe(s); });
  }

  var year = document.querySelectorAll("[data-year]");
  year.forEach(function (y) { y.textContent = new Date().getFullYear(); });

  // Quote form: checked in the browser, sent by e-mail through FormSubmit, then a clear thank-you in its place.
  var form = document.getElementById("qform");
  if (!form) return;
  var done = document.getElementById("qdone");
  var sendErr = document.getElementById("send-err");
  var f = {
    namn: document.getElementById("f-namn"),
    tel: document.getElementById("f-tel"),
    epost: document.getElementById("f-epost"),
    typ: document.getElementById("f-typ"),
    besk: document.getElementById("f-besk"),
    web: document.getElementById("f-web")
  };

  // "Begär offert" on a service page arrives with ?typ=… and the project type already chosen.
  var typ = new URLSearchParams(location.search).get("typ");
  if (typ) {
    for (var i = 0; i < f.typ.options.length; i++) if (f.typ.options[i].text === typ) f.typ.selectedIndex = i;
  }

  function setErr(key, input, show) {
    var el = document.getElementById("e-" + key);
    if (el) el.hidden = !show;
    if (input) {
      input.setAttribute("aria-invalid", show ? "true" : "false");
      if (show) input.setAttribute("aria-describedby", "e-" + key); else input.removeAttribute("aria-describedby");
    }
  }
  function shake(el) {
    if (reduced || !el || !el.animate) return;
    el.parentElement.animate([{ transform: "translateX(0)" }, { transform: "translateX(-6px)" }, { transform: "translateX(5px)" }, { transform: "translateX(-3px)" }, { transform: "translateX(0)" }], { duration: 360, easing: "ease-out" });
  }
  function validate() {
    var bad = [];
    var namnOk = f.namn.value.trim().length > 0;
    var tel = f.tel.value.trim(), ep = f.epost.value.trim();
    var epOk = !ep || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(ep);
    var contactOk = tel || ep;
    setErr("namn", f.namn, !namnOk); if (!namnOk) bad.push(f.namn);
    setErr("tel", f.tel, !contactOk); if (!contactOk) bad.push(f.tel);
    setErr("epost", f.epost, !epOk); if (!epOk) bad.push(f.epost);
    return bad;
  }
  ["input", "change"].forEach(function (ev) {
    form.addEventListener(ev, function (e) {
      if (e.target.getAttribute("aria-invalid") === "true" || e.target === f.tel || e.target === f.epost) validate();
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var bad = validate();
    if (bad.length) { bad.forEach(shake); bad[0].focus(); return; }
    var btn = form.querySelector("button[type=submit]");
    var label = btn.querySelector(".bt");
    btn.disabled = true;
    label.textContent = "Skickar …";
    sendErr.hidden = true;
    var payload = {
      _subject: "Offertförfrågan från hemsidan – " + f.namn.value.trim(),
      _template: "table",
      _captcha: "false",
      _honey: f.web.value,
      Namn: f.namn.value.trim(),
      Telefon: f.tel.value.trim() || "–",
      "E-post": f.epost.value.trim() || "–",
      "Typ av byggprojekt": f.typ.value || "–",
      Beskrivning: f.besk.value.trim() || "–"
    };
    if (f.epost.value.trim()) payload._replyto = f.epost.value.trim();
    fetch(form.getAttribute("data-endpoint"), {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return null; }).then(function (j) {
        if (!r.ok || !j || String(j.success) !== "true") throw new Error("not sent");
      });
    }).then(function () {
      form.reset();
      form.hidden = true;
      done.hidden = false;
      done.focus();
    }).catch(function () {
      // Kept as typed, so it can be sent again or read out over the phone.
      sendErr.hidden = false;
    }).then(function () {
      btn.disabled = false;
      label.textContent = "Skicka förfrågan";
    });
  });

  document.getElementById("qagain").addEventListener("click", function () {
    done.hidden = true;
    form.hidden = false;
    f.namn.focus();
  });
})();
