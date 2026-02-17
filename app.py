from flask import Flask, render_template, request
from fraud_detector import analyze_message
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    message = request.form.get("message")

    if not message:
        return render_template("index.html")

    result = analyze_message(message)

    # SAFE unpack (works even if counts change)
    score = result[0]
    level = result[1]
    reasons = result[2]
    words = result[3]
    ai_prob = result[4]
    creds = result[5]
    urls = result[6]
    explanation = result[7] if len(result) > 7 else ""

    return render_template(
        "result.html",
        message=message,
        score=score,
        level=level,
        reasons=reasons,
        words=words,
        ai_prob=ai_prob,
        creds=creds,
        urls=urls,
        explanation=explanation
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)






