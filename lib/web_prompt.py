"""web_prompt emitter: GENERATE_WEB.md + ASK_USER_WEB.md + chapter text, chunked,
plus normative docs/RESEARCH_WEB_MULTIMODAL_LEARNING.md excerpts for generating
Brilliant.org-grade web-native chapter studies.
"""
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
BUDGET = 12000
OVERLAP = 500


def chunk(text: str, budget: int = BUDGET, overlap: int = OVERLAP) -> list[str]:
    """Chunk text into overlapping slices for LLM context management."""
    if len(text) <= budget:
        return [text]
    parts, i = [], 0
    while i < len(text):
        parts.append(text[i:i + budget])
        i += budget - overlap
    return parts


def get_research_excerpts() -> str:
    """Extract key pedagogical and architectural sections from the research white paper."""
    doc_path = ROOT / "docs" / "RESEARCH_WEB_MULTIMODAL_LEARNING.md"
    if not doc_path.exists():
        return ""
    content = doc_path.read_text(encoding="utf-8")
    
    # We select key sections: Empirical effect sizes, 5-stage micro-stepping,
    # the 6 archetypes, design system, and the two production prototypes.
    lines = content.splitlines()
    
    # Locate Section 2 to Section 7
    s2_idx = next((i for i, l in enumerate(lines) if "## 2. Empirical Cognitive Research" in l), 0)
    s7_idx = next((i for i, l in enumerate(lines) if "## 7. Strategic Implementation Roadmap" in l), len(lines))
    
    return "\n".join(lines[s2_idx:s7_idx])


def get_server_template(book: str, chapter: str) -> str:
    """Returns a standalone, production-ready Python server script for web_pack/<book>/<chapter>/server.py."""
    return f'''#!/usr/bin/env python3
"""Dedicated Local Chapter Server for {book} - {chapter}
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
                data = json.loads(body) if body else {{}}
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON body")
                return

            code = data.get("code", "")
            lang = data.get("lang", "c")

            if not code.strip():
                self._send_json({{"success": False, "error": "Empty code payload"}})
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
                        return {{
                            "success": False,
                            "phase": "compile",
                            "stdout": comp.stdout,
                            "stderr": comp.stderr,
                            "returncode": comp.returncode,
                        }}
                    if not run_exec:
                        return {{
                            "success": True,
                            "phase": "compile",
                            "stdout": comp.stdout,
                            "stderr": comp.stderr,
                            "returncode": 0,
                        }}

                    # Run binary with strict timeout
                    run = subprocess.run([str(binary)], capture_output=True, text=True, timeout=2.0)
                    return {{
                        "success": run.returncode == 0,
                        "phase": "run",
                        "stdout": run.stdout,
                        "stderr": run.stderr,
                        "returncode": run.returncode,
                    }}
                except subprocess.TimeoutExpired:
                    return {{"success": False, "error": "Execution timed out (2.0s limit)"}}
                except FileNotFoundError:
                    return {{"success": False, "error": "Host compiler 'gcc' not found"}}
            elif lang == "python":
                src = tmppath / "main.py"
                src.write_text(code, encoding="utf-8")
                try:
                    run = subprocess.run([sys.executable, str(src)], capture_output=True, text=True, timeout=2.0)
                    return {{
                        "success": run.returncode == 0,
                        "phase": "run",
                        "stdout": run.stdout,
                        "stderr": run.stderr,
                        "returncode": run.returncode,
                    }}
                except subprocess.TimeoutExpired:
                    return {{"success": False, "error": "Execution timed out (2.0s limit)"}}
            else:
                return {{"success": False, "error": f"Unsupported language: {{lang}}"}}


def run_server(port: int = 8080, open_browser: bool = True):
    free_port = find_free_port(port)
    url = f"http://localhost:{{free_port}}/"
    
    # Custom TCPServer allowing port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", free_port), ChapterRequestHandler) as httpd:
        print(f"============================================================")
        print(f"  termlearn web study: {book} / {chapter}")
        print(f"  Serving at: {{url}}")
        print(f"  Directory:  {{DIRECTORY}}")
        print(f"  Press Ctrl+C to stop.")
        print(f"============================================================")
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nServer stopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Serve {book} {chapter} interactive web study")
    parser.add_argument("--port", type=int, default=8080, help="Preferred port (default: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open browser automatically")
    args = parser.parse_args()
    run_server(port=args.port, open_browser=not args.no_browser)
'''


