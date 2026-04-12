#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, mimetypes, os, signal, threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

VERSION = '0.3.4-direct-now-playing-topmost-keeper-patch'
STATE_DEFAULT = {
    'standby': False,
    'startup_completed': False,
    'startup_started_at': None,
    'last_transition': None,
    'version': VERSION,
}
READY_MARKER = Path('/tmp/mediastreamer-kiosk-ready')
KEEPER_PIDFILE = Path('/tmp/mediastreamer-artwork-keeper.pid')
_KEEPER_RELEASE_LOCK = threading.Lock()
_KEEPER_RELEASED = False


def atomic_write_json(path: Path, payload: dict) -> None:
    tmp_path = path.with_suffix(path.suffix + '.tmp')
    tmp_path.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    os.replace(tmp_path, path)


def read_json_or_default(path: Path, default: dict) -> dict:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default.copy()


def release_keeper() -> None:
    global _KEEPER_RELEASED
    with _KEEPER_RELEASE_LOCK:
        if _KEEPER_RELEASED:
            return
        _KEEPER_RELEASED = True
    try:
        pid_text = KEEPER_PIDFILE.read_text(encoding='utf-8').strip()
        if not pid_text:
            return
        os.kill(int(pid_text), signal.SIGTERM)
    except Exception:
        pass


def release_keeper_later(delay_seconds: float = 0.9) -> None:
    timer = threading.Timer(delay_seconds, release_keeper)
    timer.daemon = True
    timer.start()


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, state_path: Path, root_dir: Path, **kwargs):
        self.state_path = state_path
        self.root_dir = root_dir
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        super().end_headers()

    def _send_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, path: Path):
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, 'Not found')
            return
        ctype, _ = mimetypes.guess_type(str(path))
        if not ctype:
            ctype = 'application/octet-stream'
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path or '/'
        if path == '/api/state':
            self._send_json(read_json_or_default(self.state_path, STATE_DEFAULT))
            return
        if path == '/api/healthz':
            self._send_json({'ok': True, 'version': VERSION})
            return
        if path in ('/', '/index.html'):
            try:
                READY_MARKER.touch(exist_ok=True)
            except Exception:
                pass
            release_keeper_later(0.9)
            self._serve_file(self.root_dir / 'index.html')
            return
        if path.startswith('/assets/'):
            rel = path.lstrip('/')
            candidate = (self.root_dir / rel).resolve()
            try:
                candidate.relative_to(self.root_dir.resolve())
            except Exception:
                self.send_error(HTTPStatus.FORBIDDEN, 'Forbidden')
                return
            self._serve_file(candidate)
            return
        self.send_error(HTTPStatus.NOT_FOUND, 'Unknown endpoint')

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != '/api/state':
            self.send_error(HTTPStatus.NOT_FOUND, 'Unknown endpoint')
            return
        length = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(length)
        try:
            update = json.loads(raw.decode('utf-8'))
        except Exception:
            self.send_error(HTTPStatus.BAD_REQUEST, 'Invalid JSON')
            return
        current = read_json_or_default(self.state_path, STATE_DEFAULT)
        current.update(update)
        atomic_write_json(self.state_path, current)
        self._send_json(current)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', required=True)
    parser.add_argument('--root', required=True)
    parser.add_argument('--port', type=int, default=7700)
    args = parser.parse_args()
    state_path = Path(args.state).resolve()
    root_dir = Path(args.root).resolve()
    state_path.parent.mkdir(parents=True, exist_ok=True)
    root_dir.mkdir(parents=True, exist_ok=True)
    if not state_path.exists():
        atomic_write_json(state_path, STATE_DEFAULT)

    def handler(*a, **kw):
        return Handler(*a, state_path=state_path, root_dir=root_dir, **kw)

    ThreadingHTTPServer(('127.0.0.1', args.port), handler).serve_forever()


if __name__ == '__main__':
    main()
