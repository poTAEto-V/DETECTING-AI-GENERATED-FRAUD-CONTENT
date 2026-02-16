from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Analyze Page (FORM yaha aayega)
@app.route("/analyze", methods=["POST"])
def analyze():
    message = request.form["message"]

    # abhi fake result (later AI model)
    risk = random.randint(10, 95)

    if risk > 60:
        result = "⚠️ Fraud Message Detected"
    else:
        result = "✅ Safe Message"

    return render_template("result.html", result=result, message=message)


if __name__ == "__main__":
    app.run(debug=True)
