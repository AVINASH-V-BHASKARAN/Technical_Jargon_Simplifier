"""Local UI for the glossary engine. Run python app.py and open localhost:8527."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
from simplifier import simplify, GLOSSARY, SAMPLES

ROOT = Path(__file__).resolve().parent
MAX_CHARS = 12000
MAX_BYTES = 64000

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Do not log pasted text.

    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ('/','/index.html'):
            body = (ROOT/'index.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(body)))
            self.send_header('X-Content-Type-Options','nosniff')
            self.end_headers(); self.wfile.write(body)
        elif self.path == '/api/glossary':
            self.send_json(200, {'terms':GLOSSARY,'samples':[text for text,expected in SAMPLES[:16]]})
        elif self.path == '/api/health':
            self.send_json(200, {'status':'ready','method':'rule-based glossary','terms':len(GLOSSARY)})
        else:
            self.send_json(404, {'error':'Page not found.'})

    def do_POST(self):
        if self.path != '/api/simplify':
            return self.send_json(404, {'error':'Page not found.'})
        try:
            length = int(self.headers.get('Content-Length','0'))
        except ValueError:
            return self.send_json(400, {'error':'Invalid request length.'})
        if length <= 0 or length > MAX_BYTES:
            return self.send_json(413, {'error':'Send a text request smaller than 64 KB.'})
        body = self.rfile.read(length)
        if self.headers.get('Content-Type','').split(';')[0].strip().lower() != 'application/json':
            return self.send_json(415, {'error':'Send JSON with a text field.'})
        try:
            payload = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            return self.send_json(400, {'error':'The request is not valid JSON.'})
        if not isinstance(payload,dict) or not isinstance(payload.get('text'),str):
            return self.send_json(400, {'error':'The text field must contain text.'})
        if len(payload['text']) > MAX_CHARS:
            return self.send_json(400, {'error':'Keep the text under 12,001 characters.'})
        self.send_json(200, simplify(payload['text']))

if __name__ == '__main__':
    print('Technical Jargon Simplifier: http://127.0.0.1:8527',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8527),Handler).serve_forever()
