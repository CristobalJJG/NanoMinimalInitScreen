from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SITES_FILE = ROOT / "sites.json"


class DashboardHandler(SimpleHTTPRequestHandler):
    def do_DELETE(self):
        if not self.path.startswith("/api/sites/"):
            self.send_error(404)
            return

        try:
            index = int(self.path.rsplit("/", 1)[-1])
            sites = json.loads(SITES_FILE.read_text(encoding="utf-8"))
            if index < 0 or index >= len(sites):
                raise ValueError("El sitio no existe.")
            sites.pop(index)
            SITES_FILE.write_text(
                json.dumps(sites, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            self.send_json(200, {"sites": sites})
        except (ValueError, json.JSONDecodeError, OSError) as error:
            self.send_json(400, {"error": str(error)})

    def do_POST(self):
        if self.path != "/api/sites":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
            name = str(payload.get("name", "")).strip()
            url = str(payload.get("url", "")).strip()
            photo = str(payload.get("photo", "")).strip()

            if not name or not url:
                raise ValueError("El nombre y la URL del sitio son obligatorios.")
            if not (url.startswith("http://") or url.startswith("https://")):
                raise ValueError("La URL debe comenzar por http:// o https://.")
            if photo and not (photo.startswith("http://") or photo.startswith("https://")):
                raise ValueError("La imagen debe ser una URL http(s).")

            sites = json.loads(SITES_FILE.read_text(encoding="utf-8"))
            site = {"name": name, "url": url}
            if photo:
                site["photo"] = photo
            sites.append(site)
            SITES_FILE.write_text(
                json.dumps(sites, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            self.send_json(200, {"sites": sites})
        except (ValueError, json.JSONDecodeError, OSError) as error:
            self.send_json(400, {"error": str(error)})

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("", 8000), DashboardHandler)
    print("Dashboard disponible en http://localhost:8000/dashboard.html")
    server.serve_forever()
