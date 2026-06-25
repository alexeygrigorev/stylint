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
    :root { font-family: system-ui, sans-serif; color: #1b1b1f; background: #f7f7f4; line-height: 1.45; }
    body { margin: 0; }
    header { position: sticky; top: 0; background: #fff; border-bottom: 1px solid #e3e3e3; padding: 8px 14px; z-index: 2; }
    main { max-width: 720px; margin: 0 auto; padding: 10px 12px 28px; }
    .toolbar { display: flex; gap: 10px; align-items: baseline; justify-content: space-between; }
    .toolbar strong { font-size: 16px; }
    .muted { color: #888; }
    button, select, textarea { font: inherit; }

    .card { background: #fff; border-radius: 10px; padding: 12px 14px; margin-top: 10px; }

    /* Context: one flowing block, target sentence highlighted in place */
    .ctx { margin: 0; font-size: 16px; line-height: 1.55; }
    .ctx-side { color: #9a9a9a; }
    .ctx-target { color: #1b1b1f; }
    mark { background: #ffe066; padding: 0 2px; border-radius: 3px; }

    /* Transform: original -> suggested rewrite */
    .rw { margin: 10px 0 0; font-size: 14px; display: grid; grid-template-columns: 1fr auto 1fr; gap: 8px; align-items: center; }
    .rw-from { color: #8a8a8a; }
    .rw-arrow { color: #1f6feb; font-weight: 700; font-size: 18px; text-align: center; }
    .rw-to { color: #1b6b2e; }

    /* Decision row: one compact row */
    .decide { display: grid; grid-template-columns: 1fr 1fr 0.8fr; gap: 8px; margin-top: 12px; }
    .decide button { border: 1px solid #cfcfcf; background: #fff; padding: 11px 0; border-radius: 8px; cursor: pointer; font-weight: 600; }
    .decide .good { background: #eef8ef; border-color: #bcdcc0; color: #1b6b2e; }
    .decide .bad { background: #fdeeee; border-color: #e4bdbd; color: #a3322f; }
    .decide .skip { background: #f2f2f2; color: #555; }
    .decide button.sel { outline: 3px solid #1f6feb; outline-offset: -1px; }

    /* Agent review (secondary, small) */
    .agent { margin: 12px 0 0; font-size: 13px; color: #555; }
    .decision { display: inline-block; border-radius: 999px; padding: 2px 8px; border: 1px solid #ccc; background: #fafafa; font-weight: 650; font-size: 12px; }
    .decision.bad { background: #fff0f0; border-color: #e3aaaa; color: #a3322f; }
    .decision.keep { background: #eef8ef; border-color: #a8d3ad; color: #1b6b2e; }

    /* Note + nav + meta */
    label { display: grid; gap: 4px; font-size: 13px; color: #666; }
    textarea { width: 100%; min-height: 44px; box-sizing: border-box; margin-top: 8px; border: 1px solid #ccc; border-radius: 8px; padding: 8px; font-size: 14px; }
    .nav { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }
    .nav button { border: 1px solid #cfcfcf; background: #fff; padding: 9px 0; border-radius: 8px; cursor: pointer; }
    .meta { color: #999; font-size: 11px; display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
    .pill { border: 1px solid #e6e6e6; border-radius: 999px; padding: 2px 8px; background: #fafafa; }
    .path { overflow-wrap: anywhere; }

    .filters { margin-top: 10px; }
    .filters h2 { margin: 0 0 8px; font-size: 14px; color: #555; }
    .filter-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }
    select { min-height: 38px; border: 1px solid #c4c4c4; border-radius: 6px; background: #fff; padding: 6px 8px; }
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
      fill('status', ['unlabeled', 'all', 'keep', 'bad', 'skip']);
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
      const target = item.highlighted_target_sentence || item.highlighted_line || '';
      const before = item.before_sentence ? `<span class="ctx-side">${escapeHtml(item.before_sentence)}</span> ` : '';
      const after = item.after_sentence ? ` <span class="ctx-side">${escapeHtml(item.after_sentence)}</span>` : '';
      const rewrite = item.classifier_rewrite ? `
        <p class="rw">
          <span class="rw-from">${escapeHtml(item.target_sentence || item.line || '')}</span>
          <span class="rw-arrow">&rarr;</span>
          <span class="rw-to">${escapeHtml(item.classifier_rewrite)}</span>
        </p>` : '';
      const label = item.human_label || '';
      card.innerHTML = `
        <p class="ctx">${before}<span class="ctx-target">${target}</span>${after}</p>
        ${rewrite}
        <div class="decide">
          <button class="good ${label === 'keep' ? 'sel' : ''}" onclick="labelCurrent('keep')">Good</button>
          <button class="bad ${label === 'bad' ? 'sel' : ''}" onclick="labelCurrent('bad')">Bad</button>
          <button class="skip ${label === 'skip' ? 'sel' : ''}" onclick="labelCurrent('skip')">Skip</button>
        </div>
        <p class="agent"><span class="decision ${escapeHtml(item.classifier_label || '')}">${escapeHtml(decisionText(item.classifier_label))}</span> ${escapeHtml(item.classifier_reason || '')}</p>
        <label>Note<textarea id="note" onchange="saveOnly()">${escapeHtml(item.human_note || '')}</textarea></label>
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
      if (label === 'bad') return 'Agent: bad';
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
      if (e.key === 'g') labelCurrent('keep');
      else if (e.key === 'b') labelCurrent('bad');
      else if (e.key === 's') labelCurrent('skip');
      else if (e.key === 'ArrowLeft') move(-1);
      else if (e.key === 'ArrowRight') move(1);
    });

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, ch => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
      }[ch]));
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
