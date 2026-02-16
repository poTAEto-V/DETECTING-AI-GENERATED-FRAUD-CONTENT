from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# ANALYZE ROUTE (FORM SUBMIT)
@app.route("/analyze", methods=["POST"])
def analyze():

    message = request.form.get("message")

    # fake AI score (later model laga dena)
    score = random.randint(10, 100)

    if score >= 70:
        level = "CRITICAL FRAUD"
    elif score >= 40:
        level = "SUSPICIOUS"
    else:
        level = "SAFE"

    return render_template(
        "result.html",
        text=message,
        score=score,
        level=level
    )


if __name__ == "__main__":
    app.run(debug=True)

