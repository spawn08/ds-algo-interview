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
    const pad = 36, r = 21;
    const xs = layout.nodes.map((n) => n.x), ys = layout.nodes.map((n) => n.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const w = maxX - minX + pad * 2, h = maxY - minY + pad * 2;
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "viz-svg");
    svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
    const ox = pad - minX, oy = pad - minY;
    const active = step.activeEdges || new Set();

    layout.edges.forEach((e) => {
      const a = layout.nodes.find((n) => n.id === e.from);
      const b = layout.nodes.find((n) => n.id === e.to);
      const line = document.createElementNS(svg.namespaceURI, "line");
      const isActive = active.has(e.from + "-" + e.to) || active.has(e.to + "-" + e.from);
      line.setAttribute("class", "edge-line" + (isActive ? " active" : ""));
      line.setAttribute("x1", a.x + ox); line.setAttribute("y1", a.y + oy);
      line.setAttribute("x2", b.x + ox); line.setAttribute("y2", b.y + oy);
      svg.appendChild(line);
    });
    layout.nodes.forEach((n) => {
      const g = document.createElementNS(svg.namespaceURI, "g");
      const c = document.createElementNS(svg.namespaceURI, "circle");
      c.setAttribute("class", "node-circle " + ((step.nodeCls && step.nodeCls[n.id]) || ""));
      c.setAttribute("cx", n.x + ox); c.setAttribute("cy", n.y + oy); c.setAttribute("r", r);
      const t = document.createElementNS(svg.namespaceURI, "text");
      t.setAttribute("class", "node-label");
      t.setAttribute("x", n.x + ox); t.setAttribute("y", n.y + oy + 1);
      t.textContent = n.label;
      g.appendChild(c); g.appendChild(t);
      svg.appendChild(g);
    });
    stage.appendChild(svg);

    if (step.output != null) {
      stage.appendChild(el("div", "output-strip",
        `<span class="muted">visited:</span> ${step.output || "<span class='muted'>—</span>"}`));
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
