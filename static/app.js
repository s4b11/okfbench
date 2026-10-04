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
  let busy = false;

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
    if (!sessionId) { runsEl.innerHTML = '<p class="empty-soft">No runs in this session.</p>'; return; }
    try {
      const res = await fetch('/api/runs?limit=12&session_id=' + encodeURIComponent(sessionId));
      if (!res.ok) throw new Error('Could not load runs');
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

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const question = input.value.trim();
    if (!question || busy) return;
    busy = true;
    form.querySelector('button').disabled = true;
    $('clear-chat').disabled = true;
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
      addBubble('assistant', data.answer, data.retrieval_label + ' | run #' + data.run_id);
      renderMetrics(data.metrics, data.retrieval_label, data.llm_provider);
      renderSources(data.sources);
      setStatus('Done in ' + data.metrics.latency_ms + ' ms');
      loadRuns();
    } catch (e) {
      setStatus(String(e.message || e), 'err');
      addBubble('assistant', 'Request failed: ' + (e.message || e));
    } finally {
      busy = false;
      form.querySelector('button').disabled = false;
      $('clear-chat').disabled = false;
    }
  });

  $('clear-chat').addEventListener('click', () => {
    messagesEl.innerHTML = '';
    sessionId = '';
    localStorage.removeItem(sessionKey);
    renderMetrics(null);
    renderSources([]);
    loadRuns();
    setStatus('New session ready');
  });

  function toggleTheme() {
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem(themeKey, next); } catch (e) {}
  }
  const themeButton = $('themeBtn');
  if (themeButton) themeButton.addEventListener('click', toggleTheme);


  loadRuns();
  loadSamples();
  setStatus('Ready');
})();
