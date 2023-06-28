from flask import Flask, render_template, request, redirect, url_for, flash
import secrets
import os
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config["APPLICATION_ROOT"] = "/onetimelink"

# Add the following line to enable proxy awareness
app.wsgi_app = ProxyFix(app.wsgi_app)

messages = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        if not message:
            flash("Please enter a message.")
            return redirect(app.config["APPLICATION_ROOT"])

        token = secrets.token_hex(16)
        messages[token] = {
            'data': message,
            'opened': False,
        }
        unique_link = url_for("unique_link", token=token, _external=True).replace('/unique-link/', '/onetimelink/unique-link/')
        flash(f"Your unique link: {unique_link}")
        return redirect(app.config["APPLICATION_ROOT"])

    return render_template("index.html")


@app.route("/unique-link/<token>")
def unique_link(token):
    if token in messages and not messages[token]['opened']:
        messages[token]['opened'] = True
        return messages[token]['data']
    else:
        return "Sorry, this link has expired or does not exist.", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

