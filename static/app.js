(() => {
  const $ = (id) => document.getElementById(id);
  const sessionKey = 'okfbench_session_id';
  const themeKey = 'okfbench_theme';
  let sessionId = localStorage.getItem(sessionKey) || '';
  const messagesEl = $('messages');
  const form = $('chat-form');
  const input = $('question');
  const modeEl = $('mode');
  const statusEl = $('status');
  const metricsEl = $('metrics');
  const sourcesEl = $('sources');
  const runsEl = $('runs');
  const sampleEl = $('sample-questions');
  const modeSelect = document.querySelector('.mode-select');
  const modeToggle = $('mode-toggle');
  const modeMenu = $('mode-menu');
  const modeValue = $('mode-value');
  const modeOptions = Array.from(document.querySelectorAll('[data-mode-option]'));
  const app = $('app');

  function setStatus(text, kind = '') {
    statusEl.textContent = text;
    statusEl.className = 'status-line' + (kind === 'err' ? ' err' : '');
  }

  function addBubble(role, text, meta) {
    const wrap = document.createElement('div');
    wrap.className = 'msg-row ' + (role === 'user' ? 'user' : 'assistant');
    const bubble = document.createElement('div');
    bubble.className = 'bubble ' + (role === 'user' ? 'bubble-user' : 'bubble-assistant');
    bubble.textContent = text;
    wrap.appendChild(bubble);
    if (meta) {
      const m = document.createElement('div');
      m.className = 'msg-meta' + (role === 'user' ? ' right' : '');
      m.textContent = meta;
      wrap.appendChild(m);
    }
    messagesEl.appendChild(wrap);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  async function addTypingBubble(text, meta) {
    const wrap = document.createElement('div');
    wrap.className = 'msg-row assistant';
    const bubble = document.createElement('div');
    bubble.className = 'bubble bubble-assistant';
    bubble.setAttribute('aria-label', 'Assistant response');
    const textNode = document.createTextNode('');
    const caret = document.createElement('span');
    caret.className = 'typing-caret';
    caret.setAttribute('aria-hidden', 'true');
    bubble.appendChild(textNode);
    bubble.appendChild(caret);
    wrap.appendChild(bubble);
    messagesEl.appendChild(wrap);
    const tokens = String(text == null ? '' : text).match(/\S+\s*/g) || [];
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const delay = reducedMotion ? 0 : Math.min(24, Math.max(8, 7000 / Math.max(tokens.length, 1)));
    for (const token of tokens) {
      if (delay) await new Promise((r) => setTimeout(r, delay));
      textNode.data += token;
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }
    caret.remove();
    if (meta) {
      const m = document.createElement('div');
      m.className = 'msg-meta';
      m.textContent = meta;
      wrap.appendChild(m);
    }
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function escapeHtml(str) {
    return String(str == null ? '' : str)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function renderMetrics(m, label, provider) {
    if (!m) { metricsEl.innerHTML = '<p class="empty-soft">No metrics yet.</p>'; return; }
    const cells = [
      ['Mode', m.mode], ['LLM', provider || '-'], ['Total', m.latency_ms + ' ms'],
      ['Retrieval', m.retrieval_ms + ' ms'], ['LLM time', m.llm_ms + ' ms'],
      ['Sources', m.source_count], ['Prompt tokens', m.prompt_tokens], ['Completion', m.completion_tokens],
    ];
    metricsEl.innerHTML = '<div class="metrics-grid">' + cells.map(([k,v]) =>
      '<div class="metric-cell"><div class="metric-key">' + k + '</div><div class="metric-val">' + escapeHtml(v) + '</div></div>'
    ).join('') + '</div>' + (label ? '<p class="metrics-note">' + escapeHtml(label) + '</p>' : '');
  }

  function renderSources(sources) {
    if (!sources || !sources.length) { sourcesEl.innerHTML = '<p class="empty-soft">No sources.</p>'; return; }
    sourcesEl.innerHTML = sources.map((s) => {
      const kindClass = s.kind === 'concept' ? 'concept' : s.kind === 'hop' ? 'hop' : '';
      const hops = s.hops ? ' h' + s.hops : '';
      return '<article class="source-card"><div class="source-top"><h3 class="source-title">' + escapeHtml(s.title) +
        '</h3><span class="source-kind ' + kindClass + '">' + escapeHtml(s.kind) + hops +
        '</span></div><p class="source-meta">' + escapeHtml(s.id) + ' · score ' + escapeHtml(s.score) +
        '</p><p class="source-snip">' + escapeHtml(s.snippet) + '</p></article>';
    }).join('');
  }

  async function loadRuns() {
    try {
      const res = await fetch('/api/runs?limit=12');
      const data = await res.json();
      const runs = data.runs || [];
      if (!runs.length) { runsEl.innerHTML = '<p class="empty-soft">No runs logged yet.</p>'; return; }
      runsEl.innerHTML = runs.map((r) =>
        '<div class="run-card"><div class="run-top"><span class="run-mode">' + escapeHtml(r.mode) +
        '</span><span class="run-lat">' + Math.round(r.latency_ms) + ' ms</span></div><p class="run-q">' +
        escapeHtml(r.question) + '</p><p class="run-meta">' + r.source_count + ' sources · tok ' +
        r.prompt_tokens + '/' + r.completion_tokens + '</p></div>'
      ).join('');
    } catch (e) { runsEl.innerHTML = '<p class="status-line err">Could not load runs.</p>'; }
  }

  async function loadSamples() {
    try {
      const res = await fetch('/static/sample_questions.json');
      if (!res.ok) throw new Error('missing');
      const items = await res.json();
      sampleEl.innerHTML = items.map((q) =>
        '<button type="button" data-q="' + escapeHtml(q.question) + '" class="sample-btn">' + escapeHtml(q.question) + '</button>'
      ).join('');
      sampleEl.querySelectorAll('.sample-btn').forEach((btn) => {
        btn.addEventListener('click', () => { input.value = btn.getAttribute('data-q'); input.focus(); });
      });
    } catch (e) { sampleEl.innerHTML = '<p class="empty-soft">Sample questions unavailable.</p>'; }
  }

  function setModeMenuOpen(isOpen) {
    modeSelect.classList.toggle('is-open', isOpen);
    modeToggle.setAttribute('aria-expanded', String(isOpen));
    if (modeMenu) modeMenu.hidden = !isOpen;
  }
  function setMode(value) {
    const option = modeOptions.find((item) => item.dataset.modeOption === value);
    if (!option) return;
    modeEl.value = value;
    modeValue.textContent = option.textContent;
    modeOptions.forEach((item) => item.setAttribute('aria-selected', String(item === option)));
  }

  modeToggle.addEventListener('click', () => setModeMenuOpen(!modeSelect.classList.contains('is-open')));
  modeOptions.forEach((option) => {
    option.addEventListener('click', () => { setMode(option.dataset.modeOption); setModeMenuOpen(false); modeToggle.focus(); });
  });
  modeToggle.addEventListener('keydown', (ev) => {
    if (ev.key === 'Escape') { setModeMenuOpen(false); return; }
    if (ev.key === 'ArrowDown' || ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); setModeMenuOpen(true); modeOptions[0]?.focus(); }
  });
  modeMenu.addEventListener('keydown', (ev) => {
    const currentIndex = modeOptions.indexOf(document.activeElement);
    if (ev.key === 'Escape') { setModeMenuOpen(false); modeToggle.focus(); }
    else if (ev.key === 'ArrowDown') { ev.preventDefault(); modeOptions[(currentIndex + 1) % modeOptions.length].focus(); }
    else if (ev.key === 'ArrowUp') { ev.preventDefault(); modeOptions[(currentIndex - 1 + modeOptions.length) % modeOptions.length].focus(); }
  });
  document.addEventListener('click', (ev) => { if (!modeSelect.contains(ev.target)) setModeMenuOpen(false); });

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const question = input.value.trim();
    if (!question) return;
    const mode = modeEl.value;
    addBubble('user', question);
    input.value = '';
    setStatus('Retrieving (' + mode + ')...');
    try {
      const res = await fetch('/api/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, mode, session_id: sessionId || null }),
      });
      if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || res.statusText); }
      const data = await res.json();
      sessionId = data.session_id;
      localStorage.setItem(sessionKey, sessionId);
      setStatus('Typing answer...');
      await addTypingBubble(data.answer, data.retrieval_label + ' | run #' + data.run_id);
      renderMetrics(data.metrics, data.retrieval_label, data.llm_provider);
      renderSources(data.sources);
      setStatus('Done in ' + data.metrics.latency_ms + ' ms');
      loadRuns();
    } catch (e) {
      setStatus(String(e.message || e), 'err');
      addBubble('assistant', 'Request failed: ' + (e.message || e));
    }
  });

  $('clear-chat').addEventListener('click', () => {
    messagesEl.innerHTML = '';
    sessionId = '';
    localStorage.removeItem(sessionKey);
    renderMetrics(null);
    renderSources([]);
    setStatus('Session cleared');
  });

  function toggleTheme() {
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem(themeKey, next); } catch (e) {}
  }
  ['themeBtn', 'themeBtnSide', 'themeBtnMobile'].forEach((id) => { const el = $(id); if (el) el.addEventListener('click', toggleTheme); });

  const collapseBtn = $('collapseBtn');
  const expandBtn = $('expandBtn');
  const menuBtn = $('menuBtn');
  const scrim = $('scrim');
  if (collapseBtn) collapseBtn.addEventListener('click', () => app.classList.add('collapsed'));
  if (expandBtn) expandBtn.addEventListener('click', () => app.classList.remove('collapsed'));
  function setNavOpen(open) { app.classList.toggle('nav-open', open); if (menuBtn) menuBtn.setAttribute('aria-expanded', String(open)); }
  if (menuBtn) menuBtn.addEventListener('click', () => setNavOpen(!app.classList.contains('nav-open')));
  if (scrim) scrim.addEventListener('click', () => setNavOpen(false));

  loadRuns();
  loadSamples();
  setStatus('Ready');
})();