def build_web_prompt(book: str, chapter: str) -> str:
    """Build a complete, self-contained AI prompt for generating an interactive web study."""
    gen_web_path = ROOT / "prompts" / "GENERATE_WEB.md"
    ask_web_path = ROOT / "prompts" / "ASK_USER_WEB.md"
    
    if not gen_web_path.exists():
        raise FileNotFoundError(f"Missing master web prompt: {gen_web_path}")
    if not ask_web_path.exists():
        raise FileNotFoundError(f"Missing web interrogation template: {ask_web_path}")
        
    gen = gen_web_path.read_text(encoding="utf-8")
    ask = ask_web_path.read_text(encoding="utf-8")
    
    raw = ROOT / "books" / book / "raw_chapters" / f"{chapter}.txt"
    if not raw.exists():
        raise FileNotFoundError(f"No extracted text found at: {raw} — run extract first")
    text = raw.read_text(encoding="utf-8")
    parts = chunk(text)
    
    target_dir = f"web_pack/{book}/{chapter}"
    
    agent_header = (
        f"# =============================================================================\n"
        f"# INSTRUCTIONS FOR AI AGENTS & CODING ASSISTANTS:\n"
        f"# TARGET OUTPUT DIRECTORY: {target_dir}/\n"
        f"# REQUIRED FILES TO CREATE IN DIRECTORY:\n"
        f"#   1. {target_dir}/index.html  (Semantic HTML5 shell with all micro-step cards & SVG viewports)\n"
        f"#   2. {target_dir}/style.css   (Brilliant design system, $44px touch targets, dark palette)\n"
        f"#   3. {target_dir}/app.js      (Reactive state engine, scrubbers, sandboxes, validation)\n"
        f"#   4. {target_dir}/server.py   (Self-contained chapter HTTP server with auto-port & browser launch)\n"
        f"#   5. {target_dir}/meta.json   (Manifest of chapter concepts, steps, and widgets)\n"
        f"#\n"
        f"# [MANDATORY DIRECTIVES — READ CAREFULLY BEFORE WRITING A SINGLE LINE]\n"
        f"# 1. PUT ALL YOUR MIGHT & GO PLUS ULTRA (NO HALF-ASSING):\n"
        f"#    The learner studies SOLELY from your generated interactive web app — never from the book.\n"
        f"#    Produce a masterwork of pedagogical engineering grounded in cognitive science.\n"
        f"#    Zero placeholders (NO 'TODO', NO '/* implement later */', NO lazy hand-waving).\n"
        f"# 2. STANDALONE ZERO-BUILD ARCHITECTURE:\n"
        f"#    Use vanilla HTML5, CSS3, ES2022+ JavaScript, and responsive inline SVG.\n"
        f"#    Require zero npm packages, zero bundlers, and zero build steps. The app must run\n"
        f"#    immediately by opening `index.html` or executing `python server.py`.\n"
        f"# 3. THE 5-STAGE MICRO-STEPPING MODEL:\n"
        f"#    Decompose every core concept into 3–7 atomized cards following:\n"
        f"#    Stage 1: Intuitive Puzzle (direct manipulation, 0 jargon)\n"
        f"#    Stage 2: Pattern Induction (scrubbers, observe invariants)\n"
        f"#    Stage 3: Productive Failure (boundary case stress-test breaking naive model)\n"
        f"#    Stage 4: Subgoal Naming (functional concept label & spatial bridge)\n"
        f"#    Stage 5: Formal Abbreviation (mathematical formula / C code implementation)\n"
        f"# 4. INTERACTION ARCHETYPES (MINIMUM 2 PER CHAPTER):\n"
        f"#    Incorporate real interactive scrubbers (drag-to-resize geometry/parameters),\n"
        f"#    constrained memory sandboxes (pointers, stack frames, heap leak detectors),\n"
        f"#    algorithmic steppers (synchronized code cursor + memory graph), or bug spotters.\n"
        f"# 5. INLINE VARIABLE COLOR-CODING & COGNITIVE ERGONOMICS:\n"
        f"#    Every prose mention of a variable or pointer MUST share the exact hex color of its\n"
        f"#    counterpart on the SVG canvas. Maximum 50 words per card before an interaction.\n"
        f"# 6. MULTI-TURN / MULTI-STEP GENERATION PROTOCOL:\n"
        f"#    Do not rush or compress the output. Write the files methodically across turns or tool calls:\n"
        f"#    First scaffold directory + meta.json + server.py + style.css, then write index.html, then app.js.\n"
        f"# =============================================================================\n\n"
    )
    
    research_excerpts = get_research_excerpts()
    server_template = get_server_template(book, chapter)
    
    out = [
        agent_header,
        gen, "\n---\n",
        ask, "\n---\n",
        "# NORMATIVE PEDAGOGICAL & TECHNICAL RESEARCH EXCERPTS (from docs/RESEARCH_WEB_MULTIMODAL_LEARNING.md):\n",
        research_excerpts, "\n---\n",
        f"# STANDALONE CHAPTER SERVER TEMPLATE ({target_dir}/server.py):\n",
        "```python\n" + server_template + "\n```\n",
        "\n---\n",
        f"# CHAPTER {chapter} OF {book} ({len(parts)} part(s))",
        f"# TARGET DIRECTORY DESTINATION: {target_dir}/",
        f"# Process: Answer ASK_USER_WEB questions first, then create files in `{target_dir}/`.\n"
    ]
    
    for n, p in enumerate(parts, 1):
        out.append(f"\n## part {n}/{len(parts)}\n\n{p}\n")
        
    return "\n".join(out)


def scaffold_chapter(book: str, chapter: str, title: str = "") -> Path:
    """Creates the initial directory web_pack/<book>/<chapter> with server.py and meta.json."""
    target_dir = ROOT / "web_pack" / book / chapter
    target_dir.mkdir(parents=True, exist_ok=True)
    
    server_file = target_dir / "server.py"
    if not server_file.exists():
        server_file.write_text(get_server_template(book, chapter), encoding="utf-8")
        server_file.chmod(0o755)
        
    meta_file = target_dir / "meta.json"
    if not meta_file.exists():
        meta_content = {
            "book": book,
            "chapter_id": chapter,
            "title": title or f"Chapter {chapter.upper()}",
            "steps": [],
            "widgets": []
        }
        import json
        meta_file.write_text(json.dumps(meta_content, indent=2), encoding="utf-8")
        
    return target_dir


def emit(book: str, chapter: str, out: str | None = None):
    """Emit the generated web study prompt to stdout or a file."""
    prompt = build_web_prompt(book, chapter)
    if out:
        out_path = Path(out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(prompt, encoding="utf-8")
        print(f"wrote web prompt to {out} ({len(prompt)} chars)")
    else:
        print(prompt)
