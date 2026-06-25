"""Small local labeling app for noun-smell calibration data."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Noun Smell Review</title>
  <style>
    :root { font-family: system-ui, sans-serif; color: #111; background: #fff; line-height: 1.5; }
    body { margin: 0; }
    header { position: sticky; top: 0; background: #fff; border-bottom: 1px solid #ddd; padding: 8px 14px; z-index: 2; }
    main { max-width: 760px; margin: 0 auto; padding: 12px 14px 32px; }
    .toolbar { display: flex; gap: 10px; align-items: baseline; justify-content: space-between; }
    .toolbar strong { font-size: 17px; }
    .muted { color: #777; }
    button, select, textarea { font: inherit; }

    .card { background: #fff; border: 1px solid #e6e6e6; border-radius: 12px; padding: 16px 16px 14px; margin-top: 12px; }

    /* The whole review as one inline flow:
       before  [gap]  original -> replacement  [gap]  after */
    .ctx { margin: 0; font-size: 20px; line-height: 1.65; }
    .ctx-side { color: #6a6a6a; }
    .gap-lg { display: inline-block; width: 1.5em; }
    .gap-sm { display: inline-block; width: 0.8em; }
    .orig { color: #1b1b1f; }
    .arrow { color: #1f6feb; font-weight: 800; padding: 0 3px; }
    .repl { color: #15803d; font-weight: 600; }
    mark { background: #ffdf3d; padding: 0 2px; border-radius: 3px; }
    .ctx a { color: #1f6feb; text-decoration: underline; text-decoration-thickness: 1px; overflow-wrap: anywhere; }
    .ctx code, code { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.86em; background: #eef0f3; padding: 1px 4px; border-radius: 4px; }

    /* Three square decision buttons */
    .decide { display: flex; gap: 12px; margin-top: 20px; }
    .decide button {
      flex: 0 0 auto; width: 84px; height: 84px; border-radius: 14px;
      border: 2px solid #cfcfcf; background: #fff; cursor: pointer;
      font-size: 15px; font-weight: 700; line-height: 1.15; padding: 4px;
    }
    .decide .good { background: #e7f6e9; border-color: #8fce98; color: #15803d; }
    .decide .bad  { background: #fbe4e4; border-color: #df9b9b; color: #b91c1c; }
    .decide .skip { background: #f0f0f0; border-color: #cbcbcb; color: #444; }
    .decide button.sel { box-shadow: 0 0 0 4px #1f6feb55; border-color: #1f6feb; }

    /* Agent verdict (small, secondary) */
    .agent { margin: 16px 0 0; font-size: 14px; color: #444; }
    .decision { display: inline-block; border-radius: 999px; padding: 2px 9px; border: 1px solid #ccc; background: #f7f7f7; font-weight: 650; font-size: 13px; }
    .decision.bad  { background: #fde9e9; border-color: #e0a3a3; color: #b91c1c; }
    .decision.keep { background: #e7f6e9; border-color: #9bd0a3; color: #15803d; }

    /* Collapsible note */
    details.note-wrap { margin-top: 14px; }
    details.note-wrap summary { cursor: pointer; color: #1f6feb; font-size: 14px; font-weight: 600; list-style: none; }
    details.note-wrap summary::-webkit-details-marker { display: none; }
    details.note-wrap summary::before { content: "+ "; }
    details.note-wrap[open] summary::before { content: "– "; }
    textarea { width: 100%; min-height: 56px; box-sizing: border-box; margin-top: 8px; border: 1px solid #c9c9c9; border-radius: 8px; padding: 9px; font-size: 15px; }

    .nav { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 16px; }
    .nav button { border: 1px solid #cfcfcf; background: #fff; padding: 11px 0; border-radius: 10px; cursor: pointer; font-size: 15px; }
    .meta { color: #999; font-size: 12px; display: flex; gap: 6px; flex-wrap: wrap; margin-top: 14px; }
    .pill { border: 1px solid #e6e6e6; border-radius: 999px; padding: 2px 9px; background: #fafafa; }
    .path { overflow-wrap: anywhere; }

    .filters { margin-top: 12px; }
    .filters h2 { margin: 0 0 8px; font-size: 14px; color: #555; }
    .filter-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
    label { display: grid; gap: 4px; font-size: 13px; color: #666; }
    select { min-height: 40px; border: 1px solid #c4c4c4; border-radius: 8px; background: #fff; padding: 7px 9px; }
  </style>
</head>
<body>
  <header>
    <div class="toolbar">
      <strong>Noun Smell Review</strong>
      <span id="counter" class="muted"></span>
    </div>
  </header>
  <main>
    <section class="card" id="card"></section>
    <section class="card filters">
      <h2>Queue</h2>
      <div class="filter-grid">
        <label>Source <select id="source"></select></label>
        <label>Smell <select id="smell"></select></label>
        <label>Status <select id="status"></select></label>
      </div>
    </section>
  </main>
  <script>
    const state = { items: [], filtered: [], index: 0 };
    const $ = (id) => document.getElementById(id);

    async function load() {
      state.items = await fetch('/api/items').then(r => r.json());
      setupFilters();
      applyFilters();
    }

    function setupFilters() {
      fill('source', ['all', ...new Set(state.items.map(x => x.source))]);
      fill('smell', ['all', ...new Set(state.items.map(x => x.smell))]);
      fill('status', ['unlabeled', 'all', 'agree', 'disagree', 'skip']);
      $('source').onchange = applyFilters;
      $('smell').onchange = applyFilters;
      $('status').onchange = applyFilters;
    }

    function fill(id, values) {
      $(id).innerHTML = values.map(v => `<option value="${v}">${v}</option>`).join('');
    }

    function applyFilters() {
      const source = $('source').value;
      const smell = $('smell').value;
      const status = $('status').value;
      state.filtered = state.items.filter(item => {
        const label = item.human_label || '';
        return (source === 'all' || item.source === source)
          && (smell === 'all' || item.smell === smell)
          && (status === 'all' || (status === 'unlabeled' ? !label : label === status));
      });
      state.index = 0;
      render();
    }

    function move(delta) {
      if (!state.filtered.length) return;
      state.index = Math.max(0, Math.min(state.filtered.length - 1, state.index + delta));
      render();
      focusReview();
    }

    function render() {
      const card = $('card');
      $('counter').textContent = `${state.filtered.length ? state.index + 1 : 0} / ${state.filtered.length}`;
      if (!state.filtered.length) {
        card.innerHTML = '<p>No items for these filters.</p>';
        return;
      }
      const item = state.filtered[state.index];
      const original = mdHighlight(item.target_sentence || item.line || '', item.phrase || '');
      const transform = item.classifier_rewrite
        ? `<span class="orig">${original}</span><span class="arrow">&rarr;</span><span class="repl">${md(item.classifier_rewrite)}</span>`
        : `<span class="orig">${original}</span>`;
      const before = item.before_sentence ? `<span class="ctx-side">${md(item.before_sentence)}</span><span class="gap-lg"></span>` : '';
      const after = item.after_sentence ? `<span class="gap-sm"></span><span class="ctx-side">${md(item.after_sentence)}</span>` : '';
      const label = item.human_label || '';
      const note = item.human_note || '';
      card.innerHTML = `
        <p class="ctx">${before}${transform}${after}</p>
        <div class="decide">
          <button class="good ${label === 'agree' ? 'sel' : ''}" onclick="labelCurrent('agree')">Agree</button>
          <button class="bad ${label === 'disagree' ? 'sel' : ''}" onclick="labelCurrent('disagree')">Disagree</button>
          <button class="skip ${label === 'skip' ? 'sel' : ''}" onclick="labelCurrent('skip')">Skip</button>
        </div>
        <p class="agent"><span class="decision ${escapeHtml(item.classifier_label || '')}">${escapeHtml(decisionText(item.classifier_label))}</span> ${escapeHtml(item.classifier_reason || '')}</p>
        <details class="note-wrap" ${note ? 'open' : ''}>
          <summary>Add note</summary>
          <textarea id="note" onchange="saveOnly()">${escapeHtml(note)}</textarea>
        </details>
        <div class="nav">
          <button onclick="move(-1)">Prev</button>
          <button onclick="move(1)">Next</button>
        </div>
        <div class="meta">
          <span class="pill">${item.source}</span>
          <span class="pill">${item.smell}</span>
          <span class="path">${item.path}:${item.line_no}</span>
        </div>
      `;
    }

    function decisionText(label) {
      if (label === 'bad') return 'Agent: not good';
      if (label === 'keep') return 'Agent: good';
      if (label === 'skip') return 'Agent: skip';
      return 'Agent: unclassified';
    }

    async function labelCurrent(label) {
      await save(label);
      move(1);
    }

    async function saveOnly() {
      const item = state.filtered[state.index];
      await save(item.human_label || '');
    }

    function focusReview() {
      $('card').scrollIntoView({ block: 'start', behavior: 'smooth' });
    }

    async function save(label) {
      const item = state.filtered[state.index];
      const note = $('note').value;
      const updated = await fetch('/api/label', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ id: item.id, human_label: label, human_note: note }),
      }).then(r => r.json());
      Object.assign(item, updated);
      const original = state.items.find(x => x.id === item.id);
      if (original) Object.assign(original, updated);
    }

    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
      if (e.key === 'a') labelCurrent('agree');
      else if (e.key === 'd') labelCurrent('disagree');
      else if (e.key === 's') labelCurrent('skip');
      else if (e.key === 'ArrowLeft') move(-1);
      else if (e.key === 'ArrowRight') move(1);
    });

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
      }[ch]));
    }

    // Markdown-lite: links collapse to their text, `code` -> monospace.
    function md(value) {
      let s = escapeHtml(String(value));
      s = s.replace(/\\[([^\\]]+)\\]\\((https?:\\/\\/[^\\s)]+)\\)/g,
        (m, text, url) => `<a href="${url}" target="_blank" rel="noopener">${text}</a>`);
      s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
      return s;
    }

    // Render markdown-lite and wrap the smell phrase in <mark>.
    function mdHighlight(text, phrase) {
      const SOM = '\\u0001', EOM = '\\u0002';
      let t = String(text);
      if (phrase && t.includes(phrase)) t = t.replace(phrase, SOM + phrase + EOM);
      return md(t).replace(SOM, '<mark>').replace(EOM, '</mark>');
    }

    load();
  </script>
</body>
</html>
"""


