import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize an in-memory SQLite DB
conn = sqlite3.connect(":memory:", check_same_thread=False)

# Enforce read-only mode after creating the schema
with conn:
  conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
  conn.execute(
      "INSERT INTO users (username, password) VALUES ('admin', 'Sup3r_S3cr3t_P@ssw0rd_98412');"
  )
  conn.execute(
      "INSERT INTO users (username, password) VALUES ('guest', 'guest123');"
  )
  # Prevent any INSERT / UPDATE / DELETE operations
  conn.execute("PRAGMA query_only = ON;")

FLAG = "IITMCC{SQL1_C0MM3NT_BYP4SS_UNL0CK3D}"

@app.route("/", methods=["GET", "POST"])
def login():
  message = None
  success = False
  flag = None

  if request.method == "POST":
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Vulnerable raw SQL concatenation
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}';"

    try:
      cursor = conn.cursor()
      cursor.execute(query)
      user = cursor.fetchone()

      if user:
        # Check if the returned row is the admin account
        if user[1] == "admin":
          success = True
          message = f"Welcome, {user[1]}! Access granted to core reboot sector."
          flag = FLAG
        else:
          message = f"Logged in as {user[1]}. Access restricted: Admin privilege required."
      else:
        message = "Invalid credentials. Access Denied."
    except Exception as e:
      message = f"Database Error: {str(e)}"

  return render_template("index.html", message=message, success=success, flag=flag)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)