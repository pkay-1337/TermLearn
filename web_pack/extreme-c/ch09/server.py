#!/usr/bin/env python3
"""Dedicated Local Chapter Server for extreme-c - ch09
Zero-dependency static file server with auto-port discovery, browser launch,
and optional /api/compile or /api/run sandbox endpoints.
"""
import argparse
import http.server
import json
import mimetypes
import os
import socket
import socketserver
import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent

# Ensure modern web MIME types are properly recognized
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/javascript", ".mjs")
mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("text/css", ".css")


def find_free_port(start_port: int = 8080, max_attempts: int = 100) -> int:
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


class ChapterRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # Enable CORS and disable aggressive caching for local interactive development
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_POST(self):
        """Handle optional local code compilation or execution requests."""
        if self.path in ("/api/compile", "/api/run"):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON body")
                return

            code = data.get("code", "")
            lang = data.get("lang", "c")

            if not code.strip():
                self._send_json({"success": False, "error": "Empty code payload"})
                return

            # Execute host compiler/runner safely
            result = self._execute_code(code, lang, run_exec=(self.path == "/api/run"))
            self._send_json(result)
        else:
            self.send_error(404, "Endpoint not found")

    def _send_json(self, data: dict, status: int = 200):
        response_bytes = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def _execute_code(self, code: str, lang: str, run_exec: bool = False) -> dict:
        """Compile and optionally run code in a temporary sandbox with timeout."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            if lang in ("c", "c99"):
                src = tmppath / "main.c"
                binary = tmppath / "main.out"
                src.write_text(code, encoding="utf-8")
                
                cmd = ["gcc", "-Wall", "-Wextra", "-std=c99", str(src), "-o", str(binary)]
                try:
                    comp = subprocess.run(cmd, capture_output=True, text=True, timeout=5.0)
                    if comp.returncode != 0:
                        return {
                            "success": False,
                            "phase": "compile",
                            "stdout": comp.stdout,
                            "stderr": comp.stderr,
                            "returncode": comp.returncode,
                        }
                    if not run_exec:
                        return {
                            "success": True,
                            "phase": "compile",
                            "stdout": comp.stdout,
                            "stderr": comp.stderr,
                            "returncode": 0,
                        }

                    # Run binary with strict timeout
                    run = subprocess.run([str(binary)], capture_output=True, text=True, timeout=2.0)
                    return {
                        "success": run.returncode == 0,
                        "phase": "run",
                        "stdout": run.stdout,
                        "stderr": run.stderr,
                        "returncode": run.returncode,
                    }
                except subprocess.TimeoutExpired:
                    return {"success": False, "error": "Execution timed out (2.0s limit)"}
                except FileNotFoundError:
                    return {"success": False, "error": "Host compiler 'gcc' not found"}
            elif lang == "python":
                src = tmppath / "main.py"
                src.write_text(code, encoding="utf-8")
                try:
                    run = subprocess.run([sys.executable, str(src)], capture_output=True, text=True, timeout=2.0)
                    return {
                        "success": run.returncode == 0,
                        "phase": "run",
                        "stdout": run.stdout,
                        "stderr": run.stderr,
                        "returncode": run.returncode,
                    }
                except subprocess.TimeoutExpired:
                    return {"success": False, "error": "Execution timed out (2.0s limit)"}
            else:
                return {"success": False, "error": f"Unsupported language: {lang}"}


def run_server(port: int = 8080, open_browser: bool = True):
    free_port = find_free_port(port)
    url = f"http://localhost:{free_port}/"
    
    # Custom TCPServer allowing port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", free_port), ChapterRequestHandler) as httpd:
        print(f"============================================================")
        print(f"  termlearn web study: extreme-c / ch09")
        print(f"  Serving at: {url}")
        print(f"  Directory:  {DIRECTORY}")
        print(f"  Press Ctrl+C to stop.")
        print(f"============================================================")
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Serve extreme-c ch09 interactive web study")
    parser.add_argument("--port", type=int, default=8080, help="Preferred port (default: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()
    run_server(port=args.port, open_browser=not args.no_browser)
