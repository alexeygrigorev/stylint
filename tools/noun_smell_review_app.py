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
    :root { font-family: system-ui, sans-serif; color: #1b1b1f; background: #f7f7f4; line-height: 1.5; }
    body { margin: 0; }
    header { position: sticky; top: 0; background: #fff; border-bottom: 1px solid #ddd; padding: 10px 18px; z-index: 2; }
    main { max-width: 960px; margin: 0 auto; padding: 14px 18px; }
    .toolbar { display: flex; gap: 12px; align-items: baseline; justify-content: space-between; }
    .filters { margin-top: 18px; }
    .filters h2 { margin: 0 0 8px; font-size: 16px; }
    .filter-grid { display: grid; grid-template-columns: repeat(3, minmax(150px, 1fr)); gap: 10px; align-items: end; }
    label { display: grid; gap: 4px; font-size: 14px; color: #555; }
    select, button, textarea { font: inherit; }
    select { min-height: 42px; border: 1px solid #bbb; border-radius: 6px; background: #fff; padding: 7px 9px; }
    button { border: 1px solid #b8b8b8; background: #fff; padding: 9px 11px; border-radius: 6px; cursor: pointer; min-height: 40px; }
    button.primary { background: #1f6feb; border-color: #1f6feb; color: white; }
    button.keep { background: #eef8ef; }
    button.bad { background: #fff0f0; }
    button.skip { background: #f3f3f3; }
    .card { background: white; border: 0; border-radius: 8px; padding: 16px; margin-top: 14px; }
    .meta { color: #666; font-size: 13px; display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
    .context { margin: 10px 0; }
    .context h3, .section h3 { margin: 0 0 6px; font-size: 14px; color: #555; }
    blockquote { border: 0; margin: 0; padding: 10px 12px; background: #fafafa; border-radius: 6px; }
    .original blockquote { font-size: 16px; line-height: 1.45; background: #fafafa; color: #555; }
    .replace blockquote { font-size: 18px; line-height: 1.45; background: #fffdf2; }
    .rewrite blockquote { font-size: 17px; line-height: 1.45; background: #f4fbf5; }
    .before-after blockquote { font-size: 15px; color: #666; background: #f7f7f7; }
    .context-lines blockquote { font-size: 15px; color: #666; background: #f7f7f7; }
    mark { background: #ffec80; padding: 1px 3px; border-radius: 3px; }
    textarea { width: 100%; min-height: 70px; box-sizing: border-box; margin-top: 6px; border: 1px solid #bbb; border-radius: 6px; padding: 8px; }
    .row { display: grid; grid-template-columns: repeat(4, minmax(100px, 1fr)); gap: 8px; margin-top: 10px; }
    .nav-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
    .pill { border: 1px solid #ddd; border-radius: 999px; padding: 4px 9px; background: #fafafa; }
    .muted { color: #777; }
    .path { overflow-wrap: anywhere; }
    .section { margin-top: 10px; }
    .decision { display: inline-block; border-radius: 999px; padding: 4px 9px; border: 1px solid #ccc; background: #fafafa; font-weight: 650; }
    .decision.bad { background: #fff0f0; border-color: #e3aaaa; }
    .decision.keep { background: #eef8ef; border-color: #a8d3ad; }
    .explain { margin: 6px 0 0; color: #333; }
    .agent-summary { background: #fafafa; border-radius: 6px; padding: 9px 10px; }
    .agent-summary p { margin: 6px 0 0; }
    .agent-summary p:first-child { margin-top: 0; }
    .review-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 12px; align-items: start; }
    .side-panel { display: grid; gap: 10px; }
    .review-flow { display: grid; gap: 10px; }
    @media (max-width: 760px) {
      header { position: static; padding: 12px; }
      main { padding: 10px 10px 24px; }
      header { padding: 8px 12px; }
      .toolbar strong { font-size: 18px; }
      .filter-grid { grid-template-columns: 1fr; }
      .card { padding: 14px 12px; margin-top: 10px; }
      .row { grid-template-columns: 1fr 1fr; }
      .replace blockquote { font-size: 17px; }
      .review-grid { grid-template-columns: 1fr; gap: 8px; }
    }
    @media (max-width: 420px) {
      .row { grid-template-columns: 1fr; }
      .nav-row { grid-template-columns: 1fr; }
    }
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

	    function sentenceBlock(title, value, className) {
	      if (!value) return '';
	      return `
	        <div class="context ${className}">
	          <h3>${title}</h3>
	          <blockquote>${value}</blockquote>
	        </div>
	      `;
	    }

    function render() {
      const card = $('card');
      $('counter').textContent = `${state.filtered.length ? state.index + 1 : 0} / ${state.filtered.length}`;
      if (!state.filtered.length) {
        card.innerHTML = '<p>No items for these filters.</p>';
        return;
      }
	      const item = state.filtered[state.index];
		      card.innerHTML = `
				        <div class="review-grid">
				          <div class="review-flow">
				            ${sentenceBlock('Previous sentence', escapeHtml(item.before_sentence || ''), 'before-after')}
				            ${sentenceBlock('Text to review', item.highlighted_target_sentence || item.highlighted_line, 'replace')}
				            ${sentenceBlock('Next sentence', escapeHtml(item.after_sentence || ''), 'before-after')}
				            ${item.classifier_rewrite ? `
				              <div class="section rewrite">
				                <h3>Suggested rewrite</h3>
				                <blockquote>${escapeHtml(item.classifier_rewrite)}</blockquote>
				              </div>
			            ` : ''}
          </div>
          <div class="side-panel">
            <div class="agent-summary">
	              <p><strong>Agent review:</strong> <span class="decision ${escapeHtml(item.classifier_label || '')}">${escapeHtml(decisionText(item.classifier_label))}</span></p>
	              ${item.classifier_reason ? `<p>${escapeHtml(item.classifier_reason)}</p>` : ''}
	            </div>
            <div class="section">
              <label>Note<textarea id="note">${escapeHtml(item.human_note || '')}</textarea></label>
            </div>
	            <div class="row">
	              <button class="keep" onclick="labelCurrent('keep')">Good</button>
	              <button class="bad" onclick="labelCurrent('bad')">Bad</button>
	              <button class="skip" onclick="labelCurrent('skip')">Skip</button>
	              <button class="primary" onclick="saveOnly()">Save note</button>
	            </div>
	            <div class="nav-row">
	              <button onclick="move(-1)">Prev</button>
	              <button onclick="move(1)">Next</button>
	            </div>
	          </div>
	        </div>
	        <div class="meta">
	          <span class="pill">${item.id}</span>
	          <span class="pill">${item.source}</span>
	          <span class="pill">${item.smell}</span>
	          <span class="path">${item.path}:${item.line_no}</span>
	        </div>
	      `;
	    }

    function decisionText(label) {
      if (label === 'bad') return 'Bad: rewrite this';
      if (label === 'keep') return 'Good: keep';
      if (label === 'skip') return 'Skip';
      return 'Unclassified';
    }

	    async function labelCurrent(label) {
	      await save(label);
	      move(1);
	    }

	    async function saveOnly() {
	      const item = state.filtered[state.index];
	      await save(item.human_label || '');
	      render();
	      focusReview();
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
