from flask import Flask, make_response, render_template, request

app = Flask(__name__)

# Predefined active sessions in memory
SESSIONS = {
    "abcdefghijklmnopqrstuvwxyz_guest": "guest",
    "zyxwvutsrqponmlkjihgfedcba22926": "admin",  # Leaked token target
}

FLAG = "IITMCC{S3SS10N_H1J4CK_C00K13_SW4P_PWN}"


@app.route("/", methods=["GET", "POST"])
def index():
  session_token = request.cookies.get("session_id")
  current_user = SESSIONS.get(session_token)

  message = None
  flag = None

  # Handle standard guest login
  if request.method == "POST":
    username = request.form.get("username", "").strip().lower()

    if username == "admin":
      message = "Direct login for 'admin' is disabled. Password resets only."
      resp = make_response(
          render_template(
              "index.html",
              user=current_user,
              message=message,
              flag=flag,
              token=session_token,
          )
      )
      return resp

    elif username == "guest":
      resp = make_response(
          render_template(
              "index.html",
              user="guest",
              message="Logged in as guest.",
              flag=flag,
              token="abcdefghijklmnopqrstuvwxyz_guest",
          )
      )
      resp.set_cookie("session_id", "abcdefghijklmnopqrstuvwxyz_guest")
      return resp
    else:
      message = "Unknown user. Valid trial account is 'guest'."

  # Check current user from cookie
  if current_user == "admin":
    flag = FLAG

  resp = make_response(
      render_template(
          "index.html",
          user=current_user,
          message=message,
          flag=flag,
          token=session_token,
      )
  )
  return resp


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)