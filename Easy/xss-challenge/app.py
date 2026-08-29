import hashlib
import time
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = "super_secret_arcade_glitch_key_999"

FLAG = "IITMCC{XSS_DOM_1NJ3CT10N_PWN}"


@app.route("/", methods=["GET", "POST"])
def index():
  user_input = ""
  # Generate a temporary challenge nonce per session
  if "nonce" not in session:
    session["nonce"] = hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]

  if request.method == "POST":
    user_input = request.form.get("payload", "")

  return render_template(
      "index.html", user_input=user_input, nonce=session["nonce"]
  )


@app.route("/api/verify-xss", methods=["POST"])
def verify():
  data = request.get_json() or {}
  token = data.get("token", "")

  # The backend computes expected hash using the session nonce + secret salt
  expected = hashlib.sha256(
      (session.get("nonce", "") + "_glitch_solved").encode()
  ).hexdigest()

  if token == expected:
    return jsonify({"success": True, "flag": FLAG})
  return jsonify({"error": "Invalid execution proof"}), 403


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)