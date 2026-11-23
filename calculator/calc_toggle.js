/* Thermo Lab 3D - scientific calculator toggle (lab / simulation page only).
   The maths runs in Python: calc_engine.py is loaded into Pyodide (in a Web Worker) on first use. */
(() => {
  'use strict';
  const page = location.pathname.split('/').pop() || 'index.html';
  if (page !== 'index.html' || document.getElementById('calc-toggle')) return;   // lab page only

  const base = document.currentScript ? document.currentScript.src.replace(/[^/]*$/, '') : 'calculator/';
  const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';
  const css = document.createElement('link');
  css.rel = 'stylesheet'; css.href = base + 'calc_toggle.css'; document.head.appendChild(css);

  const KEYS = [
    ['Deg','mode','fn'],['sin','sin(','fn'],['cos','cos(','fn'],['tan','tan(','fn'],['AC','ac','op'],
    ['sin⁻¹','asin(','fn'],['cos⁻¹','acos(','fn'],['tan⁻¹','atan(','fn'],['(','(','fn'],[')',')','fn'],
    ['ln','ln(','fn'],['log','log(','fn'],['√','sqrt(','fn'],['x²','^2','fn'],['xʸ','^','fn'],
    ['π','pi','fn'],['e','e','fn'],['n!','!','fn'],['1/x','1/(','fn'],['⌫','del','op'],
    ['7','7'],['8','8'],['9','9'],['÷','/','op'],['Ans','ans','fn'],
    ['4','4'],['5','5'],['6','6'],['×','*','op'],['EXP','*10^(','fn'],
    ['1','1'],['2','2'],['3','3'],['−','-','op'],['abs','abs(','fn'],
    ['0','0'],['.','.'],['±','neg','fn'],['+','+','op'],['=','eq','eq']
  ];

  const toggle = document.createElement('button');
  toggle.id = 'calc-toggle'; toggle.type = 'button'; toggle.textContent = '🧮';
  toggle.setAttribute('aria-label', 'Toggle scientific calculator');
  toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-controls', 'calc-panel');

  const panel = document.createElement('div');
  panel.id = 'calc-panel'; panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-label', 'Scientific calculator');
  panel.innerHTML = `<div class="calc-head"><b>Scientific Calculator</b><span id="calc-status">Python: not loaded</span></div>
    <input id="calc-in" type="text" inputmode="none" autocomplete="off" spellcheck="false" placeholder="e.g. sin(30)+2^3">
    <div id="calc-out">0</div><div id="calc-hist"></div><div class="calc-grid"></div>`;
  document.body.append(toggle, panel);

  const $ = s => panel.querySelector(s);
  const inp = $('#calc-in'), out = $('#calc-out'), hist = $('#calc-hist'), status = $('#calc-status');
  let mode = 'deg', worker = null, ready = false, loading = null, nextId = 1;
  const pending = new Map();

  function setOut(text, isErr) { out.textContent = text; out.classList.toggle('err', !!isErr); }
  const notify = msg => window.ThermoLabExtras && window.ThermoLabExtras.toast(msg);

  /* Pyodide runs inside a Web Worker. Starting it on the main thread froze the whole
     page (animation, sliders, scrolling) for several seconds while WebAssembly compiled. */
  const WORKER_SRC = `
let evalFn = null;
self.onmessage = async (e) => {
  const m = e.data;
  if (m.type === 'init') {
    try {
      importScripts(m.pyodide + 'pyodide.js');
      const p = await loadPyodide({ indexURL: m.pyodide });
      p.runPython(await (await fetch(m.engine)).text());
      evalFn = p.globals.get('web_eval');
      self.postMessage({ type: 'ready' });
    } catch (err) { self.postMessage({ type: 'error', message: String((err && err.message) || err) }); }
  } else if (m.type === 'eval') {
    let data;
    try { data = evalFn(m.expr, m.mode); }
    catch (err) { data = JSON.stringify({ ok: false, text: 'Python error' }); }
    self.postMessage({ type: 'result', id: m.id, data: data });
  }
};`;

  function loadPython() {                                   // runs once, on first open
    if (loading) return loading;
    const t0 = Date.now();
    status.textContent = 'Python: loading…';
    const tick = setInterval(() => { status.textContent = 'Python: loading… ' + Math.round((Date.now() - t0) / 1000) + ' s'; }, 1000);
    loading = new Promise((ok, fail) => {
      try { worker = new Worker(URL.createObjectURL(new Blob([WORKER_SRC], { type: 'text/javascript' }))); }
      catch (err) { fail(err); return; }
      worker.onmessage = e => {
        const m = e.data;
        if (m.type === 'ready') ok();
        else if (m.type === 'error') fail(new Error(m.message));
        else if (m.type === 'result' && pending.has(m.id)) { pending.get(m.id)(m.data); pending.delete(m.id); }
      };
      worker.onerror = err => fail(new Error(err.message || 'Worker failed'));
      worker.postMessage({ type: 'init', pyodide: PYODIDE, engine: base + 'calc_engine.py' });
    }).then(() => {
      clearInterval(tick); ready = true; status.textContent = 'Python: ready ✓';
    }).catch(err => {
      clearInterval(tick); loading = null; ready = false;
      if (worker) { worker.terminate(); worker = null; }
      status.textContent = 'Python: unavailable';
      setOut('Could not load Python. Check your internet connection and open the site over http(s).', true);
      notify('Calculator could not load Python'); console.error(err);
    });
    return loading;
  }

  function runPython(expr) {
    return new Promise((resolve, reject) => {
      const id = nextId++;
      const timer = setTimeout(() => { pending.delete(id); reject(new Error('timeout')); }, 15000);
      pending.set(id, data => { clearTimeout(timer); resolve(JSON.parse(data)); });
      worker.postMessage({ type: 'eval', id: id, expr: expr, mode: mode });
    });
  }

  async function evaluate() {
    const expr = inp.value.trim(); if (!expr) return;
    if (!ready) { setOut('Waiting for Python to finish loading…'); await loadPython(); if (!ready) return; }
    let r;
    try { r = await runPython(expr); } catch (err) { setOut('Python did not answer. Please try again.', true); return; }
    setOut(r.text, !r.ok);
    if (r.ok) {
      const row = document.createElement('div'); row.textContent = `${expr} = ${r.text}`;
      row.onclick = () => { inp.value = expr; inp.focus(); };
      hist.prepend(row); while (hist.children.length > 6) hist.lastChild.remove();
    }
  }

  function insert(text) {
    const s = inp.selectionStart ?? inp.value.length, e = inp.selectionEnd ?? s;
    inp.value = inp.value.slice(0, s) + text + inp.value.slice(e);
    inp.setSelectionRange(s + text.length, s + text.length); inp.focus();
  }

  function press(action, btn) {
    if (action === 'ac') { inp.value = ''; setOut('0'); }
    else if (action === 'del') {
      const s = inp.selectionStart, e = inp.selectionEnd;
      if (s !== e) { inp.value = inp.value.slice(0, s) + inp.value.slice(e); inp.setSelectionRange(s, s); }
      else if (s > 0) { inp.value = inp.value.slice(0, s - 1) + inp.value.slice(s); inp.setSelectionRange(s - 1, s - 1); }
    }
    else if (action === 'mode') { mode = mode === 'deg' ? 'rad' : 'deg'; btn.textContent = mode === 'deg' ? 'Deg' : 'Rad'; }
    else if (action === 'neg') { const v = inp.value; inp.value = /^-\(.*\)$/.test(v) ? v.slice(2, -1) : '-(' + v + ')'; }
    else if (action === 'eq') evaluate();
    else insert(action);
  }

  const grid = $('.calc-grid');
  KEYS.forEach(([label, action, kind]) => {
    const b = document.createElement('button');
    b.type = 'button'; b.textContent = label; if (kind) b.className = kind;
    b.onclick = () => press(action, b); grid.appendChild(b);
  });
  inp.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); evaluate(); } if (e.key !== 'Escape') e.stopPropagation(); });

  function setOpen(open) {
    panel.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    if (open) { loadPython(); if (matchMedia('(hover:hover)').matches) inp.focus(); }
  }
  toggle.onclick = () => setOpen(!panel.classList.contains('open'));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
})();