class App(BaseHTTPRequestHandler):
    data_path: Path
    items: list[dict]

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.respond_text(HTML, "text/html")
            return
        if parsed.path == "/api/items":
            query = parse_qs(parsed.query)
            items = self.items
            if "source" in query:
                items = [item for item in items if item.get("source") in query["source"]]
            if "smell" in query:
                items = [item for item in items if item.get("smell") in query["smell"]]
            self.respond_json(items)
            return
        self.send_error(404)

    def do_POST(self) -> None:
        if self.path != "/api/label":
            self.send_error(404)
            return
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        item_id = payload.get("id")
        for item in self.items:
            if item.get("id") == item_id:
                item["human_label"] = payload.get("human_label", item.get("human_label", ""))
                item["human_note"] = payload.get("human_note", item.get("human_note", ""))
                self.data_path.write_text(json.dumps(self.items, indent=2), encoding="utf-8")
                self.respond_json(item)
                return
        self.send_error(404)

    def respond_text(self, text: str, content_type: str) -> None:
        encoded = text.encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", f"{content_type}; charset=utf-8")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def respond_json(self, value) -> None:
        self.respond_text(json.dumps(value), "application/json")

    def log_message(self, format: str, *args) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    App.data_path = args.data
    App.items = json.loads(args.data.read_text(encoding="utf-8"))
    server = ThreadingHTTPServer((args.host, args.port), App)
    print(f"Serving {args.data} at http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
