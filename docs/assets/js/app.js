/* ===========================================================================
   AlgoLab SPA — hash router, sidebar, and views.
   =========================================================================== */
(function () {
  "use strict";

  const DATA = window.SITE_DATA || { categories: [], problems: [], counts: {}, total: 0, guides: [] };
  if (!DATA.guides) DATA.guides = [];
  const byId = (id) => DATA.problems.find((p) => p.id === id);
  const guideById = (id) => DATA.guides.find((g) => g.id === id);
  const catName = (id) => (DATA.categories.find((c) => c.id === id) || {}).name || id;
  const contentEl = document.getElementById("content");
  const sidebarEl = document.getElementById("sidebar");
  const searchEl = document.getElementById("search");

  let activeVizzes = [];
  function destroyVizzes() {
    activeVizzes.forEach((v) => v && v.destroy && v.destroy());
    activeVizzes = [];
  }

  function langCount() {
    const langs = new Set();
    DATA.problems.forEach((p) => p.files.forEach((f) => langs.add(f.lang)));
    return langs.size;
  }
  function vizCount() { return DATA.problems.filter((p) => p.viz).length; }

  function highlight(scope) {
    if (window.Prism) window.Prism.highlightAllUnder(scope || document);
  }

  // ---------------------------------------------------------------- Sidebar
  function renderSidebar() {
    const route = parseHash();
    let html = '<div class="side-section-title">Categories</div>';
    html += `<a class="side-link ${route.view === "home" ? "active" : ""}" href="#/">🏠 Home<span></span></a>`;
    DATA.categories.forEach((c) => {
      const count = DATA.counts[c.id] || 0;
      if (!count) return;
      const active = route.view === "category" && route.id === c.id;
      html += `<a class="side-link ${active ? "active" : ""}" href="#/category/${c.id}">${c.name}<span class="side-count">${count}</span></a>`;
    });
    if (DATA.guides.length) {
      html += '<div class="side-section-title">Learn — Concept Guides</div>';
      DATA.guides.forEach((g) => {
        const active = route.view === "guide" && route.id === g.id;
        html += `<a class="side-link ${active ? "active" : ""}" href="#/guide/${g.id}">${g.icon || "📘"} ${g.shortTitle || g.title}<span></span></a>`;
      });
    }
    sidebarEl.innerHTML = html;
  }

  // ------------------------------------------------------------------- Home
  function viewHome() {
    const cats = DATA.categories
      .filter((c) => DATA.counts[c.id])
      .map((c) => `
        <div class="cat-card" onclick="location.hash='#/category/${c.id}'">
          <h3>${c.name}</h3>
          <p>${c.blurb}</p>
          <div class="meta">${DATA.counts[c.id]} problem${DATA.counts[c.id] > 1 ? "s" : ""}</div>
        </div>`).join("");

    const featuredIds = ["two-sum", "binary-search", "valid-parentheses", "tree-traversals", "graph-traversal", "max-subarray"];
    const featured = featuredIds.map(byId).filter(Boolean).map(problemCardHtml).join("");

    const guideCards = DATA.guides.map((g) => `
        <div class="guide-card" onclick="location.hash='#/guide/${g.id}'">
          <div class="guide-card-icon">${g.icon || "📘"}</div>
          <div class="guide-card-body">
            <h3>${g.title}</h3>
            <p>${g.blurb}</p>
            <div class="meta">${(g.sections || []).filter((s) => s.viz).length} interactive visuals · concept guide</div>
          </div>
        </div>`).join("");
    const guidesBlock = DATA.guides.length ? `
      <div class="section-head"><h2>Concept guides</h2><span class="sub">read these first if problems feel overwhelming</span></div>
      <div class="guide-card-grid">${guideCards}</div>` : "";

    contentEl.innerHTML = `
      <section class="hero">
        <h1>Learn <span class="grad">Data Structures &amp; Algorithms</span><br/>the way interviews actually test them.</h1>
        <p>Every problem comes with real Java &amp; Python code from the repo, a step-by-step
           <strong>visualization you can play and scrub</strong>, the reasoning behind the data-structure
           choice, and full time/space complexity. Some snippets even <strong>run live in your browser</strong>.</p>
        <div class="hero-stats">
          <div class="hero-stat"><div class="num">${DATA.total}</div><div class="lbl">problems</div></div>
          <div class="hero-stat"><div class="num">${DATA.categories.filter((c) => DATA.counts[c.id]).length}</div><div class="lbl">categories</div></div>
          <div class="hero-stat"><div class="num">${vizCount()}</div><div class="lbl">visualizations</div></div>
          <div class="hero-stat"><div class="num">${langCount()}</div><div class="lbl">languages</div></div>
        </div>
      </section>

      ${guidesBlock}

      <div class="section-head"><h2>Featured problems</h2><span class="sub">great starting points</span></div>
      <div class="card-grid">${featured}</div>

      <div class="section-head"><h2>Browse by topic</h2><span class="sub">pick a pattern to drill</span></div>
      <div class="card-grid">${cats}</div>

      <div class="footer-note">
        Built from the <a href="https://github.com/spawn08/ds-algo-interview" target="_blank" rel="noopener">ds-algo-interview</a>
        repository. Code shown here is generated directly from the source files, so it always matches the repo.
      </div>`;
  }

  // --------------------------------------------------------------- Category
  function problemCardHtml(p) {
    const tags = (p.tags || []).slice(0, 3).map((t) => `<span class="tag">${t}</span>`).join("");
    const vizChip = p.viz ? `<span class="viz-chip">▶ visual</span>` : "";
    return `
      <div class="prob-card" onclick="location.hash='#/problem/${p.id}'">
        <div class="prob-top">
          <h3>${p.title}</h3>
          <span class="badge ${p.difficulty}">${p.difficulty}</span>
        </div>
        <div class="prob-sum">${p.summary}</div>
        <div class="tags">${tags}${vizChip}</div>
      </div>`;
  }

  function viewCategory(id) {
    const cat = DATA.categories.find((c) => c.id === id);
    const probs = DATA.problems.filter((p) => p.category === id);
    if (!cat) { contentEl.innerHTML = '<div class="empty-state">Unknown category.</div>'; return; }
    contentEl.innerHTML = `
      <div class="breadcrumb"><a href="#/">Home</a> / ${cat.name}</div>
      <div class="prob-header"><h1>${cat.name}</h1></div>
      <p class="prob-lead">${cat.blurb}</p>
      <div class="card-grid">${probs.map(problemCardHtml).join("")}</div>`;
  }

  // ---------------------------------------------------------------- Problem
  function viewProblem(id) {
    const p = byId(id);
    if (!p) { contentEl.innerHTML = '<div class="empty-state">Problem not found.</div>'; return; }

    const tags = (p.tags || []).map((t) => `<span class="tag">${t}</span>`).join("");
    const linkBtn = p.link && p.link !== "#"
      ? `<a class="ghost-btn" href="${p.link}" target="_blank" rel="noopener">Problem source ↗</a>` : "";

    const cx = p.complexity || {};
    const cxNote = cx.note ? `<div class="cx-note">${window.mdToHtml(cx.note)}</div>` : "";

    contentEl.innerHTML = `
      <div class="breadcrumb"><a href="#/">Home</a> / <a href="#/category/${p.category}">${catName(p.category)}</a> / ${p.title}</div>
      <div class="prob-header">
        <h1>${p.title}</h1>
        <div class="prob-meta">
          <span class="badge ${p.difficulty}">${p.difficulty}</span>
          ${tags}
          ${linkBtn}
        </div>
        <p class="prob-lead">${p.summary}</p>
      </div>

      ${p.statement ? `
      <div class="panel">
        <div class="panel-head"><span class="ico">❓</span>Problem</div>
        <div class="panel-body statement">${window.statementToHtml(p.statement)}</div>
      </div>` : ""}

      <div id="viz-slot"></div>

      <div class="panel">
        <div class="panel-head"><span class="ico">💡</span>Intuition</div>
        <div class="panel-body prose">${window.mdToHtml(p.idea)}</div>
      </div>

      <div class="panel">
        <div class="panel-head"><span class="ico">🧠</span>Why this approach &amp; data structure</div>
        <div class="panel-body prose">${window.mdToHtml(p.why)}</div>
      </div>

      ${p.deepDive ? `
      <div class="panel">
        <div class="panel-head"><span class="ico">🔬</span>Deep dive &amp; worked example</div>
        <div class="panel-body prose">${window.mdToHtml(p.deepDive)}</div>
      </div>` : ""}

      <div class="panel">
        <div class="panel-head"><span class="ico">⏱️</span>Complexity</div>
        <div class="panel-body">
          <div class="cx-grid">
            <div class="cx-card time"><div class="lbl">Time</div><div class="val">${cx.time || "—"}</div></div>
            <div class="cx-card space"><div class="lbl">Space</div><div class="val">${cx.space || "—"}</div></div>
          </div>
          ${cxNote}
        </div>
      </div>

      <div class="panel" id="code-panel">
        <div class="panel-head"><span class="ico">⌨️</span>Implementation</div>
        <div class="tabs" id="code-tabs"></div>
        <div id="code-body"></div>
      </div>`;

    // visualization
    if (p.viz) {
      const slot = document.getElementById("viz-slot");
      try { activeVizzes.push(window.mountVisualizer(slot, p.viz.type, p.viz)); }
      catch (e) { slot.innerHTML = `<div class="empty-state">Visualization error: ${e.message}</div>`; }
    }

    renderCodeTabs(p);
  }

  // ----------------------------------------------------------------- Guide
  function viewGuide(id) {
    const g = guideById(id);
    if (!g) { contentEl.innerHTML = '<div class="empty-state">Guide not found.</div>'; return; }

    const toc = (g.sections || [])
      .filter((s) => s.title)
      .map((s, i) => `<a href="#guide-sec-${i}">${s.title}</a>`)
      .join("");

    const sectionsHtml = (g.sections || []).map((s, i) => {
      const anchor = s.title ? `id="guide-sec-${i}"` : "";
      const heading = s.title ? `<h2 class="guide-h2" ${anchor}>${s.title}</h2>` : "";
      const body = s.body ? `<div class="prose guide-prose">${window.guideToHtml(s.body)}</div>` : "";
      let vizBlock = "";
      if (s.viz) {
        vizBlock = `
          <div class="guide-viz">
            ${s.vizTitle ? `<div class="guide-viz-title"><span class="ico">▶</span>${s.vizTitle}</div>` : ""}
            <div class="viz-embed" data-viz-index="${i}"></div>
            ${s.caption ? `<p class="guide-viz-caption">${window.guideToHtml(s.caption)}</p>` : ""}
          </div>`;
      }
      return `<section class="guide-section">${heading}${body}${vizBlock}</section>`;
    }).join("");

    contentEl.innerHTML = `
      <div class="breadcrumb"><a href="#/">Home</a> / Concept Guides / ${g.title}</div>
      <div class="guide-hero">
        <div class="guide-hero-icon">${g.icon || "📘"}</div>
        <div>
          <h1>${g.title}</h1>
          <p class="prob-lead">${g.blurb}</p>
        </div>
      </div>
      ${toc ? `<div class="guide-toc"><span class="guide-toc-label">On this page</span>${toc}</div>` : ""}
      ${sectionsHtml}
      <div class="footer-note">
        You've reached the end. Now open a problem in the
        <a href="#/category/${g.id}">${catName(g.id)}</a> category and apply the procedure above.
      </div>`;

    // mount each embedded visualizer
    (g.sections || []).forEach((s, i) => {
      if (!s.viz) return;
      const slot = contentEl.querySelector(`.viz-embed[data-viz-index="${i}"]`);
      if (!slot) return;
      try { activeVizzes.push(window.mountVisualizer(slot, s.viz.type, s.viz)); }
      catch (e) { slot.innerHTML = `<div class="empty-state">Visualization error: ${e.message}</div>`; }
    });

    highlight(contentEl);
  }

  function renderCodeTabs(p) {
    const tabsEl = document.getElementById("code-tabs");
    const bodyEl = document.getElementById("code-body");
    let current = 0;

    function show(i) {
      current = i;
      const f = p.files[i];
      [...tabsEl.children].forEach((c, k) => c.classList.toggle("active", k === i));
      const runBtn = f.lang === "python"
        ? `<button class="run-btn" id="run-btn">▶ Run Python</button>` : "";
      bodyEl.innerHTML = `
        <div class="code-wrap">
          <div class="code-toolbar">${runBtn}<button class="copy-btn" id="copy-btn">Copy</button></div>
          <pre class="language-${f.lang}"><code class="language-${f.lang}">${window.escapeHtml(f.code)}</code></pre>
          <div class="run-output" id="run-output" style="display:none"></div>
        </div>`;
      highlight(bodyEl);

      document.getElementById("copy-btn").onclick = (e) => {
        navigator.clipboard.writeText(f.code).then(() => {
          e.target.textContent = "Copied!";
          setTimeout(() => (e.target.textContent = "Copy"), 1400);
        });
      };
      const rb = document.getElementById("run-btn");
      if (rb) rb.onclick = () => window.runPython(f.code, document.getElementById("run-output"));
    }

    tabsEl.innerHTML = "";
    p.files.forEach((f, i) => {
      const tab = document.createElement("div");
      tab.className = "tab";
      tab.innerHTML = `<span class="lang-dot ${f.lang}"></span>${f.label}`;
      tab.onclick = () => show(i);
      tabsEl.appendChild(tab);
    });
    show(0);
  }

  // ----------------------------------------------------------------- Search
  function viewSearch(q) {
    const query = q.toLowerCase();
    const results = DATA.problems.filter((p) => {
      const hay = (p.title + " " + p.summary + " " + (p.tags || []).join(" ") + " " + catName(p.category)).toLowerCase();
      return hay.includes(query);
    });
    contentEl.innerHTML = `
      <div class="breadcrumb">Search results for “${window.escapeHtml(q)}”</div>
      <div class="prob-header"><h1>${results.length} match${results.length === 1 ? "" : "es"}</h1></div>
      ${results.length ? `<div class="card-grid">${results.map(problemCardHtml).join("")}</div>`
        : '<div class="empty-state">No problems matched. Try another keyword.</div>'}`;
  }

  // ------------------------------------------------------------------ Router
  function parseHash() {
    const h = (location.hash || "#/").replace(/^#/, "");
    const parts = h.split("/").filter(Boolean);
    if (parts[0] === "category" && parts[1]) return { view: "category", id: parts[1] };
    if (parts[0] === "problem" && parts[1]) return { view: "problem", id: parts[1] };
    if (parts[0] === "guide" && parts[1]) return { view: "guide", id: parts[1] };
    return { view: "home" };
  }

  function route() {
    destroyVizzes();
    if (searchEl.value.trim()) { viewSearch(searchEl.value.trim()); renderSidebar(); return; }
    const r = parseHash();
    if (r.view === "category") viewCategory(r.id);
    else if (r.view === "problem") viewProblem(r.id);
    else if (r.view === "guide") viewGuide(r.id);
    else viewHome();
    renderSidebar();
    window.scrollTo(0, 0);
  }

  let searchTimer = null;
  searchEl.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(route, 120);
  });
  window.addEventListener("hashchange", () => { if (!searchEl.value.trim()) route(); });
  window.addEventListener("prism-ready", () => highlight(document));

  // boot
  renderSidebar();
  route();
})();
