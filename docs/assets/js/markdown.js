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

  // ===========================================================================
  // Richer renderer used by the learning Guides. On top of the basics it adds
  // headings (#, ##, ###), ordered lists, blockquotes, fenced code blocks,
  // pipe tables, horizontal rules, italics and links. Still escapes first.
  // ===========================================================================
  function guideInline(s) {
    let out = escapeHtml(s);
    out = out.replace(/`([^`]+)`/g, (_, c) => `<code>${c}</code>`);
    out = out.replace(/\*\*([^*]+)\*\*/g, (_, c) => `<strong>${c}</strong>`);
    out = out.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, (_, pre, c) => `${pre}<em>${c}</em>`);
    out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g,
      (_, t, u) => `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
    return out;
  }

  function splitRow(line) {
    let s = line.trim();
    if (s.startsWith("|")) s = s.slice(1);
    if (s.endsWith("|")) s = s.slice(0, -1);
    return s.split("|").map((c) => c.trim());
  }

  const BLOCK_START = (l) =>
    /^(#{1,4})\s/.test(l) || l.startsWith(">") || l.startsWith("```") ||
    /^---+$/.test(l) || l.startsWith("- ") || l.startsWith("* ") || /^\d+\.\s/.test(l);

  function guideToHtml(text) {
    if (!text) return "";
    const lines = text.replace(/\r\n/g, "\n").split("\n");
    const html = [];
    let i = 0;
    while (i < lines.length) {
      const t = lines[i].trim();

      if (!t) { i++; continue; }

      // fenced code block
      if (t.startsWith("```")) {
        const lang = t.slice(3).trim() || "none";
        const buf = [];
        i++;
        while (i < lines.length && !lines[i].trim().startsWith("```")) { buf.push(lines[i]); i++; }
        i++; // closing fence
        html.push(`<pre class="language-${lang}"><code class="language-${lang}">${escapeHtml(buf.join("\n"))}</code></pre>`);
        continue;
      }

      // horizontal rule
      if (/^---+$/.test(t)) { html.push("<hr/>"); i++; continue; }

      // heading
      const hm = t.match(/^(#{1,4})\s+(.*)$/);
      if (hm) {
        const lvl = hm[1].length;
        html.push(`<h${lvl} class="guide-h${lvl}">${guideInline(hm[2])}</h${lvl}>`);
        i++; continue;
      }

      // blockquote
      if (t.startsWith(">")) {
        const buf = [];
        while (i < lines.length && lines[i].trim().startsWith(">")) {
          buf.push(lines[i].trim().replace(/^>\s?/, ""));
          i++;
        }
        html.push(`<blockquote class="guide-quote">${guideInline(buf.join(" "))}</blockquote>`);
        continue;
      }

      // table: header row followed by a |---|---| separator
      if (t.includes("|") && i + 1 < lines.length &&
          /-/.test(lines[i + 1]) && /^\s*\|?[\s:|-]+\|?\s*$/.test(lines[i + 1])) {
        const header = splitRow(t);
        i += 2;
        const rows = [];
        while (i < lines.length && lines[i].trim().includes("|") && lines[i].trim()) {
          rows.push(splitRow(lines[i].trim())); i++;
        }
        const th = header.map((h) => `<th>${guideInline(h)}</th>`).join("");
        const body = rows.map((r) => `<tr>${r.map((c) => `<td>${guideInline(c)}</td>`).join("")}</tr>`).join("");
        html.push(`<div class="table-wrap"><table class="guide-table"><thead><tr>${th}</tr></thead><tbody>${body}</tbody></table></div>`);
        continue;
      }

      // ordered list
      if (/^\d+\.\s/.test(t)) {
        const items = [];
        while (i < lines.length && /^\d+\.\s/.test(lines[i].trim())) {
          items.push(`<li>${guideInline(lines[i].trim().replace(/^\d+\.\s/, ""))}</li>`);
          i++;
        }
        html.push(`<ol>${items.join("")}</ol>`);
        continue;
      }

      // unordered list
      if (t.startsWith("- ") || t.startsWith("* ")) {
        const items = [];
        while (i < lines.length && (lines[i].trim().startsWith("- ") || lines[i].trim().startsWith("* "))) {
          items.push(`<li>${guideInline(lines[i].trim().slice(2))}</li>`);
          i++;
        }
        html.push(`<ul>${items.join("")}</ul>`);
        continue;
      }

      // paragraph
      const buf = [t];
      i++;
      while (i < lines.length && lines[i].trim() && !BLOCK_START(lines[i].trim())) {
        buf.push(lines[i].trim()); i++;
      }
      html.push(`<p>${guideInline(buf.join(" "))}</p>`);
    }
    return html.join("");
  }

  window.mdToHtml = mdToHtml;
  window.statementToHtml = statementToHtml;
  window.guideToHtml = guideToHtml;
  window.escapeHtml = escapeHtml;
})();
