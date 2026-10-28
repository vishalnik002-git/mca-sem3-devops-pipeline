"""DevOps Pipeline Dashboard — local verification and optional Docker build."""
import os
import sqlite3
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent
DB = Path(os.environ.get("DEVOPS_DB", ROOT / "data" / "pipeline.db"))
APP_STARTED = time.monotonic()
app = Flask(__name__)
run_lock = threading.Lock()

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB, timeout=20)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kind TEXT NOT NULL,
        status TEXT NOT NULL,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        duration_ms INTEGER,
        output TEXT NOT NULL DEFAULT ''
    )""")
    conn.commit()
    return conn

def clock():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def update_run(run_id, **updates):
    with connect() as db:
        keys = list(updates)
        db.execute(f"UPDATE runs SET {', '.join(k + '=?' for k in keys)} WHERE id=?",
                   [updates[k] for k in keys] + [run_id])
        db.commit()

def worker(run_id, kind):
    started = time.monotonic()
    if kind == "tests":
        command = [os.environ.get("PYTHON", "python"), "-m", "unittest", "discover", "-s", "tests", "-v"]
        timeout = 90
    else:
        command = ["docker", "build", "-t", "mca-devops-app:local", "."]
        timeout = 240
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                timeout=timeout, check=False)
        output = (result.stdout + "\n" + result.stderr)[-18000:]
        status = "success" if result.returncode == 0 else "failed"
    except (OSError, subprocess.TimeoutExpired) as exc:
        output, status = str(exc), "failed"
    finally:
        update_run(run_id, status=status, output=output, finished_at=clock(),
                   duration_ms=int((time.monotonic() - started) * 1000))
        run_lock.release()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify(status="healthy", service="DevOps Pipeline Dashboard",
                   uptime_seconds=round(time.monotonic()-APP_STARTED), server_time=clock(),
                   docker_enabled=os.environ.get("ENABLE_DOCKER_BUILDS") == "1")

@app.get("/api/runs")
def runs():
    with connect() as db:
        records = [dict(r) for r in db.execute("SELECT * FROM runs ORDER BY id DESC LIMIT 50")]
    return jsonify(runs=records)

@app.get("/api/stats")
def stats():
    with connect() as db:
        rows = [dict(r) for r in db.execute("SELECT * FROM runs")]
    completed = [r for r in rows if r["status"] != "running"]
    successful = [r for r in completed if r["status"] == "success"]
    return jsonify(total=len(rows), successful=len(successful), failed=sum(r["status"] == "failed" for r in rows),
                   running=sum(r["status"] == "running" for r in rows),
                   success_rate=round(100*len(successful)/len(completed)) if completed else None,
                   avg_duration_ms=round(sum(r["duration_ms"] or 0 for r in completed)/len(completed)) if completed else None)

@app.post("/api/runs")
def start_run():
    if request.content_type and "application/json" not in request.content_type:
        return jsonify(error="Use JSON request body"), 415
    data = request.get_json(silent=True) or {}
    kind = data.get("kind")
    if kind not in {"tests", "docker"}:
        return jsonify(error="Allowed kinds: tests, docker"), 400
    if kind == "docker" and os.environ.get("ENABLE_DOCKER_BUILDS") != "1":
        return jsonify(error="Docker builds are disabled. Set ENABLE_DOCKER_BUILDS=1 on a trusted local machine."), 403
    if not run_lock.acquire(blocking=False):
        return jsonify(error="Another job is running. Try again after it finishes."), 409
    try:
        with connect() as db:
            cur = db.execute("INSERT INTO runs(kind,status,started_at) VALUES(?,?,?)", (kind,"running",clock()))
            db.commit()
            run_id = cur.lastrowid
        threading.Thread(target=worker,args=(run_id,kind),daemon=True).start()
        return jsonify(id=run_id,status="running",kind=kind), 202
    except Exception:
        run_lock.release()
        raise

@app.get("/api/runs/<int:run_id>")
def get_run(run_id):
    with connect() as db:
        row = db.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
    return (jsonify(dict(row)), 200) if row else (jsonify(error="Run not found"), 404)

@app.errorhandler(404)
def not_found(_error):
    return jsonify(error="Not found"),404

if __name__ == "__main__":
    connect()
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT", "5000")),debug=False)
