import re

def fraud_detector(text):

    score=0
    reasons=[]
    suspicious_words=[]
    t=text.lower()

    urgency=["urgent","immediately","act now","limited time"]
    authority=["bank","income tax","police","rbi","sbi","hdfc","icici"]
    credentials=["otp","password","cvv","pin","verify otp"]
    threats=["blocked","suspended","legal action","account locked"]

    for w in urgency:
        if w in t:
            score+=20
            reasons.append("Creates urgency pressure")
            suspicious_words.append(w)

    for w in authority:
        if w in t:
            score+=20
            reasons.append("Possible authority impersonation")
            suspicious_words.append(w)

    for w in credentials:
        if w in t:
            score+=40
            reasons.append("Requests sensitive information")
            suspicious_words.append(w)

    for w in threats:
        if w in t:
            score+=25
            reasons.append("Uses threatening language")
            suspicious_words.append(w)

    if "http" in t or "www" in t:
        score+=25
        reasons.append("Contains external link")

    if any(w in t for w in credentials) and ("http" in t or "www" in t):
        score+=20
        reasons.append("Sensitive info + link combination")

    score=min(score,100)

    if score<25: level="LOW RISK"
    elif score<50: level="MEDIUM RISK"
    elif score<75: level="HIGH RISK"
    else: level="CRITICAL FRAUD"

    return score,level,reasons,suspicious_words


def ai_probability(score):

    if score<25:return 20
    elif score<50:return 45
    elif score<75:return 70
    else:return 90


def detect_credentials(text):

    findings=[]

    if re.search(r"\S+@\S+",text):
        findings.append("Email detected")

    if re.search(r"\b\d{4,6}\b",text):
        findings.append("Possible OTP detected")

    if re.search(r"\b\d{16}\b",text):
        findings.append("Possible card number detected")

    return findings


def check_phishing_url(text):

    alerts=[]
    urls=re.findall(r'(https?://\S+)',text.lower())

    suspicious_tlds=[".xyz",".top",".ru",".tk"]
    suspicious_words=["secure","verify","login","account"]

    for url in urls:

        for tld in suspicious_tlds:
            if tld in url:
                alerts.append(f"Suspicious domain extension in {url}")

        for w in suspicious_words:
            if w in url:
                alerts.append(f"Phishing keyword in URL: {url}")

    return alerts


def analyze_message(text):

    score,level,reasons,words=fraud_detector(text)
    ai_prob=ai_probability(score)
    creds=detect_credentials(text)
    urls=check_phishing_url(text)

    explanation="This message appears safe."

    if score>=50:
        explanation="⚠️ This message shows phishing characteristics. Avoid sharing personal details."

    if score>=75:
        explanation="🚨 Strong fraud indicators detected! Do NOT click links or share OTP."

    return score,level,reasons,words,ai_prob,creds,urls,explanation

