/* Optional in-browser Python execution via Pyodide (lazy-loaded on first run).
   Pyodide (~6-10MB) is only fetched when a user clicks "Run", so the rest of
   the site stays fast and fully works offline without it. */
(function () {
  "use strict";

  // The repo's tree solutions do `from tree import TreeNode`; provide that module
  // inside Pyodide's virtual filesystem so those snippets run as-is.
  const TREE_SRC = [
    "class TreeNode:",
    "    def __init__(self, val=0, left=None, right=None):",
    "        self.val = val",
    "        self.left = left",
    "        self.right = right",
    "",
  ].join("\n");

  let pyodidePromise = null;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src; s.onload = resolve; s.onerror = () => reject(new Error("Failed to load " + src));
      document.head.appendChild(s);
    });
  }

  async function ensurePyodide(onStatus) {
    if (pyodidePromise) return pyodidePromise;
    pyodidePromise = (async () => {
      onStatus && onStatus("Downloading Python runtime (one-time)…");
      await loadScript("https://cdn.jsdelivr.net/pyodide/v0.26.2/full/pyodide.js");
      onStatus && onStatus("Starting Python…");
      const py = await window.loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.2/full/" });
      py.FS.writeFile("tree.py", TREE_SRC);
      return py;
    })();
    return pyodidePromise;
  }

  async function runPython(code, outEl) {
    outEl.style.display = "block";
    outEl.innerHTML = '<span class="spinner"></span> Preparing…';
    let py;
    try {
      py = await ensurePyodide((msg) => { outEl.innerHTML = '<span class="spinner"></span> ' + msg; });
    } catch (e) {
      outEl.innerHTML = '<span class="err">Could not load Pyodide: ' + (e.message || e) + "</span>";
      return;
    }
    outEl.innerHTML = '<span class="spinner"></span> Running…';
    try {
      py.runPython("import sys, io\n_buf = io.StringIO()\nsys.stdout = _buf\nsys.stderr = _buf\n");
      py.runPython(code);
      const out = py.runPython("_buf.getvalue()");
      py.runPython("sys.stdout = sys.__stdout__\nsys.stderr = sys.__stderr__\n");
      outEl.innerHTML = out && out.trim()
        ? '<span class="ok">✔ ran successfully</span>\n' + window.escapeHtml(out)
        : '<span class="ok">✔ ran successfully (no output — try adding a print).</span>';
    } catch (e) {
      try { py.runPython("sys.stdout = sys.__stdout__\nsys.stderr = sys.__stderr__\n"); } catch (_) {}
      outEl.innerHTML = '<span class="err">' + window.escapeHtml(String(e.message || e)) + "</span>";
    }
  }

  window.runPython = runPython;
})();
