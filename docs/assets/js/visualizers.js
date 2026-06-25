/* ===========================================================================
   AlgoLab visualizers
   ---------------------------------------------------------------------------
   Each entry in `Visualizers` re-implements an algorithm to emit a list of
   "steps". A generic player renders steps with play / step / scrub controls
   and a narration line, so learners watch the data structure evolve.

   A generator returns:
     {
       kind: '1d' | '2d' | 'tree' | 'graph',
       modes?: [{id, label}],          // optional toggle (e.g. BFS/DFS)
       layout?: {...},                 // for tree/graph (nodes + edges)
       build(modeId) -> [ step, ... ]
     }
   =========================================================================== */
(function () {
  "use strict";

  const hl = (v) => `<span class="hl">${v}</span>`;

  // ---- small DOM helpers ----
  function el(tag, cls, html) {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  // =========================================================================
  // RENDERERS
  // =========================================================================
  function renderSidePanels(stage, side) {
    if (!side || !side.length) return;
    const wrap = el("div", "viz-side");
    side.forEach((p) => {
      const panel = el("div", "kv-panel");
      panel.appendChild(el("h4", null, p.title));
      if (p.type === "stack") {
        const box = el("div", "stack-box");
        (p.items || []).forEach((it, i) => {
          const top = i === p.items.length - 1;
          box.appendChild(el("div", "stack-item" + (top ? " top" : ""), String(it)));
        });
        if (!p.items || !p.items.length) box.appendChild(el("div", "kv-row", "<span class='muted'>empty</span>"));
        panel.appendChild(box);
      } else {
        if (!p.rows || !p.rows.length) {
          panel.appendChild(el("div", "kv-row", "<span class='muted'>—</span>"));
        }
        (p.rows || []).forEach((r) => {
          panel.appendChild(el("div", "kv-row", `<span class="k">${r.k}</span><span>${r.v}</span>`));
        });
      }
      wrap.appendChild(panel);
    });
    stage.appendChild(wrap);
  }

  function render1D(stage, step) {
    stage.innerHTML = "";
    const row = el("div", "cells");
    step.cells.forEach((c, i) => {
      const col = el("div", "cell-col");
      const badge = c.badge
        ? `<div class="ptr-badge ${c.badge}">${c.badge}</div>`
        : `<div class="ptr-empty"></div>`;
      col.innerHTML = `${badge}<div class="cell ${c.cls || ""}">${c.v}<span class="idx">${c.idx != null ? c.idx : i}</span></div>`;
      row.appendChild(col);
    });
    stage.appendChild(row);
    renderSidePanels(stage, step.side);
  }

  function render2D(stage, step) {
    stage.innerHTML = "";
    const cols = step.grid[0].length;
    const grid = el("div", "grid2d");
    grid.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    step.grid.forEach((rowArr) => {
      rowArr.forEach((c) => {
        grid.appendChild(el("div", "cell " + (c.cls || ""), String(c.v)));
      });
    });
    stage.appendChild(grid);
    renderSidePanels(stage, step.side);
  }

  function renderGraphLike(stage, layout, step) {
    stage.innerHTML = "";
    const NS = "http://www.w3.org/2000/svg";
    const pad = 44, r = 21;
    const xs = layout.nodes.map((n) => n.x), ys = layout.nodes.map((n) => n.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const w = maxX - minX + pad * 2, h = maxY - minY + pad * 2;
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", "viz-svg");
    svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
    const ox = pad - minX, oy = pad - minY;
    const active = step.activeEdges || new Set();

    if (layout.directed) {
      const defs = document.createElementNS(NS, "defs");
      defs.innerHTML =
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">' +
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#6b7682"/></marker>';
      svg.appendChild(defs);
    }

    layout.edges.forEach((e) => {
      const a = layout.nodes.find((n) => n.id === e.from);
      const b = layout.nodes.find((n) => n.id === e.to);
      const line = document.createElementNS(NS, "line");
      const isActive = active.has(e.from + "-" + e.to) || active.has(e.to + "-" + e.from);
      line.setAttribute("class", "edge-line" + (isActive ? " active" : ""));
      // For directed graphs, stop the line short of the target node so the arrow shows.
      let x1 = a.x + ox, y1 = a.y + oy, x2 = b.x + ox, y2 = b.y + oy;
      if (layout.directed) {
        const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
        x2 -= (dx / len) * (r + 4); y2 -= (dy / len) * (r + 4);
        x1 += (dx / len) * r; y1 += (dy / len) * r;
        line.setAttribute("marker-end", "url(#arrow)");
      }
      line.setAttribute("x1", x1); line.setAttribute("y1", y1);
      line.setAttribute("x2", x2); line.setAttribute("y2", y2);
      svg.appendChild(line);
      // optional edge weight label (for weighted graphs like Dijkstra)
      if (e.weight != null) {
        const mx = (a.x + b.x) / 2 + ox, my = (a.y + b.y) / 2 + oy;
        const wt = document.createElementNS(NS, "text");
        wt.setAttribute("class", "edge-weight");
        wt.setAttribute("x", mx); wt.setAttribute("y", my - 4);
        wt.textContent = e.weight;
        svg.appendChild(wt);
      }
    });
    layout.nodes.forEach((n) => {
      const g = document.createElementNS(NS, "g");
      const c = document.createElementNS(NS, "circle");
      c.setAttribute("class", "node-circle " + ((step.nodeCls && step.nodeCls[n.id]) || ""));
      c.setAttribute("cx", n.x + ox); c.setAttribute("cy", n.y + oy); c.setAttribute("r", r);
      const t = document.createElementNS(NS, "text");
      t.setAttribute("class", "node-label");
      t.setAttribute("x", n.x + ox); t.setAttribute("y", n.y + oy + 1);
      t.textContent = n.label;
      g.appendChild(c); g.appendChild(t);
      // optional per-node badge (computed value: height, gain, in-degree…)
      const badge = step.nodeBadge && step.nodeBadge[n.id];
      if (badge != null) {
        const bt = document.createElementNS(NS, "text");
        bt.setAttribute("class", "node-badge");
        bt.setAttribute("x", n.x + ox + r + 4); bt.setAttribute("y", n.y + oy - r + 2);
        bt.textContent = badge;
        g.appendChild(bt);
      }
      svg.appendChild(g);
    });
    stage.appendChild(svg);

    if (step.output != null) {
      stage.appendChild(el("div", "output-strip",
        `<span class="muted">${step.outputLabel || "visited"}:</span> ${step.output || "<span class='muted'>—</span>"}`));
    }
    renderSidePanels(stage, step.side);
  }

  // =========================================================================
  // GENERATORS
  // =========================================================================
  const Visualizers = {};

  // ---------- Two Sum (hash map) ----------
  Visualizers.twoSumHash = function (p) {
    const nums = p.nums, target = p.target;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const base = (extra) => nums.map((v, i) => ({ v, idx: i, cls: extra && extra[i] || "" }));
        const seen = {};
        steps.push({
          narration: `Goal: find two indices summing to ${hl(target)}. We keep a hash map of <code>value → index</code> for O(1) lookups.`,
          cells: base(), side: [{ title: "seen map", type: "kv", rows: [] }],
        });
        for (let i = 0; i < nums.length; i++) {
          const need = target - nums[i];
          const rows = Object.entries(seen).map(([k, v]) => ({ k, v }));
          const cls = {}; cls[i] = "active";
          steps.push({
            narration: `i=${hl(i)}: value ${hl(nums[i])}. Complement needed = ${target} − ${nums[i]} = ${hl(need)}. Is ${need} in the map?`,
            cells: base(cls),
            side: [{ title: "seen map", type: "kv", rows }],
          });
          if (need in seen) {
            const cls2 = {}; cls2[seen[need]] = "match"; cls2[i] = "match";
            steps.push({
              narration: `✅ ${need} is in the map at index ${hl(seen[need])}. Answer = [${seen[need]}, ${i}].`,
              cells: base(cls2),
              side: [{ title: "seen map", type: "kv", rows }],
            });
            return steps;
          }
          seen[nums[i]] = i;
          const rows2 = Object.entries(seen).map(([k, v]) => ({ k, v }));
          const cls3 = {}; cls3[i] = "visited";
          steps.push({
            narration: `Not found — store ${hl(nums[i] + " → " + i)} in the map and move on.`,
            cells: base(cls3),
            side: [{ title: "seen map", type: "kv", rows: rows2 }],
          });
        }
        steps.push({ narration: "No pair found.", cells: base() });
        return steps;
      },
    };
  };

  // ---------- Two pointers on a sorted array ----------
  Visualizers.twoPointers = function (p) {
    const nums = [...p.nums].sort((a, b) => a - b), target = p.target;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const frame = (lo, hi, cls) => nums.map((v, i) => ({
          v, idx: i,
          cls: cls && cls[i] || (i < lo || i > hi ? "dim" : ""),
          badge: i === lo && i === hi ? "L" : i === lo ? "L" : i === hi ? "R" : null,
        }));
        let lo = 0, hi = nums.length - 1;
        steps.push({
          narration: `Array is sorted: ${hl("[" + nums.join(", ") + "]")}. Start with L at the smallest and R at the largest value.`,
          cells: frame(lo, hi),
        });
        while (lo < hi) {
          const sum = nums[lo] + nums[hi];
          steps.push({
            narration: `sum = ${nums[lo]} + ${nums[hi]} = ${hl(sum)}, target = ${hl(target)}.`,
            cells: frame(lo, hi),
            side: [{ title: "state", type: "kv", rows: [{ k: "L", v: lo }, { k: "R", v: hi }, { k: "sum", v: sum }] }],
          });
          if (sum === target) {
            const cls = {}; cls[lo] = "match"; cls[hi] = "match";
            steps.push({ narration: `✅ sum equals target. Answer = 1-indexed [${lo + 1}, ${hi + 1}].`, cells: frame(lo, hi, cls) });
            return steps;
          } else if (sum < target) {
            steps.push({ narration: `sum ${hl(sum)} < ${target}: too small → move ${hl("L")} right to grow the sum.`, cells: frame(lo, hi) });
            lo++;
          } else {
            steps.push({ narration: `sum ${hl(sum)} > ${target}: too big → move ${hl("R")} left to shrink the sum.`, cells: frame(lo, hi) });
            hi--;
          }
        }
        steps.push({ narration: "Pointers crossed — no pair.", cells: frame(lo, hi) });
        return steps;
      },
    };
  };

  // ---------- Kadane ----------
  Visualizers.kadane = function (p) {
    const nums = p.nums;
    return {
      kind: "1d",
      build() {
        const steps = [];
        let cur = nums[0], best = nums[0], runStart = 0, bestS = 0, bestE = 0;
        const frame = (i, rs, re, finalBest) => nums.map((v, idx) => {
          let cls = "";
          if (finalBest) { if (idx >= bestS && idx <= bestE) cls = "match"; }
          else { if (idx >= rs && idx <= re) cls = "window"; if (idx === i) cls += " active"; }
          return { v, idx, cls: cls.trim() };
        });
        steps.push({
          narration: `Kadane: at each step, extend the current run or restart. current = best = ${hl(nums[0])}.`,
          cells: frame(0, 0, 0),
          side: [{ title: "state", type: "kv", rows: [{ k: "current", v: cur }, { k: "best", v: best }] }],
        });
        for (let i = 1; i < nums.length; i++) {
          if (nums[i] > cur + nums[i]) { cur = nums[i]; runStart = i; }
          else { cur = cur + nums[i]; }
          let restarted = runStart === i;
          if (cur > best) { best = cur; bestS = runStart; bestE = i; }
          steps.push({
            narration: restarted
              ? `i=${hl(i)}: starting fresh is better (${nums[i]} > current+${nums[i]}). current = ${hl(cur)}.`
              : `i=${hl(i)}: extend the run. current = ${hl(cur)}. best so far = ${hl(best)}.`,
            cells: frame(i, runStart, i),
            side: [{ title: "state", type: "kv", rows: [{ k: "current", v: cur }, { k: "best", v: best }] }],
          });
        }
        steps.push({
          narration: `Done. Maximum subarray sum = ${hl(best)} (highlighted).`,
          cells: frame(-1, 0, 0, true),
          side: [{ title: "result", type: "kv", rows: [{ k: "answer", v: best }] }],
        });
        return steps;
      },
    };
  };

  // ---------- Fixed-size window (optionally distinct) ----------
  Visualizers.fixedWindow = function (p) {
    const nums = p.nums, k = p.k, distinct = !!p.distinct;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const frame = (l, r, cls) => nums.map((v, i) => ({
          v, idx: i, cls: (cls && cls[i]) || (i >= l && i <= r ? "window" : "dim"),
        }));
        const freq = {};
        let sum = 0, best = 0;
        const rowsFor = () => {
          const base = [{ k: "window sum", v: sum }, { k: "max", v: best }];
          if (distinct) base.push({ k: "distinct?", v: Object.keys(freq).length === k ? "yes" : "no" });
          return base;
        };
        steps.push({ narration: `Window of size k=${hl(k)} will slide across the array.`, cells: nums.map((v, i) => ({ v, idx: i, cls: "dim" })) });
        for (let r = 0; r < nums.length; r++) {
          sum += nums[r]; freq[nums[r]] = (freq[nums[r]] || 0) + 1;
          if (r >= k) {
            const left = nums[r - k];
            sum -= left; freq[left]--; if (freq[left] === 0) delete freq[left];
          }
          const l = Math.max(0, r - k + 1);
          if (r >= k - 1) {
            const valid = !distinct || Object.keys(freq).length === k;
            if (valid) best = Math.max(best, sum);
            steps.push({
              narration: r >= k
                ? `Slide: add ${hl(nums[r])}, drop ${hl(nums[r - k])}. Window sum = ${hl(sum)}.` + (distinct ? ` ${valid ? "All distinct ✅" : "has a duplicate ✗"}` : "")
                : `First full window [${l}..${r}], sum = ${hl(sum)}.` + (distinct ? ` ${valid ? "All distinct ✅" : "has a duplicate ✗"}` : ""),
              cells: frame(l, r, valid ? null : nums.reduce((a, _v, i) => { a[i] = (i >= l && i <= r) ? "bad" : "dim"; return a; }, {})),
              side: [{ title: "state", type: "kv", rows: rowsFor() }],
            });
          } else {
            steps.push({ narration: `Filling the first window… added ${hl(nums[r])}.`, cells: frame(l, r), side: [{ title: "state", type: "kv", rows: rowsFor() }] });
          }
        }
        steps.push({ narration: `Best window sum = ${hl(best)}.`, cells: nums.map((v, i) => ({ v, idx: i, cls: "dim" })), side: [{ title: "result", type: "kv", rows: [{ k: "answer", v: best }] }] });
        return steps;
      },
    };
  };

  // ---------- Variable sliding window: longest substring w/o repeat ----------
  Visualizers.slidingWindow = function (p) {
    const s = p.s;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const chars = s.split("");
        const frame = (l, r, cls) => chars.map((v, i) => ({
          v, idx: i, cls: (cls && cls[i]) || (i >= l && i <= r ? "window" : "dim"),
          badge: i === l ? "L" : i === r ? "R" : null,
        }));
        const last = {};
        let l = 0, best = 0, bestL = 0, bestR = 0;
        steps.push({ narration: `Find the longest window with all-unique characters. Track each char's last index.`, cells: chars.map((v, i) => ({ v, idx: i, cls: "dim" })) });
        for (let r = 0; r < chars.length; r++) {
          const ch = chars[r];
          if (ch in last && last[ch] >= l) {
            const old = l; l = last[ch] + 1;
            steps.push({
              narration: `'${hl(ch)}' seen at ${last[ch]} (inside window). Jump L from ${old} to ${hl(l)}.`,
              cells: frame(l, r),
              side: [{ title: "last index", type: "kv", rows: Object.entries(last).map(([k, v]) => ({ k: "'" + k + "'", v })) }],
            });
          }
          last[ch] = r;
          const len = r - l + 1;
          if (len > best) { best = len; bestL = l; bestR = r; }
          steps.push({
            narration: `r=${hl(r)} ('${ch}'). Window [${l}..${r}], length ${hl(len)}. Longest so far = ${hl(best)}.`,
            cells: frame(l, r),
            side: [{ title: "last index", type: "kv", rows: Object.entries(last).map(([k, v]) => ({ k: "'" + k + "'", v })) }],
          });
        }
        const cls = {}; for (let i = bestL; i <= bestR; i++) cls[i] = "match";
        steps.push({ narration: `Longest substring without repeats has length ${hl(best)} → "${hl(s.slice(bestL, bestR + 1))}".`, cells: frame(bestL, bestR, cls) });
        return steps;
      },
    };
  };

  // ---------- Binary search ----------
  Visualizers.binarySearch = function (p) {
    const nums = p.nums, target = p.target;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const frame = (lo, hi, mid, cls) => nums.map((v, i) => ({
          v, idx: i,
          cls: (cls && cls[i]) || (i < lo || i > hi ? "dim" : i === mid ? "active" : ""),
          badge: i === mid ? "mid" : i === lo ? "L" : i === hi ? "R" : null,
        }));
        let lo = 0, hi = nums.length - 1;
        steps.push({ narration: `Search for ${hl(target)} in a sorted array. Range = whole array.`, cells: frame(lo, hi, -1) });
        while (lo <= hi) {
          const mid = lo + ((hi - lo) >> 1);
          steps.push({
            narration: `mid = ${hl(mid)} → value ${hl(nums[mid])}. Compare with target ${target}.`,
            cells: frame(lo, hi, mid),
            side: [{ title: "range", type: "kv", rows: [{ k: "low", v: lo }, { k: "mid", v: mid }, { k: "high", v: hi }] }],
          });
          if (nums[mid] === target) {
            const cls = {}; cls[mid] = "match";
            steps.push({ narration: `✅ Found ${target} at index ${hl(mid)}.`, cells: frame(lo, hi, mid, cls) });
            return steps;
          } else if (nums[mid] > target) {
            steps.push({ narration: `${nums[mid]} > ${target}: discard the right half. high = ${hl(mid - 1)}.`, cells: frame(lo, hi, mid) });
            hi = mid - 1;
          } else {
            steps.push({ narration: `${nums[mid]} < ${target}: discard the left half. low = ${hl(mid + 1)}.`, cells: frame(lo, hi, mid) });
            lo = mid + 1;
          }
        }
        steps.push({ narration: `Range empty — ${target} is not present.`, cells: nums.map((v, i) => ({ v, idx: i, cls: "dim" })) });
        return steps;
      },
    };
  };

  // ---------- Palindrome two-pointer ----------
  Visualizers.stringTwoPointer = function (p) {
    const cleaned = p.s.toLowerCase().replace(/[^a-z0-9]/g, "");
    return {
      kind: "1d",
      build() {
        const steps = [];
        const chars = cleaned.split("");
        const frame = (l, r, cls) => chars.map((v, i) => ({
          v, idx: i, cls: (cls && cls[i]) || (i < l || i > r ? "dim" : ""),
          badge: i === l && i === r ? "L" : i === l ? "L" : i === r ? "R" : null,
        }));
        steps.push({ narration: `Cleaned string: "${hl(cleaned)}". Compare characters from both ends inward.`, cells: frame(0, chars.length - 1) });
        let l = 0, r = chars.length - 1;
        while (l < r) {
          if (chars[l] === chars[r]) {
            const cls = {}; cls[l] = "match"; cls[r] = "match";
            steps.push({ narration: `'${hl(chars[l])}' == '${hl(chars[r])}' ✅ — move both inward.`, cells: frame(l, r, cls) });
            l++; r--;
          } else {
            const cls = {}; cls[l] = "bad"; cls[r] = "bad";
            steps.push({ narration: `'${hl(chars[l])}' ≠ '${hl(chars[r])}' ✗ — not a palindrome.`, cells: frame(l, r, cls) });
            return steps;
          }
        }
        steps.push({ narration: `Pointers met with no mismatch → it IS a palindrome. ✅`, cells: chars.map((v, i) => ({ v, idx: i, cls: "match" })) });
        return steps;
      },
    };
  };

  // ---------- Valid parentheses (stack) ----------
  Visualizers.stackParens = function (p) {
    const s = p.s;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const chars = s.split("");
        const frame = (i, cls) => chars.map((v, idx) => ({ v, idx, cls: (cls && cls[idx]) || (idx === i ? "active" : idx < i ? "" : "dim") }));
        const pairs = { ")": "(", "]": "[", "}": "{" };
        const stack = [];
        steps.push({ narration: `Scan left→right. Push openers; on a closer, the stack top must match.`, cells: frame(-1), side: [{ title: "stack", type: "stack", items: [] }] });
        for (let i = 0; i < chars.length; i++) {
          const c = chars[i];
          if (c in pairs) {
            const expect = pairs[c];
            if (!stack.length || stack[stack.length - 1] !== expect) {
              const cls = {}; cls[i] = "bad";
              steps.push({ narration: `Closer '${hl(c)}' but top is '${hl(stack[stack.length - 1] || "∅")}' (need '${expect}') ✗ — invalid.`, cells: frame(i, cls), side: [{ title: "stack", type: "stack", items: [...stack] }] });
              return steps;
            }
            stack.pop();
            steps.push({ narration: `Closer '${hl(c)}' matches top '${hl(expect)}' ✅ — pop it.`, cells: frame(i), side: [{ title: "stack", type: "stack", items: [...stack] }] });
          } else {
            stack.push(c);
            steps.push({ narration: `Opener '${hl(c)}' → push onto stack.`, cells: frame(i), side: [{ title: "stack", type: "stack", items: [...stack] }] });
          }
        }
        const ok = stack.length === 0;
        steps.push({
          narration: ok ? `End of string and stack is empty → valid. ✅` : `Leftover openers on the stack → invalid. ✗`,
          cells: chars.map((v, idx) => ({ v, idx, cls: ok ? "match" : "" })),
          side: [{ title: "stack", type: "stack", items: [...stack] }],
        });
        return steps;
      },
    };
  };

  // ---------- Matrix rotate ----------
  Visualizers.matrixRotate = function (p) {
    const src = p.matrix.map((r) => [...r]);
    return {
      kind: "2d",
      build() {
        const steps = [];
        const n = src.length;
        const m = src.map((r) => [...r]);
        const snap = (cls) => m.map((row, i) => row.map((v, j) => ({ v, cls: (cls && cls[i + "," + j]) || "" })));
        steps.push({ narration: `Rotate 90° clockwise = transpose, then reverse each row. Start:`, grid: snap() });
        // transpose
        for (let i = 0; i < n; i++) {
          for (let j = i + 1; j < n; j++) {
            const cls = {}; cls[i + "," + j] = "active"; cls[j + "," + i] = "active";
            const tmp = m[i][j]; m[i][j] = m[j][i]; m[j][i] = tmp;
            steps.push({ narration: `Transpose: swap (${i},${j}) ↔ (${j},${i}).`, grid: snap(cls) });
          }
        }
        steps.push({ narration: `Transpose complete. Now reverse each row.`, grid: snap() });
        for (let i = 0; i < n; i++) {
          m[i].reverse();
          const cls = {}; for (let j = 0; j < n; j++) cls[i + "," + j] = "fill-match";
          steps.push({ narration: `Reverse row ${hl(i)}.`, grid: snap(cls) });
        }
        steps.push({ narration: `Done — matrix rotated 90° clockwise in place.`, grid: snap() });
        return steps;
      },
    };
  };

  // ---------- DP grid (LCS / longest common substring) ----------
  Visualizers.dpGrid = function (p) {
    const a = p.a, b = p.b, mode = p.mode || "subsequence";
    return {
      kind: "2d",
      build() {
        const steps = [];
        const m = a.length, n = b.length;
        const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
        // grid with header row/col (chars)
        const snap = (ai, bj, cls) => {
          const grid = [];
          const header = [{ v: "·", cls: "water" }, { v: "∅", cls: "water" }];
          for (let j = 0; j < n; j++) header.push({ v: b[j], cls: "land" + ((bj === j) ? " active" : "") });
          grid.push(header);
          for (let i = 0; i <= m; i++) {
            const row = [];
            row.push({ v: i === 0 ? "∅" : a[i - 1], cls: "land" + ((ai === i - 1) ? " active" : "") });
            for (let j = 0; j <= n; j++) {
              let c = "water";
              if (cls && cls[i + "," + j]) c = cls[i + "," + j];
              row.push({ v: dp[i][j], cls: c });
            }
            grid.push(row);
          }
          return grid;
        };
        steps.push({
          narration: mode === "substring"
            ? `Longest common <strong>substring</strong> of "${hl(a)}" and "${hl(b)}". Match → dp[i][j]=1+diagonal; mismatch → <strong>reset to 0</strong>.`
            : `Longest common <strong>subsequence</strong> of "${hl(a)}" and "${hl(b)}". Match → 1+diagonal; else max(up, left).`,
          grid: snap(-1, -1),
        });
        let best = 0;
        for (let i = 1; i <= m; i++) {
          for (let j = 1; j <= n; j++) {
            const match = a[i - 1] === b[j - 1];
            if (match) dp[i][j] = 1 + dp[i - 1][j - 1];
            else dp[i][j] = mode === "substring" ? 0 : Math.max(dp[i - 1][j], dp[i][j - 1]);
            best = Math.max(best, dp[i][j]);
            const cls = {}; cls[i + "," + j] = match ? "fill-match" : "active";
            steps.push({
              narration: match
                ? `'${hl(a[i - 1])}' == '${hl(b[j - 1])}' → dp=1+diagonal=${hl(dp[i][j])}.`
                : (mode === "substring"
                  ? `'${a[i - 1]}' ≠ '${b[j - 1]}' → reset dp=${hl(0)}.`
                  : `'${a[i - 1]}' ≠ '${b[j - 1]}' → dp=max(up,left)=${hl(dp[i][j])}.`),
              grid: snap(i - 1, j - 1, cls),
              side: [{ title: "result", type: "kv", rows: [{ k: mode === "substring" ? "longest" : "LCS", v: mode === "substring" ? best : dp[m][n] }] }],
            });
          }
        }
        steps.push({
          narration: mode === "substring"
            ? `Answer = largest cell = ${hl(best)}.`
            : `Answer = bottom-right cell = ${hl(dp[m][n])}.`,
          grid: snap(-1, -1),
          side: [{ title: "result", type: "kv", rows: [{ k: "answer", v: mode === "substring" ? best : dp[m][n] }] }],
        });
        return steps;
      },
    };
  };

  // ---------- Grid DFS (number of islands) ----------
  Visualizers.gridDFS = function (p) {
    const src = p.grid.map((r) => [...r]);
    return {
      kind: "2d",
      build() {
        const steps = [];
        const g = src.map((r) => [...r]);
        const rows = g.length, cols = g[0].length;
        const cellCls = (val, sunk) => sunk ? "sunk" : val === "1" ? "land" : "water";
        const snap = (active) => g.map((row, i) => row.map((v, j) => ({
          v, cls: (active && active === i + "," + j) ? "active" : cellCls(v, false),
        })));
        let islands = 0;
        const dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]];
        steps.push({ narration: `Scan the grid. Each unvisited land cell starts a new island; flood-fill sinks it.`, grid: snap(), side: [{ title: "count", type: "kv", rows: [{ k: "islands", v: 0 }] }] });
        for (let i = 0; i < rows; i++) {
          for (let j = 0; j < cols; j++) {
            if (g[i][j] === "1") {
              islands++;
              const stack = [[i, j]]; g[i][j] = "0";
              steps.push({ narration: `Found land at (${hl(i)},${hl(j)}) → island #${hl(islands)}. Begin flood fill.`, grid: snap(i + "," + j), side: [{ title: "count", type: "kv", rows: [{ k: "islands", v: islands }] }] });
              while (stack.length) {
                const [x, y] = stack.pop();
                for (const [dx, dy] of dirs) {
                  const nx = x + dx, ny = y + dy;
                  if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && g[nx][ny] === "1") {
                    g[nx][ny] = "0"; stack.push([nx, ny]);
                  }
                }
              }
              steps.push({ narration: `Flood fill done — whole landmass sunk.`, grid: snap(), side: [{ title: "count", type: "kv", rows: [{ k: "islands", v: islands }] }] });
            }
          }
        }
        steps.push({ narration: `Scan complete. Total islands = ${hl(islands)}.`, grid: snap(), side: [{ title: "result", type: "kv", rows: [{ k: "islands", v: islands }] }] });
        return steps;
      },
    };
  };

  // ---------- Tree traversal (DFS orders) ----------
  function buildTreeLayout(arr) {
    // LeetCode-style level-order deserialization with explicit nulls.
    if (!arr.length || arr[0] == null) return { nodes: [], edges: [], root: null };
    let idCounter = 0;
    const mk = (val) => ({ id: idCounter++, val, left: null, right: null });
    const root = mk(arr[0]);
    const q = [root];
    let i = 1;
    while (q.length && i < arr.length) {
      const node = q.shift();
      if (i < arr.length) { if (arr[i] != null) { node.left = mk(arr[i]); q.push(node.left); } i++; }
      if (i < arr.length) { if (arr[i] != null) { node.right = mk(arr[i]); q.push(node.right); } i++; }
    }
    // assign x by in-order index, y by depth
    const nodes = [], edges = [];
    let xCounter = 0;
    const SX = 64, SY = 74;
    (function place(node, depth) {
      if (!node) return;
      place(node.left, depth + 1);
      node._x = xCounter++ * SX; node._y = depth * SY;
      nodes.push({ id: node.id, label: String(node.val), x: node._x, y: node._y });
      if (node.left) edges.push({ from: node.id, to: node.left.id });
      if (node.right) edges.push({ from: node.id, to: node.right.id });
      place(node.right, depth + 1);
    })(root, 0);
    return { nodes, edges, root };
  }

  Visualizers.treeTraversal = function (p) {
    const layout = buildTreeLayout(p.tree);
    return {
      kind: "tree",
      layout,
      modes: [
        { id: "in", label: "In-order (L, N, R)" },
        { id: "pre", label: "Pre-order (N, L, R)" },
        { id: "post", label: "Post-order (L, R, N)" },
      ],
      build(mode) {
        const steps = [];
        const out = [];
        const nodeCls = {};
        const visit = (node, label) => {
          out.push(node.val);
          nodeCls[node.id] = "done";
          steps.push({
            narration: `Visit node ${hl(node.val)} (${label}).`,
            nodeCls: { ...nodeCls },
            output: out.join(" → "),
          });
        };
        const enter = (node) => {
          if (!node) return;
          nodeCls[node.id] = "active";
          steps.push({ narration: `Enter node ${hl(node.val)}.`, nodeCls: { ...nodeCls }, output: out.join(" → ") });
        };
        const dfs = (node) => {
          if (!node) return;
          enter(node);
          if (mode === "pre") visit(node, "record on enter");
          dfs(node.left);
          if (mode === "in") visit(node, "record after left subtree");
          dfs(node.right);
          if (mode === "post") visit(node, "record after both subtrees");
          nodeCls[node.id] = "done";
        };
        steps.push({ narration: `Depth-first traversal in <strong>${mode}-order</strong>.`, nodeCls: {}, output: "" });
        dfs(layout.root);
        steps.push({ narration: `Traversal order: ${hl(out.join(", "))}.`, nodeCls: { ...nodeCls }, output: out.join(" → ") });
        return steps;
      },
    };
  };

  // ---------- Tree level-order (BFS) ----------
  Visualizers.treeLevelOrder = function (p) {
    const layout = buildTreeLayout(p.tree);
    // need child links: rebuild map id->node via layout edges
    const idToNode = {};
    (function () {
      // reconstruct adjacency from edges (parent->child) to BFS
    })();
    return {
      kind: "tree",
      layout,
      build() {
        const steps = [];
        // rebuild tree object for BFS
        const arr = p.tree;
        const root = layout.root;
        const nodeCls = {};
        const result = [];
        steps.push({ narration: `BFS with a queue: process the tree one level at a time.`, nodeCls: {}, output: "" });
        let queue = [root].filter(Boolean);
        let level = 0;
        while (queue.length) {
          const size = queue.length;
          const levelVals = [];
          const next = [];
          queue.forEach((n) => { nodeCls[n.id] = "active"; });
          steps.push({ narration: `Level ${hl(level)}: queue holds ${hl(size)} node(s). Drain them all.`, nodeCls: { ...nodeCls }, output: result.map((l) => "[" + l.join(",") + "]").join(" ") });
          for (const n of queue) {
            levelVals.push(n.val);
            nodeCls[n.id] = "done";
            if (n.left) next.push(n.left);
            if (n.right) next.push(n.right);
          }
          result.push(levelVals);
          steps.push({ narration: `Collected level ${level} = ${hl("[" + levelVals.join(", ") + "]")}; enqueue their children.`, nodeCls: { ...nodeCls }, output: result.map((l) => "[" + l.join(",") + "]").join(" ") });
          queue = next; level++;
        }
        steps.push({ narration: `Result = ${hl(result.map((l) => "[" + l.join(",") + "]").join(", "))}.`, nodeCls: { ...nodeCls }, output: result.map((l) => "[" + l.join(",") + "]").join(" ") });
        return steps;
      },
    };
  };

  // ---------- Graph traversal (BFS / DFS) ----------
  Visualizers.graphTraversal = function (p) {
    const adj = p.graph, start = p.start;
    const ids = Object.keys(adj);
    // circular layout
    const N = ids.length, R = 120, cx = 150, cy = 140;
    const nodes = ids.map((id, i) => ({
      id, label: id,
      x: cx + R * Math.cos((2 * Math.PI * i) / N - Math.PI / 2),
      y: cy + R * Math.sin((2 * Math.PI * i) / N - Math.PI / 2),
    }));
    const edgeSet = new Set();
    const edges = [];
    ids.forEach((u) => adj[u].forEach((v) => {
      const key = [u, v].sort().join("|");
      if (!edgeSet.has(key)) { edgeSet.add(key); edges.push({ from: u, to: v }); }
    }));
    const layout = { nodes, edges };
    return {
      kind: "graph",
      layout,
      modes: [{ id: "bfs", label: "BFS (queue)" }, { id: "dfs", label: "DFS (stack)" }],
      build(mode) {
        const steps = [];
        const nodeCls = {};
        const order = [];
        const visited = new Set([start]);
        let frontier = [start];
        nodeCls[start] = "active";
        steps.push({
          narration: `${mode.toUpperCase()} from ${hl(start)}. ${mode === "bfs" ? "Queue (FIFO)" : "Stack (LIFO)"} = [${start}].`,
          nodeCls: { ...nodeCls }, output: "",
          side: [{ title: mode === "bfs" ? "queue" : "stack", type: "stack", items: [start] }],
        });
        while (frontier.length) {
          const cur = mode === "bfs" ? frontier.shift() : frontier.pop();
          order.push(cur);
          nodeCls[cur] = "done";
          const active = new Set();
          adj[cur].forEach((nb) => active.add(cur + "-" + nb));
          steps.push({
            narration: `Take ${hl(cur)} from the ${mode === "bfs" ? "front of the queue" : "top of the stack"}; record it. Visit order: ${hl(order.join(" → "))}.`,
            nodeCls: { ...nodeCls }, activeEdges: active, output: order.join(" → "),
            side: [{ title: mode === "bfs" ? "queue" : "stack", type: "stack", items: [...frontier] }],
          });
          for (const nb of adj[cur]) {
            if (!visited.has(nb)) {
              visited.add(nb); frontier.push(nb);
              if (nodeCls[nb] !== "done") nodeCls[nb] = "visited";
            }
          }
          steps.push({
            narration: `Add unvisited neighbours of ${hl(cur)} → ${mode === "bfs" ? "queue" : "stack"} = [${frontier.join(", ")}].`,
            nodeCls: { ...nodeCls }, output: order.join(" → "),
            side: [{ title: mode === "bfs" ? "queue" : "stack", type: "stack", items: [...frontier] }],
          });
        }
        steps.push({ narration: `${mode.toUpperCase()} complete. Visit order: ${hl(order.join(" → "))}.`, nodeCls: { ...nodeCls }, output: order.join(" → ") });
        return steps;
      },
    };
  };

  // ---------- House Robber (rolling DP) ----------
  Visualizers.dpRolling = function (p) {
    const nums = p.nums;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const frame = (cls) => nums.map((v, idx) => ({ v, idx, cls: (cls && cls[idx]) || "" }));
        let prev2 = 0, prev1 = 0;
        steps.push({
          narration: `Rob houses for the most money, but never two adjacent. <code>dp[i] = max(skip dp[i-1], rob nums[i]+dp[i-2])</code>.`,
          cells: frame(), side: [{ title: "state", type: "kv", rows: [{ k: "prev1 (dp i-1)", v: 0 }, { k: "prev2 (dp i-2)", v: 0 }] }],
        });
        for (let i = 0; i < nums.length; i++) {
          const rob = nums[i] + prev2, skip = prev1, cur = Math.max(skip, rob);
          const cls = {}; cls[i] = "active";
          steps.push({
            narration: rob >= skip
              ? `House ${hl(i)} (\$${nums[i]}): <strong>rob</strong> → ${nums[i]}+${prev2} = ${hl(rob)} ≥ skip ${skip}. current = ${hl(cur)}.`
              : `House ${hl(i)} (\$${nums[i]}): <strong>skip</strong> → keep ${hl(skip)} > rob ${rob}. current = ${hl(cur)}.`,
            cells: frame(cls),
            side: [{ title: "decision", type: "kv", rows: [{ k: "rob = nums[i]+prev2", v: rob }, { k: "skip = prev1", v: skip }, { k: "current", v: cur }] }],
          });
          prev2 = prev1; prev1 = cur;
        }
        // reconstruct which houses were robbed
        const D = new Array(nums.length + 1).fill(0);
        for (let i = 1; i <= nums.length; i++) D[i] = Math.max(D[i - 1], nums[i - 1] + (i >= 2 ? D[i - 2] : 0));
        const robbed = {}; let i = nums.length;
        while (i > 0) { if (D[i] === D[i - 1]) i--; else { robbed[i - 1] = true; i -= 2; } }
        const cls = {}; nums.forEach((_, idx) => (cls[idx] = robbed[idx] ? "match" : "dim"));
        steps.push({ narration: `Maximum money = ${hl(prev1)} (robbed houses highlighted).`, cells: frame(cls), side: [{ title: "result", type: "kv", rows: [{ k: "answer", v: prev1 }] }] });
        return steps;
      },
    };
  };

  // ---------- Tree DFS family (depth / balanced / max-path / LCA) ----------
  Visualizers.treeDFS = function (p) {
    const layout = buildTreeLayout(p.tree);
    const variant = p.variant;
    let pNode = null, qNode = null;
    if (variant === "lca") {
      (function find(n) { if (!n) return; if (n.val === p.p && !pNode) pNode = n; if (n.val === p.q && !qNode) qNode = n; find(n.left); find(n.right); })(layout.root);
    }
    return {
      kind: "tree",
      layout,
      build() {
        const steps = [];
        const cls = {}, badge = {};
        const snap = (narration, extra) => steps.push(Object.assign({ narration, nodeCls: { ...cls }, nodeBadge: { ...badge } }, extra || {}));

        if (variant === "depth") {
          snap(`Maximum depth via post-order DFS: a node's height = 1 + the taller child's height.`);
          const dfs = (node) => {
            if (!node) return 0;
            cls[node.id] = "active"; snap(`Enter ${hl(node.val)} — solve children first.`);
            const l = dfs(node.left), r = dfs(node.right);
            const h = 1 + Math.max(l, r); badge[node.id] = "h=" + h; cls[node.id] = "done";
            snap(`${hl(node.val)}: height = 1 + max(L=${l}, R=${r}) = ${hl(h)}.`);
            return h;
          };
          const ans = dfs(layout.root);
          snap(`Maximum depth = ${hl(ans)}.`);
        } else if (variant === "balanced") {
          snap(`Balanced check: compute height bottom-up, returning <code>-1</code> the instant a subtree is unbalanced (short-circuit).`);
          const dfs = (node) => {
            if (!node) return 0;
            cls[node.id] = "active"; snap(`Enter ${hl(node.val)}.`);
            const l = dfs(node.left);
            if (l === -1) { cls[node.id] = "bad"; badge[node.id] = "✗"; snap(`Left of ${hl(node.val)} already unbalanced → propagate −1.`); return -1; }
            const r = dfs(node.right);
            if (r === -1) { cls[node.id] = "bad"; badge[node.id] = "✗"; snap(`Right of ${hl(node.val)} already unbalanced → propagate −1.`); return -1; }
            if (Math.abs(l - r) > 1) { cls[node.id] = "bad"; badge[node.id] = "✗ |" + l + "−" + r + "|>1"; snap(`${hl(node.val)} unbalanced: |${l}−${r}| > 1 → return −1.`); return -1; }
            const h = 1 + Math.max(l, r); badge[node.id] = "h=" + h; cls[node.id] = "done";
            snap(`${hl(node.val)} balanced: heights ${l} & ${r}. height = ${hl(h)}.`);
            return h;
          };
          const ok = dfs(layout.root) !== -1;
          snap(`Tree is ${hl(ok ? "balanced ✅" : "NOT balanced ✗")}.`);
        } else if (variant === "maxpath") {
          let best = -Infinity;
          snap(`Max path sum: at each node, the best path that <em>bends</em> here is node + max(0,leftGain) + max(0,rightGain). Negative branches are dropped.`);
          const gain = (node) => {
            if (!node) return 0;
            cls[node.id] = "active"; snap(`Enter ${hl(node.val)}.`);
            const lg = Math.max(gain(node.left), 0), rg = Math.max(gain(node.right), 0);
            const through = node.val + lg + rg; best = Math.max(best, through);
            const ret = node.val + Math.max(lg, rg);
            badge[node.id] = "↑" + ret; cls[node.id] = "done";
            snap(`${hl(node.val)}: through = ${node.val}+${lg}+${rg} = ${hl(through)}; best = ${hl(best)}. Return upward ${hl(ret)} (one side only).`,
              { side: [{ title: "global best", type: "kv", rows: [{ k: "max path sum", v: best }] }] });
            return ret;
          };
          gain(layout.root);
          snap(`Maximum path sum = ${hl(best)}.`, { side: [{ title: "result", type: "kv", rows: [{ k: "answer", v: best }] }] });
        } else if (variant === "lca") {
          snap(`Find LCA of ${hl(p.p)} and ${hl(p.q)}. Post-order DFS: each call reports whether a target lives below it.`);
          const dfs = (node) => {
            if (!node) return null;
            cls[node.id] = "visited"; snap(`Search under ${hl(node.val)}.`);
            if (node === pNode || node === qNode) { cls[node.id] = "target"; snap(`Found target ${hl(node.val)} → report it upward.`); return node; }
            const L = dfs(node.left), R = dfs(node.right);
            if (L && R) { cls[node.id] = "lca"; snap(`${hl(node.val)} sees a target on BOTH sides → it is the ${hl("LCA")}.`); return node; }
            return L || R;
          };
          const ans = dfs(layout.root);
          snap(`Lowest common ancestor = ${hl(ans ? ans.val : "—")}.`);
        }
        return steps;
      },
    };
  };

  // shared circular layout for graph adjacency (string ids)
  function circleLayout(ids) {
    const N = ids.length, R = 120, cx = 150, cy = 145;
    return ids.map((id, i) => ({
      id: String(id), label: String(id),
      x: cx + R * Math.cos((2 * Math.PI * i) / N - Math.PI / 2),
      y: cy + R * Math.sin((2 * Math.PI * i) / N - Math.PI / 2),
    }));
  }

  // ---------- Kahn's algorithm (directed cycle / topological sort) ----------
  Visualizers.kahn = function (p) {
    const v = p.vertices, adj = p.adj;
    const nodes = circleLayout([...Array(v).keys()]);
    const edges = [];
    for (let u = 0; u < v; u++) adj[u].forEach((w) => edges.push({ from: String(u), to: String(w) }));
    const layout = { nodes, edges, directed: true };
    return {
      kind: "graph",
      layout,
      build() {
        const steps = [];
        const indeg = new Array(v).fill(0);
        adj.forEach((list) => list.forEach((w) => indeg[w]++));
        const badge = () => { const b = {}; for (let i = 0; i < v; i++) b[String(i)] = "in=" + indeg[i]; return b; };
        const cls = {};
        let queue = [];
        for (let i = 0; i < v; i++) if (indeg[i] === 0) { queue.push(i); cls[String(i)] = "visited"; }
        let processed = 0; const order = [];
        const push = (narration, extra) => steps.push(Object.assign({ narration, nodeCls: { ...cls }, nodeBadge: badge(), output: order.join(" → "), outputLabel: "topo order", side: [{ title: "queue", type: "stack", items: [...queue] }] }, extra || {}));
        push(`Compute in-degrees, then enqueue every node with in-degree 0.`);
        while (queue.length) {
          const n = queue.shift(); processed++; order.push(n); cls[String(n)] = "done";
          const active = new Set(); adj[n].forEach((w) => active.add(String(n) + "-" + String(w)));
          push(`Process ${hl(n)} (in-degree 0). Remove it; decrement each neighbour's in-degree.`, { activeEdges: active });
          adj[n].forEach((w) => { indeg[w]--; if (indeg[w] === 0) { queue.push(w); if (cls[String(w)] !== "done") cls[String(w)] = "visited"; } });
          push(`In-degrees updated. Queue = [${queue.join(", ")}].`);
        }
        push(processed === v
          ? `Processed all ${hl(v)} nodes ⇒ a full topological order exists ⇒ ${hl("no cycle")}.`
          : `Only ${hl(processed)} of ${v} processed ⇒ the rest are stuck in a ${hl("cycle")}.`);
        return steps;
      },
    };
  };

  // ---------- Number of provinces (connected components on a matrix) ----------
  Visualizers.matrixComponents = function (p) {
    const M = p.matrix, n = M.length;
    const nodes = circleLayout([...Array(n).keys()]).map((nd) => ({ ...nd, label: "C" + nd.id }));
    const edges = [];
    for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) if (M[i][j] === 1) edges.push({ from: String(i), to: String(j) });
    const layout = { nodes, edges };
    return {
      kind: "graph",
      layout,
      build() {
        const steps = [];
        const visited = new Array(n).fill(false), cls = {};
        let provinces = 0;
        const push = (narration) => steps.push({ narration, nodeCls: { ...cls }, side: [{ title: "count", type: "kv", rows: [{ k: "provinces", v: provinces }] }] });
        push(`Each city is a node; a 1 in the matrix is an edge. Run DFS from each unvisited city — every launch is one province.`);
        for (let i = 0; i < n; i++) {
          if (!visited[i]) {
            provinces++;
            const stack = [i]; visited[i] = true; cls[String(i)] = "active";
            push(`City ${hl("C" + i)} unvisited → start province #${hl(provinces)}.`);
            while (stack.length) {
              const c = stack.pop(); cls[String(c)] = "done";
              for (let j = 0; j < n; j++) if (M[c][j] === 1 && !visited[j]) { visited[j] = true; cls[String(j)] = "visited"; stack.push(j); }
            }
            push(`Province #${provinces} fully explored.`);
          }
        }
        push(`Total provinces = ${hl(provinces)}.`);
        return steps;
      },
    };
  };

  // ---------- Detect cycle in an undirected graph (parent-aware DFS) ----------
  Visualizers.undirectedCycle = function (p) {
    const adj = p.graph, start = String(p.start);
    const ids = Object.keys(adj);
    const nodes = circleLayout(ids);
    const seen = new Set(), edges = [];
    ids.forEach((u) => adj[u].forEach((vv) => { const k = [u, String(vv)].sort().join("|"); if (!seen.has(k)) { seen.add(k); edges.push({ from: u, to: String(vv) }); } }));
    const layout = { nodes, edges };
    return {
      kind: "graph",
      layout,
      build() {
        const steps = [];
        const visited = {}, cls = {};
        const push = (narration, extra) => steps.push(Object.assign({ narration, nodeCls: { ...cls } }, extra || {}));
        push(`DFS while remembering each node's parent. A visited neighbour that ISN'T the parent means we looped back → a cycle.`);
        const stack = [[start, null]]; visited[start] = true; cls[start] = "visited";
        let found = false;
        while (stack.length && !found) {
          const [node, parent] = stack.pop();
          cls[node] = "done";
          push(`Visit ${hl(node)} (parent ${parent == null ? "none" : parent}).`, { side: [{ title: "parent", type: "kv", rows: [{ k: node, v: parent == null ? "—" : parent }] }] });
          for (const nbRaw of adj[node]) {
            const nb = String(nbRaw);
            if (!visited[nb]) { visited[nb] = true; cls[nb] = "visited"; stack.push([nb, node]); }
            else if (nb !== parent) { cls[node] = "bad"; cls[nb] = "bad"; push(`${hl(nb)} is already visited and isn't ${node}'s parent → ${hl("cycle found!")}`, { activeEdges: new Set([node + "-" + nb]) }); found = true; break; }
          }
        }
        if (!found) push(`No back-edge to a non-parent was found → ${hl("no cycle")}.`);
        return steps;
      },
    };
  };

  // ---------- Clone graph (BFS with a value→clone map) ----------
  Visualizers.cloneBFS = function (p) {
    const adj = p.graph, start = String(p.start);
    const ids = Object.keys(adj);
    const nodes = circleLayout(ids);
    const seen = new Set(), edges = [];
    ids.forEach((u) => adj[u].forEach((vv) => { const k = [u, String(vv)].sort().join("|"); if (!seen.has(k)) { seen.add(k); edges.push({ from: u, to: String(vv) }); } }));
    const layout = { nodes, edges };
    return {
      kind: "graph",
      layout,
      build() {
        const steps = [];
        const cls = {}, cloned = {};
        const mapRows = () => Object.keys(cloned).map((k) => ({ k: k, v: "clone(" + k + ")" }));
        const push = (narration, extra) => steps.push(Object.assign({ narration, nodeCls: { ...cls }, side: [{ title: "clone map", type: "kv", rows: mapRows() }] }, extra || {}));
        const queue = [start]; cloned[start] = true; cls[start] = "visited";
        push(`BFS the original graph with a map <code>value → clone</code>. Seeing a node for the first time creates its clone.`);
        while (queue.length) {
          const cur = queue.shift(); cls[cur] = "done";
          const active = new Set(); adj[cur].forEach((nb) => active.add(cur + "-" + String(nb)));
          push(`Process ${hl(cur)}; wire clone(${cur})'s neighbour list from the map.`, { activeEdges: active });
          for (const nbRaw of adj[cur]) {
            const nb = String(nbRaw);
            if (!cloned[nb]) { cloned[nb] = true; cls[nb] = "visited"; queue.push(nb); push(`First time seeing ${hl(nb)} → create clone(${nb}) and enqueue it.`); }
          }
        }
        push(`Every node copied and every edge re-linked → deep copy complete.`);
        return steps;
      },
    };
  };

  // ---------- Search in rotated sorted array ----------
  Visualizers.rotatedSearch = function (p) {
    const nums = p.nums, target = p.target;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const frame = (lo, hi, mid, cls) => nums.map((v, i) => ({
          v, idx: i,
          cls: (cls && cls[i]) || (i < lo || i > hi ? "dim" : i === mid ? "active" : ""),
          badge: i === mid ? "mid" : i === lo ? "L" : i === hi ? "R" : null,
        }));
        let lo = 0, hi = nums.length - 1;
        steps.push({ narration: `Search ${hl(target)} in a rotated sorted array. Key trick: at each mid, one half is always still sorted.`, cells: frame(lo, hi, -1) });
        while (lo <= hi) {
          const mid = lo + ((hi - lo) >> 1);
          steps.push({ narration: `mid = ${hl(mid)} → ${hl(nums[mid])}.`, cells: frame(lo, hi, mid), side: [{ title: "range", type: "kv", rows: [{ k: "low", v: lo }, { k: "mid", v: mid }, { k: "high", v: hi }] }] });
          if (nums[mid] === target) { const cls = {}; cls[mid] = "match"; steps.push({ narration: `✅ Found ${target} at index ${hl(mid)}.`, cells: frame(lo, hi, mid, cls) }); return steps; }
          if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) { steps.push({ narration: `Left half [${lo}..${mid}] is sorted and contains ${target} → search left.`, cells: frame(lo, hi, mid) }); hi = mid - 1; }
            else { steps.push({ narration: `Left half is sorted but ${target} isn't in it → search right.`, cells: frame(lo, hi, mid) }); lo = mid + 1; }
          } else {
            if (nums[mid] < target && target <= nums[hi]) { steps.push({ narration: `Right half [${mid}..${hi}] is sorted and contains ${target} → search right.`, cells: frame(lo, hi, mid) }); lo = mid + 1; }
            else { steps.push({ narration: `Right half is sorted but ${target} isn't in it → search left.`, cells: frame(lo, hi, mid) }); hi = mid - 1; }
          }
        }
        steps.push({ narration: `Range empty — ${target} is not present (return −1).`, cells: nums.map((v, i) => ({ v, idx: i, cls: "dim" })) });
        return steps;
      },
    };
  };

  // ---------- Prefix sums (range-sum in O(1)) ----------
  Visualizers.prefixSum = function (p) {
    const nums = p.nums, L = p.queryL, R = p.queryR;
    return {
      kind: "2d",
      build() {
        const n = nums.length;
        const prefix = new Array(n).fill(null);
        const snap = (cls) => {
          cls = cls || {};
          const header = [{ v: "idx", cls: "water" }];
          for (let i = 0; i < n; i++) header.push({ v: i, cls: "land" + (cls["h" + i] ? " active" : "") });
          const r1 = [{ v: "nums", cls: "land" }];
          for (let i = 0; i < n; i++) r1.push({ v: nums[i], cls: cls["n" + i] || "" });
          const r2 = [{ v: "prefix", cls: "land" }];
          for (let i = 0; i < n; i++) r2.push({ v: prefix[i] == null ? "·" : prefix[i], cls: cls["p" + i] || (prefix[i] == null ? "water" : "") });
          return [header, r1, r2];
        };
        const steps = [];
        steps.push({
          narration: `A <strong>prefix-sum</strong> array answers any range-sum in O(1). Define <code>prefix[i] = nums[0] + … + nums[i]</code>.`,
          grid: snap(),
        });
        let run = 0;
        for (let i = 0; i < n; i++) {
          run += nums[i]; prefix[i] = run;
          const cls = {}; cls["n" + i] = "active"; cls["p" + i] = "fill-match";
          if (i > 0) cls["p" + (i - 1)] = "window";
          steps.push({
            narration: `prefix[${hl(i)}] = ${i > 0 ? "prefix[" + (i - 1) + "]" : "0"} + nums[${i}] = ${i > 0 ? prefix[i - 1] : 0} + ${nums[i]} = ${hl(run)}.`,
            grid: snap(cls),
          });
        }
        const before = L > 0 ? prefix[L - 1] : 0;
        const ans = prefix[R] - before;
        const cls = {};
        cls["p" + R] = "active";
        if (L > 0) cls["p" + (L - 1)] = "bad";
        for (let i = L; i <= R; i++) cls["n" + i] = "window";
        steps.push({
          narration: `Range sum of [${hl(L)}..${hl(R)}] = prefix[${R}] − prefix[${L > 0 ? L - 1 : "∅"}] = ${prefix[R]} − ${before} = ${hl(ans)}. One subtraction — no re-scanning.`,
          grid: snap(cls),
          side: [{ title: "O(1) query", type: "kv", rows: [{ k: `sum[${L}..${R}]`, v: ans }] }],
        });
        return steps;
      },
    };
  };

  // ---------- Coin change (1D bottom-up tabulation) ----------
  Visualizers.coinChange = function (p) {
    const coins = p.coins, amount = p.amount;
    return {
      kind: "2d",
      build() {
        const INF = Infinity;
        const dp = new Array(amount + 1).fill(INF); dp[0] = 0;
        const show = (v) => (v === INF ? "∞" : v);
        const snap = (cls) => {
          cls = cls || {};
          const header = [{ v: "amount", cls: "water" }];
          for (let a = 0; a <= amount; a++) header.push({ v: a, cls: "land" + (cls["h" + a] ? " active" : "") });
          const row = [{ v: "min coins", cls: "land" }];
          for (let a = 0; a <= amount; a++) row.push({ v: show(dp[a]), cls: cls["d" + a] || (dp[a] === INF ? "water" : "") });
          return [header, row];
        };
        const steps = [];
        steps.push({
          narration: `<strong>Coin change</strong>: fewest coins to make each amount. Build a table bottom-up. <code>dp[0]=0</code>; the rest start at ∞ (unreachable).`,
          grid: snap(), side: [{ title: "coins", type: "kv", rows: coins.map((c) => ({ k: "coin", v: c })) }],
        });
        for (let a = 1; a <= amount; a++) {
          let used = null;
          for (const c of coins) {
            if (c <= a && dp[a - c] + 1 < dp[a]) { dp[a] = dp[a - c] + 1; used = c; }
          }
          const cls = {}; cls["d" + a] = dp[a] === INF ? "active" : "fill-match";
          if (used != null) cls["d" + (a - used)] = "active";
          steps.push({
            narration: dp[a] === INF
              ? `Amount ${hl(a)}: no coin fits a reachable smaller amount → stays ∞.`
              : `Amount ${hl(a)}: take coin ${hl(used)} on top of dp[${a - used}] = 1 + ${dp[a - used]} = ${hl(dp[a])}.`,
            grid: snap(cls),
          });
        }
        steps.push({
          narration: dp[amount] === INF
            ? `Amount ${hl(amount)} can't be formed → answer is −1.`
            : `Fewest coins to make ${hl(amount)} = ${hl(dp[amount])} (read straight off the table).`,
          grid: snap({ ["d" + amount]: "fill-match" }),
          side: [{ title: "result", type: "kv", rows: [{ k: "min coins", v: dp[amount] === INF ? "-1" : dp[amount] }] }],
        });
        return steps;
      },
    };
  };

  // ---------- BST search (descend left/right by comparison) ----------
  Visualizers.bstSearch = function (p) {
    const layout = buildTreeLayout(p.tree);
    const target = p.target;
    return {
      kind: "tree",
      layout,
      build() {
        const steps = [];
        const cls = {};
        const snap = (narration) => steps.push({ narration, nodeCls: { ...cls } });
        snap(`Search for ${hl(target)} in a <strong>BST</strong>. At each node compare and go left (smaller) or right (larger) — each step discards half the remaining tree.`);
        let node = layout.root;
        while (node) {
          cls[node.id] = "active";
          if (target === node.val) {
            cls[node.id] = "done";
            snap(`${hl(node.val)} == ${hl(target)} ✅ — found it in O(height) steps.`);
            return steps;
          }
          if (target < node.val) {
            snap(`${hl(target)} &lt; ${hl(node.val)} → go LEFT (everything to the right is even larger).`);
            cls[node.id] = "visited";
            node = node.left;
          } else {
            snap(`${hl(target)} &gt; ${hl(node.val)} → go RIGHT (everything to the left is even smaller).`);
            cls[node.id] = "visited";
            node = node.right;
          }
        }
        snap(`Fell off the tree (reached an empty child) → ${hl(target)} is ${hl("not present")}.`);
        return steps;
      },
    };
  };

  // ---------- Dijkstra (weighted shortest path with a min-heap) ----------
  Visualizers.dijkstra = function (p) {
    const ids = p.nodes.map(String);
    const nodes = circleLayout(ids);
    const adj = {}; ids.forEach((id) => (adj[id] = []));
    const edges = [];
    p.edges.forEach(([u, v, w]) => {
      const a = String(u), b = String(v);
      edges.push({ from: a, to: b, weight: w });
      adj[a].push([b, w]);
      if (!p.directed) adj[b].push([a, w]);
    });
    const layout = { nodes, edges, directed: !!p.directed };
    const start = String(p.start);
    return {
      kind: "graph",
      layout,
      build() {
        const steps = [];
        const INF = Infinity;
        const dist = {}; ids.forEach((id) => (dist[id] = INF)); dist[start] = 0;
        const done = {}, cls = {};
        const badge = () => { const b = {}; ids.forEach((id) => (b[id] = dist[id] === INF ? "∞" : dist[id])); return b; };
        const distRows = () => ids.map((id) => ({ k: id, v: dist[id] === INF ? "∞" : dist[id] }));
        let heap = [[0, start]];
        const heapItems = () => heap.slice().sort((a, b) => a[0] - b[0]).map(([d, n]) => n + "(" + d + ")");
        const push = (narration, extra) => steps.push(Object.assign(
          { narration, nodeCls: { ...cls }, nodeBadge: badge(),
            side: [{ title: "distance", type: "kv", rows: distRows() }, { title: "min-heap", type: "stack", items: heapItems() }] }, extra || {}));
        cls[start] = "visited";
        push(`Dijkstra from ${hl(start)}: <code>dist[${start}]=0</code>, all others ∞. A <strong>min-heap</strong> always hands us the closest unfinished node.`);
        while (heap.length) {
          heap.sort((a, b) => a[0] - b[0]);
          const [d, u] = heap.shift();
          if (done[u] || d > dist[u]) continue;     // stale entry — lazy deletion
          done[u] = true; cls[u] = "done";
          const active = new Set(); adj[u].forEach(([v]) => active.add(u + "-" + v));
          push(`Pop ${hl(u)} (dist ${hl(d)}) — the smallest in the heap, so ${hl("dist[" + u + "] is now final")}.`, { activeEdges: active });
          for (const [v, w] of adj[u]) {
            if (done[v]) continue;
            const nd = d + w;
            if (nd < dist[v]) {
              dist[v] = nd; heap.push([nd, v]); if (cls[v] !== "done") cls[v] = "visited";
              push(`Relax ${u}→${v} (weight ${w}): ${d}+${w} = ${hl(nd)} beats the old ${hl(v)} distance → update and push.`);
            }
          }
        }
        push(`Heap empty — every reachable node is finalized. Each node's badge is its shortest distance from ${hl(start)}.`);
        return steps;
      },
    };
  };

  // ---------- Bipartite check (BFS 2-coloring) ----------
  Visualizers.bipartite = function (p) {
    const adj = p.graph, ids = Object.keys(adj);
    const nodes = circleLayout(ids);
    const seen = new Set(), edges = [];
    ids.forEach((u) => adj[u].forEach((vv) => { const k = [u, String(vv)].sort().join("|"); if (!seen.has(k)) { seen.add(k); edges.push({ from: u, to: String(vv) }); } }));
    const layout = { nodes, edges };
    return {
      kind: "graph",
      layout,
      build() {
        const steps = [];
        const color = {}, cls = {};
        const name = (c) => (c === 0 ? "color A" : "color B");
        const paint = (c) => (c === 0 ? "visited" : "active");
        const push = (narration, extra) => steps.push(Object.assign({ narration, nodeCls: { ...cls } }, extra || {}));
        push(`Bipartite = can we 2-color the graph so no edge joins same-colored nodes? Color a start node, force neighbours the opposite color. A same-color edge ⇒ not bipartite.`);
        let ok = true;
        for (const start of ids) {
          if (color[start] !== undefined) continue;
          color[start] = 0; cls[start] = paint(0);
          const queue = [start];
          push(`New component: paint ${hl(start)} with ${hl(name(0))}.`);
          while (queue.length && ok) {
            const u = queue.shift();
            for (const vRaw of adj[u]) {
              const v = String(vRaw);
              if (color[v] === undefined) {
                color[v] = 1 - color[u]; cls[v] = paint(color[v]); queue.push(v);
                push(`${hl(v)} is uncolored → give it ${hl(name(color[v]))} (opposite of ${u}).`);
              } else if (color[v] === color[u]) {
                cls[u] = "bad"; cls[v] = "bad";
                push(`Edge ${u}–${v} joins two ${hl(name(color[v]))} nodes → ${hl("NOT bipartite")}.`, { activeEdges: new Set([u + "-" + v]) });
                ok = false; break;
              }
            }
          }
          if (!ok) break;
        }
        if (ok) push(`No conflicting edge anywhere → the graph ${hl("IS bipartite")}: two independent groups (A and B).`);
        return steps;
      },
    };
  };

  // ---------- Heap operations: insert (sift-up) & extract-min (sift-down) ----------
  Visualizers.heapOps = function (p) {
    const startHeap = p.heap, insertVal = p.value;
    return {
      kind: "1d",
      modes: [{ id: "insert", label: "Insert " + insertVal }, { id: "extract", label: "Extract-Min" }],
      build(mode) {
        const steps = [];
        const heap = [...startHeap];
        const frame = (cls, badge) => heap.map((v, i) => ({ v, idx: i, cls: (cls && cls[i]) || "", badge: (badge && badge[i]) || null }));
        if (mode === "insert") {
          steps.push({ narration: `A min-heap lives in an array. Parent of <code>i</code> is <code>(i-1)//2</code>; children are <code>2i+1</code> and <code>2i+2</code>. We'll insert ${hl(insertVal)}.`, cells: frame() });
          heap.push(insertVal);
          let i = heap.length - 1;
          steps.push({ narration: `Drop ${hl(insertVal)} at the end (index ${hl(i)}) so the tree stays complete, then <strong>sift up</strong>.`, cells: frame({ [i]: "active" }) });
          while (i > 0) {
            const par = (i - 1) >> 1;
            steps.push({ narration: `Compare with parent at index ${hl(par)} (value ${hl(heap[par])}).`, cells: frame({ [i]: "active", [par]: "window" }) });
            if (heap[i] < heap[par]) {
              [heap[i], heap[par]] = [heap[par], heap[i]];
              steps.push({ narration: `${hl(heap[par])} &lt; ${hl(heap[i])} → swap the smaller value up.`, cells: frame({ [i]: "match", [par]: "match" }) });
              i = par;
            } else {
              steps.push({ narration: `${hl(heap[i])} ≥ parent ${hl(heap[par])} → heap property holds. Stop.`, cells: frame({ [i]: "match" }) });
              break;
            }
          }
          steps.push({ narration: `Inserted. Sift-up touches at most one node per level → ${hl("O(log n)")}.`, cells: frame() });
        } else {
          steps.push({ narration: `Extract-min returns the root ${hl(heap[0])} (always the smallest). Remove it, move the LAST element to the root, then <strong>sift down</strong>.`, cells: frame({ 0: "active" }) });
          const minVal = heap[0], last = heap.pop();
          if (heap.length) {
            heap[0] = last;
            steps.push({ narration: `Last value ${hl(last)} jumps to the root to keep the tree complete. Now sink it.`, cells: frame({ 0: "active" }) });
            let i = 0; const n = heap.length;
            while (true) {
              let smallest = i; const l = 2 * i + 1, r = 2 * i + 2;
              const cls = { [i]: "active" }; if (l < n) cls[l] = "window"; if (r < n) cls[r] = "window";
              steps.push({ narration: `Look at ${hl(heap[i])} and its child${r < n ? "ren" : ""} ${l < n ? heap[l] : ""}${r < n ? " and " + heap[r] : ""}.`, cells: frame(cls) });
              if (l < n && heap[l] < heap[smallest]) smallest = l;
              if (r < n && heap[r] < heap[smallest]) smallest = r;
              if (smallest === i) { steps.push({ narration: `${hl(heap[i])} is ≤ both children → done sinking.`, cells: frame({ [i]: "match" }) }); break; }
              [heap[i], heap[smallest]] = [heap[smallest], heap[i]];
              steps.push({ narration: `Swap with the smaller child ${hl(heap[i])}.`, cells: frame({ [i]: "match", [smallest]: "match" }) });
              i = smallest;
            }
          }
          steps.push({ narration: `Returned ${hl(minVal)}. Extract-min is ${hl("O(log n)")}; the new root is the next smallest.`, cells: frame() });
        }
        return steps;
      },
    };
  };

  // ---------- Build-heap (heapify) in O(n) ----------
  Visualizers.heapify = function (p) {
    return {
      kind: "1d",
      build() {
        const heap = [...p.array];
        const n = heap.length;
        const frame = (cls) => heap.map((v, i) => ({ v, idx: i, cls: (cls && cls[i]) || "" }));
        const steps = [];
        steps.push({ narration: `Turn a raw array into a min-heap. Naively pushing n times is O(n log n); <strong>heapify</strong> sinks each node bottom-up in only ${hl("O(n)")}.`, cells: frame() });
        const lastParent = (n >> 1) - 1;
        steps.push({ narration: `Leaves (indices ${hl(lastParent + 1)}…${hl(n - 1)}) are already valid heaps. Start sift-down at the last parent, index ${hl(lastParent)}, and walk to the root.`, cells: frame(heap.reduce((a, _v, i) => { a[i] = i > lastParent ? "dim" : ""; return a; }, {})) });
        for (let start = lastParent; start >= 0; start--) {
          let i = start;
          steps.push({ narration: `Sift down index ${hl(start)} (value ${hl(heap[start])}).`, cells: frame({ [start]: "active" }) });
          while (true) {
            let smallest = i; const l = 2 * i + 1, r = 2 * i + 2;
            if (l < n && heap[l] < heap[smallest]) smallest = l;
            if (r < n && heap[r] < heap[smallest]) smallest = r;
            if (smallest === i) break;
            [heap[i], heap[smallest]] = [heap[smallest], heap[i]];
            steps.push({ narration: `Swap ${hl(heap[smallest])} with smaller child ${hl(heap[i])}.`, cells: frame({ [i]: "match", [smallest]: "match" }) });
            i = smallest;
          }
        }
        steps.push({ narration: `Every node now satisfies the heap property → valid min-heap, root = ${hl(heap[0])}.`, cells: frame({ 0: "active" }) });
        return steps;
      },
    };
  };

  // ---------- Top-K with a size-K min-heap ----------
  Visualizers.topKHeap = function (p) {
    const nums = p.nums, k = p.k;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const heap = [];                         // min-heap of the k largest so far
        const hpush = (x) => { heap.push(x); let i = heap.length - 1; while (i > 0) { const pa = (i - 1) >> 1; if (heap[i] < heap[pa]) { [heap[i], heap[pa]] = [heap[pa], heap[i]]; i = pa; } else break; } };
        const hpop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let i = 0, n = heap.length; while (true) { let s = i, l = 2 * i + 1, r = 2 * i + 2; if (l < n && heap[l] < heap[s]) s = l; if (r < n && heap[r] < heap[s]) s = r; if (s === i) break;[heap[i], heap[s]] = [heap[s], heap[i]]; i = s; } } return top; };
        const frame = (cur) => nums.map((v, i) => ({ v, idx: i, cls: i === cur ? "active" : i < cur ? "dim" : "" }));
        const heapPanel = () => [{ title: `min-heap (≤ ${k})`, type: "kv", rows: heap.length ? [{ k: "root (smallest)", v: heap[0] }, { k: "contents", v: "[" + heap.join(", ") + "]" }] : [{ k: "contents", v: "empty" }] }];
        steps.push({ narration: `Find the ${hl(k + " largest")} values. Keep a <strong>min-heap of size ${k}</strong>: its root is the smallest of the current top-${k}, so it's the easiest to evict.`, cells: frame(-1), side: heapPanel() });
        for (let i = 0; i < nums.length; i++) {
          hpush(nums[i]);
          steps.push({ narration: `See ${hl(nums[i])} → push it onto the heap.`, cells: frame(i), side: heapPanel() });
          if (heap.length > k) {
            const evicted = hpop();
            steps.push({ narration: `Heap exceeded ${hl(k)} → pop the smallest (${hl(evicted)}). Only the ${k} largest survive.`, cells: frame(i), side: heapPanel() });
          }
        }
        steps.push({ narration: `Stream done. The heap holds the ${hl(k)} largest; its root ${hl(heap[0])} is the ${hl("k-th largest")} (k=${k}). Cost ${hl("O(n log k)")} — far cheaper than sorting when k ≪ n.`, cells: frame(nums.length), side: heapPanel() });
        return steps;
      },
    };
  };

  // ---------- Running median with two heaps ----------
  Visualizers.twoHeaps = function (p) {
    const nums = p.nums;
    return {
      kind: "1d",
      build() {
        const steps = [];
        const low = [];   // max-heap (lower half) — top = largest
        const high = [];  // min-heap (upper half) — top = smallest
        const push = (heap, x, cmp) => { heap.push(x); let i = heap.length - 1; while (i > 0) { const pa = (i - 1) >> 1; if (cmp(heap[i], heap[pa]) < 0) { [heap[i], heap[pa]] = [heap[pa], heap[i]]; i = pa; } else break; } };
        const pop = (heap, cmp) => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let i = 0, n = heap.length; while (true) { let s = i, l = 2 * i + 1, r = 2 * i + 2; if (l < n && cmp(heap[l], heap[s]) < 0) s = l; if (r < n && cmp(heap[r], heap[s]) < 0) s = r; if (s === i) break;[heap[i], heap[s]] = [heap[s], heap[i]]; i = s; } } return top; };
        const MAX = (a, b) => b - a, MIN = (a, b) => a - b;     // comparators
        const median = () => low.length > high.length ? low[0] : (low[0] + high[0]) / 2;
        const frame = (cur) => nums.map((v, i) => ({ v, idx: i, cls: i === cur ? "active" : i < cur ? "dim" : "" }));
        const panels = () => [
          { title: "max-heap (low half)", type: "kv", rows: [{ k: "top = largest low", v: low.length ? low[0] : "—" }, { k: "size", v: low.length }] },
          { title: "min-heap (high half)", type: "kv", rows: [{ k: "top = smallest high", v: high.length ? high[0] : "—" }, { k: "size", v: high.length }] },
        ];
        steps.push({ narration: `Running median: keep the smaller half in a <strong>max-heap</strong> and the larger half in a <strong>min-heap</strong>. The two tops straddle the middle, so the median is O(1) to read.`, cells: frame(-1), side: panels() });
        for (let i = 0; i < nums.length; i++) {
          const x = nums[i];
          if (!low.length || x <= low[0]) push(low, x, MAX); else push(high, x, MIN);
          steps.push({ narration: `Add ${hl(x)} → goes to the ${low.length && x <= (low.length ? low[0] : Infinity) ? "low" : "high"} half.`, cells: frame(i), side: panels() });
          // rebalance so sizes differ by at most 1, low ≥ high
          if (low.length > high.length + 1) { const m = pop(low, MAX); push(high, m, MIN); steps.push({ narration: `Low half too big → move its max ${hl(m)} to the high half.`, cells: frame(i), side: panels() }); }
          else if (high.length > low.length) { const m = pop(high, MIN); push(low, m, MAX); steps.push({ narration: `High half too big → move its min ${hl(m)} to the low half.`, cells: frame(i), side: panels() }); }
          steps.push({ narration: `Median so far = ${hl(median())} (from the two heap tops).`, cells: frame(i), side: panels() });
        }
        steps.push({ narration: `Each insert is ${hl("O(log n)")}; the median is always the ${hl("O(1)")} read across the two tops.`, cells: frame(nums.length), side: panels() });
        return steps;
      },
    };
  };

  // =========================================================================
  // PLAYER
  // =========================================================================
  function mountVisualizer(container, type, params) {
    const gen = Visualizers[type];
    if (!gen) { container.innerHTML = `<div class="empty-state">No visualizer for "${type}".</div>`; return; }
    const inst = gen(params);

    let mode = inst.modes ? inst.modes[0].id : null;
    let steps = inst.build(mode);
    let idx = 0, timer = null, speed = 900;

    const root = el("div", "viz");
    const head = el("div", "viz-head");
    head.appendChild(el("div", "t", `<span class="ico">▶</span>Visualization`));
    if (inst.modes) {
      const modeWrap = el("div");
      inst.modes.forEach((m) => {
        const b = el("button", "viz-speed", m.label);
        b.style.marginLeft = "6px";
        b.onclick = () => {
          mode = m.id; idx = 0; steps = inst.build(mode);
          [...modeWrap.children].forEach((c) => (c.style.borderColor = ""));
          b.style.borderColor = "var(--accent)";
          stop(); draw();
        };
        if (m.id === mode) b.style.borderColor = "var(--accent)";
        modeWrap.appendChild(b);
      });
      head.appendChild(modeWrap);
    }
    root.appendChild(head);

    const stage = el("div", "viz-stage");
    const narration = el("div", "viz-narration");
    root.appendChild(stage);

    const controls = el("div", "viz-controls");
    const btnRestart = el("button", "viz-btn", "⟲");
    const btnPrev = el("button", "viz-btn", "‹");
    const btnPlay = el("button", "viz-btn primary", "▶ Play");
    const btnNext = el("button", "viz-btn", "›");
    const slider = el("input", "viz-slider"); slider.type = "range"; slider.min = 0;
    const stepLabel = el("div", "viz-step-label");
    const speedSel = el("select", "viz-speed");
    [["Slow", 1500], ["Normal", 900], ["Fast", 450]].forEach(([l, v]) => {
      const o = el("option", null, l); o.value = v; if (v === speed) o.selected = true; speedSel.appendChild(o);
    });
    controls.append(btnRestart, btnPrev, btnPlay, btnNext, slider, speedSel, stepLabel);
    root.appendChild(narration);
    root.appendChild(controls);
    container.appendChild(root);

    function draw() {
      const step = steps[idx];
      if (inst.kind === "1d") render1D(stage, step);
      else if (inst.kind === "2d") render2D(stage, step);
      else renderGraphLike(stage, inst.layout, step);
      narration.innerHTML = step.narration || "";
      slider.max = steps.length - 1;
      slider.value = idx;
      stepLabel.textContent = `Step ${idx + 1} / ${steps.length}`;
      btnPrev.disabled = idx === 0;
      btnNext.disabled = idx === steps.length - 1;
    }
    function next() { if (idx < steps.length - 1) { idx++; draw(); } else stop(); }
    function prev() { if (idx > 0) { idx--; draw(); } }
    function stop() { if (timer) { clearInterval(timer); timer = null; } btnPlay.innerHTML = "▶ Play"; }
    function play() {
      if (timer) { stop(); return; }
      if (idx === steps.length - 1) { idx = 0; draw(); }
      btnPlay.innerHTML = "❚❚ Pause";
      timer = setInterval(() => { if (idx >= steps.length - 1) stop(); else next(); }, speed);
    }

    btnPlay.onclick = play;
    btnNext.onclick = () => { stop(); next(); };
    btnPrev.onclick = () => { stop(); prev(); };
    btnRestart.onclick = () => { stop(); idx = 0; draw(); };
    slider.oninput = () => { stop(); idx = +slider.value; draw(); };
    speedSel.onchange = () => { speed = +speedSel.value; if (timer) { stop(); play(); } };

    draw();
    return { destroy: stop };
  }

  window.mountVisualizer = mountVisualizer;
  window.Visualizers = Visualizers;
})();
