import re

def fraud_detector(text):
    score = 0
    reasons = []
    suspicious_words = []

    urgency = ["urgent", "immediately", "act now"]
    authority = ["bank", "income tax", "police", "rbi"]
    credentials = ["otp", "password", "cvv", "pin"]
    threats = ["blocked", "suspended", "legal action"]

    text_lower = text.lower()

    for word in urgency:
        if word in text_lower:
            score += 15
            reasons.append("Urgency pressure detected")
            suspicious_words.append(word)

    for word in authority:
        if word in text_lower:
            score += 20
            reasons.append("Authority impersonation")
            suspicious_words.append(word)

    for word in credentials:
        if word in text_lower:
            score += 30
            reasons.append("Sensitive info requested")
            suspicious_words.append(word)

    for word in threats:
        if word in text_lower:
            score += 20
            reasons.append("Threat language detected")
            suspicious_words.append(word)

    if "http" in text_lower or "www" in text_lower:
        score += 20
        reasons.append("Suspicious link detected")

    score = min(score, 100)

    if score <= 30:
        level = "SAFE"
    elif score <= 60:
        level = "SUSPICIOUS"
    elif score <= 80:
        level = "HIGH RISK"
    else:
        level = "CRITICAL FRAUD"

    return score, level, reasons, suspicious_words


def ai_probability(score):
    return min(95, score + 10)


def detect_credentials(text):
    findings = []

    if re.search(r"\S+@\S+", text):
        findings.append("Email detected")

    if re.search(r"\b\d{4,6}\b", text):
        findings.append("OTP detected")

    if re.search(r"\b\d{16}\b", text):
        findings.append("Card number detected")

    return findings


def check_phishing_url(text):
    bad_domains = ["bit.ly", "tinyurl", "verify-account", "free-login"]
    alerts = []

    for d in bad_domains:
        if d in text.lower():
            alerts.append("Shortened/suspicious URL detected")

    return alerts


def analyze_message(text):
    score, level, reasons, words = fraud_detector(text)
    ai_prob = ai_probability(score)
    creds = detect_credentials(text)
    urls = check_phishing_url(text)

    return score, level, reasons, words, ai_prob, creds, urls
