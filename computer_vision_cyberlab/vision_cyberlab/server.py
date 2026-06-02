from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


class CyberVisionHandler(SimpleHTTPRequestHandler):
    root: Path

    def __init__(self, *args, root: Path, **kwargs):
        self.root = root.resolve()
        super().__init__(*args, directory=str(self.root), **kwargs)

    def translate_path(self, path: str) -> str:
        route = unquote(urlparse(path).path)
        if route in ("", "/"):
            route = "/vision_cyberlab/web/index.html"
        if route in ("/app.js", "/styles.css"):
            route = f"/vision_cyberlab/web{route}"

        candidate = (self.root / route.lstrip("/")).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            return str(self.root / "vision_cyberlab" / "web" / "index.html")
        return str(candidate)

    def log_message(self, format: str, *args) -> None:
        print(f"[cyber-vision] {format % args}")


def serve(host: str = "127.0.0.1", port: int = 8790, root: str | Path | None = None) -> None:
    project_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    handler = partial(CyberVisionHandler, root=project_root)
    httpd = ThreadingHTTPServer((host, port), handler)
    print(f"Cyber Vision UI running at http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")
    httpd.serve_forever()
