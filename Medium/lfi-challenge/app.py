import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Dynamically resolves relative to app.py location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(
    BASE_DIR, "welcome", "to", "harsh's", "cyber", "ctf", "pages"
)


@app.route("/")
def index():
  page = request.args.get("file", "system.txt")
  content = ""

  try:
    raw_path = os.path.join(PAGES_DIR, page)
    file_path = os.path.normpath(raw_path)
    with open(file_path, "r", encoding="utf-8") as f:
      content = f.read()
  except Exception as e:
    content = f"[!] System Error: Unable to read memory segment ({str(e)})"

  return render_template("index.html", content=content, page=page)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)