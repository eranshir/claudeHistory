#!/usr/bin/env python3
"""
Simple HTTP server for Claude History Analyzer.

Serves static files and provides an API endpoint to add instructions to CLAUDE.md.
"""

import http.server
import json
import os
import socketserver
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# CLAUDE.md location
CLAUDE_MD_PATH = Path.home() / ".claude" / "CLAUDE.md"

PORT = 9347


class HistoryHandler(http.server.SimpleHTTPRequestHandler):
    """Handler that serves static files and handles API requests."""

    def do_POST(self):
        """Handle POST requests for API endpoints."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/api/add-instruction":
            self.handle_add_instruction()
        else:
            self.send_error(404, "Not Found")

    def handle_add_instruction(self):
        """Add an instruction to CLAUDE.md."""
        try:
            # Read the request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)

            instruction = data.get("instruction", "").strip()
            title = data.get("title", "").strip()

            if not instruction:
                self.send_json_response({"error": "No instruction provided"}, 400)
                return

            # Ensure .claude directory exists
            CLAUDE_MD_PATH.parent.mkdir(parents=True, exist_ok=True)

            # Read existing content
            existing_content = ""
            if CLAUDE_MD_PATH.exists():
                existing_content = CLAUDE_MD_PATH.read_text()

            # Check if instruction already exists
            if instruction in existing_content:
                self.send_json_response({
                    "success": False,
                    "message": "This instruction already exists in CLAUDE.md"
                }, 200)
                return

            # Append the new instruction
            timestamp = datetime.now().strftime("%Y-%m-%d")
            new_entry = f"\n\n## {title}\n*Added {timestamp} via Claude History Analyzer*\n\n{instruction}\n"

            with open(CLAUDE_MD_PATH, "a") as f:
                f.write(new_entry)

            self.send_json_response({
                "success": True,
                "message": f"Instruction added to {CLAUDE_MD_PATH}",
                "path": str(CLAUDE_MD_PATH)
            }, 200)

        except json.JSONDecodeError:
            self.send_json_response({"error": "Invalid JSON"}, 400)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def do_GET(self):
        """Handle GET requests - serve static files or API endpoints."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/api/claude-md":
            self.handle_get_claude_md()
        else:
            # Serve static files
            super().do_GET()

    def handle_get_claude_md(self):
        """Return current CLAUDE.md content."""
        try:
            content = ""
            if CLAUDE_MD_PATH.exists():
                content = CLAUDE_MD_PATH.read_text()

            self.send_json_response({
                "exists": CLAUDE_MD_PATH.exists(),
                "path": str(CLAUDE_MD_PATH),
                "content": content
            }, 200)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

    def send_json_response(self, data: dict, status_code: int = 200):
        """Send a JSON response."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    """Start the server."""
    # Change to script directory
    os.chdir(Path(__file__).parent)

    with socketserver.TCPServer(("", PORT), HistoryHandler) as httpd:
        print(f"Claude History Server running at http://localhost:{PORT}")
        print(f"CLAUDE.md path: {CLAUDE_MD_PATH}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")


if __name__ == "__main__":
    main()
