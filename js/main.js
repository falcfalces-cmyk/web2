/* Grupo Belcom: carcasa (barra lateral, tema, buscador Ctrl K) y selector de tarifas. Sin dependencias. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) { /* sin almacenamiento */ } }
  };
  var app = $('#app');
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var norm = function (s) { return String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); };
  var typing = function (e) { var t = e.target; return t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable); };

  var year = $('#year');
  if (year) year.textContent = new Date().getFullYear();

  /* ---------- tema: sistema, claro u oscuro ---------- */
  function setTema(modo) {
    if (modo === 'light' || modo === 'dark') {
      document.documentElement.setAttribute('data-theme', modo);
      store.set('belcom-tema', modo);
    } else {
      document.documentElement.removeAttribute('data-theme');
      store.del('belcom-tema');
    }
    marcarTema();
  }
  function marcarTema() {
    var actual = store.get('belcom-tema') || 'system';
    $$('[data-tema]').forEach(function (b) { b.classList.toggle('on', b.dataset.tema === actual); b.setAttribute('aria-pressed', String(b.dataset.tema === actual)); });
  }
  $$('[data-tema]').forEach(function (b) { b.addEventListener('click', function () { setTema(b.dataset.tema); }); });
  marcarTema();

  /* ---------- barra lateral: plegar (escritorio) y cajón (móvil) ---------- */
  var movil = function () { return window.matchMedia('(max-width: 860px)').matches; };
  function plegar(forzar) {
    if (!app || movil()) return;
    var on = typeof forzar === 'boolean' ? forzar : !app.classList.contains('collapsed');
    app.classList.toggle('collapsed', on);
    store.set('belcom-sb', on ? '1' : '0');
  }
  function cajon(abrir) {
    if (!app) return;
    app.classList.toggle('nav-open', abrir);
    var b = $('#nav-burger');
    if (b) b.setAttribute('aria-expanded', String(abrir));
  }
  var fold = $('#sb-fold');
  if (fold) fold.addEventListener('click', function () { plegar(); });
  var burger = $('#nav-burger');
  if (burger) burger.addEventListener('click', function () { cajon(!app.classList.contains('nav-open')); });
  var cerrar = $('#sb-close');
  if (cerrar) cerrar.addEventListener('click', function () { cajon(false); });
  var scrim = $('#nav-scrim');
  if (scrim) scrim.addEventListener('click', function () { cajon(false); });
  $$('.sb a.sb-item').forEach(function (a) { a.addEventListener('click', function () { cajon(false); }); });

  /* ---------- tooltip global: cualquier elemento con data-tip ---------- */
  var tip = $('#tip');
  if (tip) {
    var tipDe = function (el) { return el && el.closest ? el.closest('[data-tip]') : null; };
    var mostrar = function (el) {
      var txt = el.getAttribute('data-tip');
      if (!txt) return;
      var enBarra = !!el.closest('.sb');
      var plegada = app.classList.contains('collapsed');
      /* con la barra desplegada el texto de sus elementos ya se ve */
      if (enBarra && !plegada && (el.classList.contains('sb-item') || el.classList.contains('sb-new') || el.classList.contains('sb-search'))) return;
      tip.textContent = txt;
      var r = el.getBoundingClientRect();
      var w = tip.offsetWidth, h = tip.offsetHeight;
      var x, y;
      if (enBarra && plegada) { x = r.right + 8; y = r.top + r.height / 2 - h / 2; }
      else {
        x = r.left + r.width / 2 - w / 2; y = r.bottom + 8;
        if (y + h > window.innerHeight - 8) y = r.top - h - 8;
      }
      tip.style.left = Math.max(8, Math.min(x, window.innerWidth - w - 8)) + 'px';
      tip.style.top = Math.max(8, y) + 'px';
      tip.classList.add('show');
    };
    document.addEventListener('mouseover', function (e) { var el = tipDe(e.target); if (el) mostrar(el); });
    document.addEventListener('mouseout', function (e) { if (tipDe(e.target)) tip.classList.remove('show'); });
    document.addEventListener('focusin', function (e) { var el = tipDe(e.target); if (el) mostrar(el); });
    document.addEventListener('focusout', function () { tip.classList.remove('show'); });
    document.addEventListener('click', function () { tip.classList.remove('show'); });
  }

  /* ---------- selector de tarifas (Fibra / Móvil / Fijo) ---------- */
  var ptabs = $$('[data-ptab]');
  var ppanels = $$('.ptab-panel');
  if (ptabs.length) {
    var showP = function (id) {
      ptabs.forEach(function (t) { var on = t.dataset.ptab === id; t.classList.toggle('on', on); t.setAttribute('aria-pressed', String(on)); });
      ppanels.forEach(function (p) { p.hidden = p.id !== 'ptab-' + id; });
    };
    ptabs.forEach(function (t) {
      t.addEventListener('click', function () { showP(t.dataset.ptab); history.replaceState(null, '', '#' + t.dataset.ptab); });
    });
    var desdeHash = function () { var h = location.hash.replace('#', ''); showP(['fibra', 'movil', 'fijo'].indexOf(h) >= 0 ? h : ptabs[0].dataset.ptab); };
    window.addEventListener('hashchange', desdeHash);
    desdeHash();
  }

  /* ---------- buscador Ctrl K ---------- */
  var cmdk = null;
  function abrirBuscador() {
    if (cmdk) return;
    var datos = window.BELCOM_INDICE || [];
    var iconos = window.BELCOM_ICONOS || {};
    var wrap = document.createElement('div');
    wrap.className = 'cmdk-wrap';
    wrap.innerHTML = '<div class="overlay"></div><div class="cmdk" role="dialog" aria-modal="true" aria-label="Buscar en la web">' +
      '<div class="cmdk-in">' + (iconos.search || '') + '<input type="text" placeholder="Buscar servicios, tarifas, delegaciones…" aria-label="Buscar" autocomplete="off" spellcheck="false"></div>' +
      '<div class="cmdk-list" role="listbox"></div>' +
      '<div class="cmdk-f"><span><kbd>↑</kbd><kbd>↓</kbd> moverte</span><span><kbd>↵</kbd> abrir</span><span><kbd>Esc</kbd> cerrar</span></div></div>';
    document.body.appendChild(wrap);
    var input = $('input', wrap), lista = $('.cmdk-list', wrap);
    var visibles = [], sel = 0;

    function resaltar(txt, palabras) {
      var n = norm(txt), marcas = [];
      palabras.forEach(function (p) { var i = n.indexOf(p); if (i >= 0) marcas.push([i, i + p.length]); });
      if (!marcas.length) return esc(txt);
      marcas.sort(function (a, b) { return a[0] - b[0]; });
      var out = '', pos = 0;
      marcas.forEach(function (m) {
        if (m[0] < pos) return;
        out += esc(txt.slice(pos, m[0])) + '<mark>' + esc(txt.slice(m[0], m[1])) + '</mark>';
        pos = m[1];
      });
      return out + esc(txt.slice(pos));
    }
    function pintar() {
      var palabras = norm(input.value).split(/\s+/).filter(Boolean);
      var hallados = datos.filter(function (d) {
        var h = norm(d.l + ' ' + d.s + ' ' + d.g);
        return palabras.every(function (p) { return h.indexOf(p) >= 0; });
      });
      if (!palabras.length) {   /* sin búsqueda, pocos por grupo */
        var cuenta = {};
        hallados = hallados.filter(function (d) { cuenta[d.g] = (cuenta[d.g] || 0) + 1; return cuenta[d.g] <= (d.g === 'Servicios' ? 4 : 7); });
      }
      visibles = hallados;
      sel = Math.min(sel, Math.max(0, visibles.length - 1));
      if (!visibles.length) { lista.innerHTML = '<div class="cmdk-empty">Nada coincide con «' + esc(input.value) + '». Prueba con «fibra» o «alarmas».</div>'; return; }
      var html = '', grupo = '';
      visibles.forEach(function (d, i) {
        if (d.g !== grupo) { grupo = d.g; html += '<div class="cmdk-g">' + esc(grupo) + '</div>'; }
        html += '<div class="cmdk-it' + (i === sel ? ' on' : '') + '" role="option" data-i="' + i + '"><span class="ic">' + (iconos[d.i] || '') + '</span>' +
          '<span class="l">' + resaltar(d.l, palabras) + '</span><span class="s">' + esc(d.s) + '</span></div>';
      });
      lista.innerHTML = html;
    }
    function ir(i) {
      var d = visibles[i];
      if (!d) return;
      cerrarBuscador();
      var actual = location.pathname.split('/').pop() || 'index.html';
      var partes = d.h.split('#');
      if (partes.length > 1 && d.h.indexOf(':') < 0 && partes[0] === actual) { location.hash = partes[1]; } else { location.href = d.h; }
    }
    function mover(n) {
      if (!visibles.length) return;
      sel = (sel + n + visibles.length) % visibles.length;
      $$('.cmdk-it', lista).forEach(function (el) { el.classList.toggle('on', Number(el.dataset.i) === sel); });
      var on = $('.cmdk-it.on', lista);
      if (on) on.scrollIntoView({ block: 'nearest' });
    }
    input.addEventListener('input', function () { sel = 0; pintar(); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { e.preventDefault(); mover(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); mover(-1); }
      else if (e.key === 'Enter') { e.preventDefault(); ir(sel); }
    });
    lista.addEventListener('click', function (e) { var it = e.target.closest('.cmdk-it'); if (it) ir(Number(it.dataset.i)); });
    lista.addEventListener('mousemove', function (e) {
      var it = e.target.closest('.cmdk-it');
      if (it && Number(it.dataset.i) !== sel) { sel = Number(it.dataset.i); $$('.cmdk-it', lista).forEach(function (el) { el.classList.toggle('on', el === it); }); }
    });
    $('.overlay', wrap).addEventListener('click', cerrarBuscador);
    cmdk = wrap;
    pintar();
    input.focus();
  }
  function cerrarBuscador() { if (cmdk) { cmdk.remove(); cmdk = null; } }
  $$('[data-cmdk]').forEach(function (b) { b.addEventListener('click', function () { cajon(false); abrirBuscador(); }); });

  /* ---------- atajos: Ctrl K buscar, Ctrl ← plegar la barra, Esc cierra ---------- */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (cmdk) { e.preventDefault(); cerrarBuscador(); } else if (app && app.classList.contains('nav-open')) cajon(false);
      return;
    }
    if ((e.ctrlKey || e.metaKey) && !e.altKey && e.key.toLowerCase() === 'k') { e.preventDefault(); if (cmdk) cerrarBuscador(); else abrirBuscador(); return; }
    /* Ctrl ← pliega la barra; dentro de un campo sigue moviendo el cursor */
    if (e.ctrlKey && !e.altKey && !e.shiftKey && e.key === 'ArrowLeft' && !typing(e)) { e.preventDefault(); plegar(); }
  }, true);

  /* al pasar a escritorio se cierra el cajón */
  window.addEventListener('resize', function () { if (!movil()) cajon(false); });
})();
