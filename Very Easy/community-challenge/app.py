import hashlib
import sqlite3
import time
from flask import Flask, jsonify, make_response, render_template, request

app = Flask(__name__)
DB_FILE = "community_stars.db"
TARGET_STARS = 250  # Set your target count here
FLAG = "IITMCC{CUt3_P4ST3L_ST4R_P0W3R_UNL0CK}"


def init_db():
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS star_givers (
                identifier TEXT PRIMARY KEY,
                ip_addr TEXT,
                device_hash TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()


init_db()


def get_real_ip():
  # Extract real user IP behind Render / Cloudflare reverse proxies
  if request.headers.get("X-Forwarded-For"):
    return request.headers.get("X-Forwarded-For").split(",")[0].strip()
  return request.remote_addr


def get_total_stars():
  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM star_givers")
    return c.fetchone()[0]


@app.route("/")
def index():
  ip = get_real_ip()
  total = get_total_stars()
  already_given = False

  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    c.execute("SELECT 1 FROM star_givers WHERE ip_addr = ?", (ip,))
    if c.fetchone():
      already_given = True

  flag_unlocked = total >= TARGET_STARS
  return render_template(
      "index.html",
      total=total,
      target=TARGET_STARS,
      already_given=already_given,
      flag_unlocked=flag_unlocked,
      flag=FLAG if flag_unlocked else None,
  )


@app.route("/api/scratch", methods=["POST"])
def scratch():
  data = request.get_json() or {}
  device_sig = data.get("device_hash", "generic")
  ip = get_real_ip()

  # Create a composite hash of IP + device attributes
  user_composite_id = hashlib.sha256(
      f"{ip}_{device_sig}".encode()
  ).hexdigest()

  with sqlite3.connect(DB_FILE) as conn:
    c = conn.cursor()
    # Check if either composite hash OR IP already contributed
    c.execute(
        "SELECT 1 FROM star_givers WHERE identifier = ? OR ip_addr = ?",
        (user_composite_id, ip),
    )
    if c.fetchone():
      return (
          jsonify({
              "status": "already_claimed",
              "message": (
                  "You have already gifted a star from this connection! ⭐"
              ),
              "total": get_total_stars(),
          }),
          200,
      )

    try:
      c.execute(
          "INSERT INTO star_givers (identifier, ip_addr, device_hash) VALUES"
          " (?, ?, ?)",
          (user_composite_id, ip, device_sig),
      )
      conn.commit()
    except sqlite3.IntegrityError:
      return (
          jsonify({
              "status": "already_claimed",
              "message": "Star already registered! ✨",
          }),
          200,
      )

  total = get_total_stars()
  return jsonify({
      "status": "success",
      "total": total,
      "flag_unlocked": total >= TARGET_STARS,
      "flag": FLAG if total >= TARGET_STARS else None,
  })


@app.route("/api/status")
def status():
  total = get_total_stars()
  return jsonify({
      "total": total,
      "target": TARGET_STARS,
      "flag_unlocked": total >= TARGET_STARS,
      "flag": FLAG if total >= TARGET_STARS else None,
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)