import re

def fraud_detector(text):
    score = 0
    reasons = []
    suspicious_words = []

    urgency = ["urgent", "immediately", "act now", "limited time"]
    authority = ["bank", "income tax", "police", "rbi", "sbi", "hdfc", "icici"]
    credentials = ["otp", "password", "cvv", "pin", "verify otp"]
    threats = ["blocked", "suspended", "legal action", "account locked"]

    text_lower = text.lower()

    # urgency
    for word in urgency:
        if word in text_lower:
            score += 20
            reasons.append("Creates urgency pressure")
            suspicious_words.append(word)

    # authority impersonation
    for word in authority:
        if word in text_lower:
            score += 20
            reasons.append("Possible authority impersonation")
            suspicious_words.append(word)

    # sensitive info request
    for word in credentials:
        if word in text_lower:
            score += 40
            reasons.append("Requests sensitive information (OTP/PIN/password)")
            suspicious_words.append(word)

    # threats
    for word in threats:
        if word in text_lower:
            score += 25
            reasons.append("Uses threatening language")
            suspicious_words.append(word)

    # link detection
    if "http" in text_lower or "www" in text_lower:
        score += 25
        reasons.append("Contains external link")

    # COMBO phishing intelligence
    if any(w in text_lower for w in credentials) and ("http" in text_lower or "www" in text_lower):
        score += 20
        reasons.append("Sensitive info + link combination (high phishing risk)")

    score = min(score, 100)

    # levels
    if score < 25:
        level = "LOW RISK"
    elif score < 50:
        level = "MEDIUM RISK"
    elif score < 75:
        level = "HIGH RISK"
    else:
        level = "CRITICAL FRAUD"

    return score, level, reasons, suspicious_words


def ai_probability(score):
    if score < 25:
        return 20
    elif score < 50:
        return 45
    elif score < 75:
        return 70
    else:
        return 90


def detect_credentials(text):
    findings = []

    if re.search(r"\S+@\S+", text):
        findings.append("Email detected")

    if re.search(r"\b\d{4,6}\b", text):
        findings.append("Possible OTP detected")

    if re.search(r"\b\d{16}\b", text):
        findings.append("Possible card number detected")

    return findings


def check_phishing_url(text):
    alerts = []

    urls = re.findall(r'(https?://\S+)', text.lower())

    suspicious_tlds = [".xyz", ".top", ".ru", ".tk"]
    suspicious_words = ["secure", "verify", "login", "account"]

    for url in urls:
        for tld in suspicious_tlds:
            if tld in url:
                alerts.append(f"Suspicious domain extension in {url}")

        for word in suspicious_words:
            if word in url:
                alerts.append(f"Phishing keyword in URL: {url}")

    return alerts


def analyze_message(text):
    score, level, reasons, words = fraud_detector(text)
    ai_prob = ai_probability(score)
    creds = detect_credentials(text)
    urls = check_phishing_url(text)

    # explanation text
    explanation = "This message appears safe."

    if score >= 50:
        explanation = "⚠️ This message shows phishing characteristics. Avoid sharing personal or banking details."

    if score >= 75:
        explanation = "🚨 Strong fraud indicators detected! Do NOT click links or share OTP/password."

    return score, level, reasons, words, ai_prob, creds, urls, explanation

    return score, level, reasons, words, ai_prob, creds, urls
