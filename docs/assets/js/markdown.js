/* Tiny, safe markdown-ish renderer for the curated prose fields.
   Supports: paragraphs (blank-line separated), **bold**, `inline code`,
   and bullet lists ("- " lines). Everything is HTML-escaped first. */
(function () {
  function escapeHtml(s) {
    return s
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function inline(s) {
    // escape, then re-introduce a tiny set of inline formats
    let out = escapeHtml(s);
    out = out.replace(/`([^`]+)`/g, (_, c) => `<code>${c}</code>`);
    out = out.replace(/\*\*([^*]+)\*\*/g, (_, c) => `<strong>${c}</strong>`);
    return out;
  }

  function mdToHtml(text) {
    if (!text) return "";
    const blocks = text.split(/\n\s*\n/);
    const html = [];
    for (const block of blocks) {
      const lines = block.split("\n");
      const isList = lines.every((l) => l.trim().startsWith("- ") || l.trim() === "");
      if (isList && block.trim().startsWith("- ")) {
        const items = lines
          .filter((l) => l.trim().startsWith("- "))
          .map((l) => `<li>${inline(l.trim().slice(2))}</li>`)
          .join("");
        html.push(`<ul>${items}</ul>`);
      } else {
        html.push(`<p>${inline(block.replace(/\n/g, " ").trim())}</p>`);
      }
    }
    return html.join("");
  }

  // Renders a problem statement: reflows prose paragraphs but preserves the
  // line structure of Example / Input / Output / Constraints blocks (and shows
  // them in a monospace box, LeetCode-style).
  const LABEL_RE = /^(Input|Output|Explanation|Examples?\s*\d*|Constraints?|Sample\s*Input\s*\d*|Sample\s*Output\s*\d*|Note)\b/i;

  function statementToHtml(text) {
    if (!text) return "";
    const blocks = text.split(/\n\s*\n/);
    const out = [];
    for (const block of blocks) {
      const lines = block.split("\n").map((l) => l.replace(/\s+$/, "")).filter((l) => l.trim().length);
      if (!lines.length) continue;
      const isExample = lines.some((l) => LABEL_RE.test(l.trim()));
      if (isExample) {
        const html = lines
          .map((l) => escapeHtml(l).replace(LABEL_RE, (m) => `<strong>${m}</strong>`))
          .join("<br>");
        out.push(`<div class="example">${html}</div>`);
      } else {
        out.push(`<p>${inline(lines.join(" "))}</p>`);
      }
    }
    return out.join("");
  }

  window.mdToHtml = mdToHtml;
  window.statementToHtml = statementToHtml;
  window.escapeHtml = escapeHtml;
})();
