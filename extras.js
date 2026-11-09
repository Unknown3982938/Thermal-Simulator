(() => {
  const STORE = 'thermolab3d_progress_v1';
  const read = () => { try { return JSON.parse(localStorage.getItem(STORE)) || {}; } catch (_) { return {}; } };
  const write = data => { try { localStorage.setItem(STORE, JSON.stringify(data)); } catch (_) {} };
  const data = read();
  data.visited = Array.isArray(data.visited) ? data.visited : [];
  data.modes = Array.isArray(data.modes) ? data.modes : [];
  data.unlocked = Array.isArray(data.unlocked) ? data.unlocked : [];
  data.journalCount = Number(data.journalCount || 0);
  const save = () => write(data);
  const unlock = id => {
    if (data.unlocked.includes(id)) return false;
    data.unlocked.push(id); save();
    toast('Achievement unlocked: ' + (ACHIEVEMENTS.find(a => a.id === id)?.name || id));
    return true;
  };
  const ACHIEVEMENTS = [
    {id:'welcome',name:'First Arrival',desc:'Visited the laboratory for the first time.',icon:'🚪'},
    {id:'gas',name:'Gas Explorer',desc:'Opened the Gas Laws simulation.',icon:'🎈'},
    {id:'heat',name:'Heat Seeker',desc:'Opened the Phase Change simulation.',icon:'🔥'},
    {id:'law',name:'Energy Accountant',desc:'Opened the First Law simulation.',icon:'⚡'},
    {id:'all-modes',name:'Full Circuit',desc:'Explored all three simulation modes.',icon:'🧭'},
    {id:'journal',name:'Lab Notebook',desc:'Saved your first journal entry.',icon:'📓'},
    {id:'secret',name:'Curiosity Rewarded',desc:'Found the hidden laboratory Easter egg.',icon:'🗝️'}
  ];
  function toast(message) {
    let el=document.getElementById('thermo-toast');
    if(!el){el=document.createElement('div');el.id='thermo-toast';document.body.appendChild(el);}
    el.textContent=message;el.classList.add('show');clearTimeout(el._hideTimer);
    el._hideTimer=setTimeout(()=>el.classList.remove('show'),2600);
  }
  function recordVisit(){
    const page=location.pathname.split('/').pop()||'index.html';
    if(!data.visited.includes(page)) data.visited.push(page);
    if(data.visited.length>=1) unlock('welcome');
    const mode=new URLSearchParams(location.search).get('mode');
    if(page==='index.html' && ['gas','heat','law'].includes(mode||'gas')){
      const m=mode||'gas'; if(!data.modes.includes(m)) data.modes.push(m);
      unlock(m);
      if(['gas','heat','law'].every(x=>data.modes.includes(x))) unlock('all-modes');
    }
    save();
  }
  function showSecret(){
    let overlay=document.getElementById('thermo-secret');
    if(!overlay){
      overlay=document.createElement('div');overlay.id='thermo-secret';
      overlay.innerHTML='<div class="secret-card"><div class="secret-mark">🧪</div><div style="letter-spacing:3px;font-size:10px;color:#62d4ff;font-weight:800">CLASSIFIED LAB NOTE</div><h2>You found the hidden chamber.</h2><p>Curiosity is a scientist’s most useful instrument. Keep experimenting, question the results, and never trust a suspiciously convenient beaker.</p><div style="font-size:12px;color:#8ea7c8">THERMO LAB 3D · ACCESS GRANTED</div><button type="button" id="secret-close">Back to the lab</button></div>';
      document.body.appendChild(overlay);
      overlay.addEventListener('click',e=>{if(e.target===overlay)overlay.classList.remove('show')});
      overlay.querySelector('#secret-close').addEventListener('click',()=>overlay.classList.remove('show'));
    }
    overlay.classList.add('show');unlock('secret');
  }
  recordVisit();
  // Type THERMO anywhere on the page (not while entering form data) to reveal the secret.
  let typed='';
  document.addEventListener('keydown',e=>{
    if(e.ctrlKey||e.altKey||e.metaKey||/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)||e.target.isContentEditable)return;
    typed=(typed+e.key.toLowerCase()).slice(-6);
    if(typed==='thermo'){typed='';showSecret();}
  });
  // Small clickable logo easter egg: tap/click a recognizable brand mark seven times.
  let taps=0,tapTimer;
  document.querySelectorAll('.site-nav-logo,.nav-brand-icon,.hero-art,.site-nav-title').forEach(el=>{
    el.style.cursor='pointer';el.addEventListener('click',()=>{
      taps++;clearTimeout(tapTimer);tapTimer=setTimeout(()=>taps=0,1800);
      if(taps>=7){taps=0;showSecret();}
    });
  });
  window.ThermoLabExtras={
    toast,
    recordMode(mode){if(!['gas','heat','law'].includes(mode))return;if(!data.modes.includes(mode))data.modes.push(mode);unlock(mode);if(['gas','heat','law'].every(x=>data.modes.includes(x)))unlock('all-modes');save();},
    recordJournal(){data.journalCount++;save();unlock('journal');},
    getProgress(){return {...data,unlocked:[...data.unlocked],visited:[...data.visited],modes:[...data.modes]};},
    achievements:ACHIEVEMENTS
  };
})();
