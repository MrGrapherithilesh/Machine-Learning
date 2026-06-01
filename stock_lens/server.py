from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


class StockLensHandler(SimpleHTTPRequestHandler):
    root: Path

    def __init__(self, *args, root: Path, **kwargs):
        self.root = root.resolve()
        super().__init__(*args, directory=str(self.root), **kwargs)

    def translate_path(self, path: str) -> str:
        route = unquote(urlparse(path).path)
        if route in ("", "/"):
            route = "/stock_lens/web/index.html"

        if route in ("/app.js", "/styles.css"):
            route = f"/stock_lens/web{route}"

        candidate = (self.root / route.lstrip("/")).resolve()
        if self.root not in candidate.parents and candidate != self.root:
            return str(self.root / "stock_lens" / "web" / "index.html")
        return str(candidate)

    def log_message(self, format: str, *args) -> None:
        print(f"[stock-lens] {format % args}")


def serve(host: str = "127.0.0.1", port: int = 8765, root: str | Path | None = None) -> None:
    project_root = Path(root) if root is not None else Path(__file__).resolve().parents[1]
    handler = partial(StockLensHandler, root=project_root)
    httpd = ThreadingHTTPServer((host, port), handler)
    print(f"Stock Lens UI running at http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")
    httpd.serve_forever()
