"""Vercel serverless API for the Technical Jargon Simplifier."""
from http.server import BaseHTTPRequestHandler
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simplifier import GLOSSARY, SAMPLES, simplify

MAX_CHARS = 12000
MAX_BYTES = 64000


class handler(BaseHTTPRequestHandler):
    """Handle the app's API routes in a Vercel Python Function."""

    def log_message(self, *_args):
        # Avoid logging submitted text or request details.
        pass

    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/glossary":
            return self.send_json(200, {
                "terms": GLOSSARY,
                "samples": [text for text, _expected in SAMPLES[:16]],
            })
        if self.path == "/api/health":
            return self.send_json(200, {
                "status": "ready",
                "method": "rule-based glossary",
                "terms": len(GLOSSARY),
            })
        return self.send_json(404, {"error": "Page not found."})

    def do_POST(self):
        if self.path != "/api/simplify":
            return self.send_json(404, {"error": "Page not found."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self.send_json(400, {"error": "Invalid request length."})
        if length <= 0 or length > MAX_BYTES:
            return self.send_json(413, {"error": "Send a text request smaller than 64 KB."})
        if self.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/json":
            return self.send_json(415, {"error": "Send JSON with a text field."})
        try:
            payload = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeDecodeError):
            return self.send_json(400, {"error": "The request is not valid JSON."})
        if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
            return self.send_json(400, {"error": "The text field must contain text."})
        if len(payload["text"]) > MAX_CHARS:
            return self.send_json(400, {"error": "Keep the text under 12,001 characters."})
        return self.send_json(200, simplify(payload["text"]))
