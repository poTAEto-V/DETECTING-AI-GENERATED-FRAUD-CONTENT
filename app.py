from flask import Flask, render_template, request
from fraud_detector import analyze_message
import os

app = Flask(__name__)

# HOME
@app.route("/")
def home():
    return render_template("index.html")

# ANALYZE
@app.route("/analyze", methods=["POST"])
def analyze():

    message = request.form.get("message")

    if not message:
        return render_template("index.html")

    # MUST MATCH fraud_detector return count
    score, level, reasons, words, ai_prob, creds, urls, explanation = analyze_message(message)

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

# RUN (DEPLOY SAFE)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render/Railway use this
    app.run(host="0.0.0.0", port=port)





