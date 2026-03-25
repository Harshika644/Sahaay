import json
import sqlite3
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sahaay.db"
HOST = "127.0.0.1"
PORT = 8000


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submission_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def insert_submission(submission_type, payload):
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO submissions (submission_type, payload, created_at) VALUES (?, ?, ?)",
            (submission_type, json.dumps(payload), created_at),
        )


def fetch_submissions():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT submission_type, payload, created_at FROM submissions ORDER BY id ASC"
        ).fetchall()

    grouped = {"aidRequests": [], "volunteerSignups": []}
    for row in rows:
        payload = json.loads(row["payload"])
        payload["savedAt"] = row["created_at"]
        if row["submission_type"] == "aid":
            grouped["aidRequests"].append(payload)
        elif row["submission_type"] == "volunteer":
            grouped["volunteerSignups"].append(payload)
    return grouped


def clear_submissions(submission_type=None):
    with get_connection() as connection:
        if submission_type in {"aid", "volunteer"}:
            connection.execute(
                "DELETE FROM submissions WHERE submission_type = ?",
                (submission_type,),
            )
        else:
            connection.execute("DELETE FROM submissions")


class SahaayHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/submissions":
            self.send_json(fetch_submissions())
            return
        if parsed.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/submit":
            self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found")
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length)
            body = json.loads(raw_body.decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid JSON payload")
            return

        submission_type = body.get("type")
        payload = body.get("data")

        if submission_type not in {"aid", "volunteer"} or not isinstance(payload, dict):
            self.send_error(HTTPStatus.BAD_REQUEST, "Invalid submission payload")
            return

        insert_submission(submission_type, payload)
        self.send_json({"ok": True}, status=HTTPStatus.CREATED)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/submissions":
            self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found")
            return

        params = parse_qs(parsed.query)
        submission_type = params.get("type", [None])[0]
        clear_submissions(submission_type)
        self.send_json({"ok": True})

    def send_json(self, payload, status=HTTPStatus.OK):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def main():
    init_db()
    server = ThreadingHTTPServer((HOST, PORT), SahaayHandler)
    print(f"Sahaay server running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
