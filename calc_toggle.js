/* Thermo Lab 3D - scientific calculator toggle (lab / simulation page only).
   The maths runs in Python: calc_engine.py is loaded into Pyodide on first use. */
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
  let mode = 'deg', py = null, loading = null;

  function setOut(text, isErr) { out.textContent = text; out.classList.toggle('err', !!isErr); }
  const notify = msg => window.ThermoLabExtras && window.ThermoLabExtras.toast(msg);

  function loadPython() {                                   // runs once, on first open
    if (loading) return loading;
    status.textContent = 'Python: loading…';
    loading = new Promise((ok, fail) => {
      const s = document.createElement('script');
      s.src = PYODIDE + 'pyodide.js'; s.onload = ok; s.onerror = () => fail(new Error('Pyodide script blocked or offline'));
      document.head.appendChild(s);
    }).then(() => loadPyodide({ indexURL: PYODIDE }))
      .then(async p => {
        const src = await (await fetch(base + 'calc_engine.py')).text();
        p.runPython(src); py = p.globals.get('web_eval');
        status.textContent = 'Python: ready ✓';
      }).catch(err => {
        loading = null; status.textContent = 'Python: unavailable';
        setOut('Could not load Python. Check your internet connection and open the site over http(s).', true);
        notify('Calculator could not load Python'); console.error(err);
      });
    return loading;
  }

  async function evaluate() {
    const expr = inp.value.trim(); if (!expr) return;
    await loadPython(); if (!py) return;
    const r = JSON.parse(py(expr, mode));
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
