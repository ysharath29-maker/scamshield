import re
from pathlib import Path

import joblib
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

BASE = Path(__file__).parent
model = joblib.load(BASE / "scamshield_model_v3.pkl")
vec = joblib.load(BASE / "scamshield_vectorizer_v3.pkl")
feature_names = np.array(vec.get_feature_names_out())

ADVICE = {
    "HIGH": [
        "Do not click any link, call any number or share any OTP/PIN.",
        "Never enter your UPI PIN to receive money.",
        "Report it at cybercrime.gov.in or call 1930.",
    ],
    "MEDIUM": [
        "Do not act on the message directly.",
        "Check with your bank or service using its official app or website.",
    ],
    "LOW": [
        "Looks fine, but stay careful. Banks never ask for your OTP, PIN or password.",
    ],
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", " urltoken ", text)
    text = re.sub(r"\b\d{10,}\b", " phonetoken ", text)
    text = re.sub(r"[£$₹]", " moneytoken ", text)
    text = re.sub(r"\d+", " numtoken ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def get_flags(msg):
    m = msg.lower()
    flags = []
    if re.search(r"http|www\.|\.xyz|\.top|\.live|\.cc\b|\.online|\.apk", m):
        flags.append("Contains a suspicious link")
    if (re.search(r"\b(otp|pin|cvv|password)\b", m)
            and re.search(r"\b(share|enter|send|reply)\b", m)
            and not re.search(r"(do not|don't|never)\s+share", m)):
        flags.append("Asks for OTP / PIN / password")
    if re.search(r"urgent|immediately|last chance|expire|blocked|suspended|deactivat|freez|disconnect|within \d+ (hours|hrs)", m):
        flags.append("Creates urgency or fear")
    if re.search(r"lottery|lucky draw|winner|you won|prize|cashback|refund|reward", m):
        flags.append("Promises a prize, refund or reward")
    if re.search(r"(processing|registration|delivery|customs|insurance|booking) (fee|charge)|pay rs", m):
        flags.append("Asks you to pay a fee first")
    if re.search(r"\bkyc\b|aadhaar|\bpan\b", m) and re.search(r"update|verify|link|expired|pending|suspend", m):
        flags.append("Asks to update KYC / Aadhaar / PAN")
    if "collect request" in m:
        flags.append("UPI collect request")
    return flags


def top_words(msg, n=5):
    v = vec.transform([clean_text(msg)])
    contrib = v.toarray()[0] * model.coef_[0]
    words = []
    for i in np.argsort(contrib)[::-1]:
        if contrib[i] <= 0 or len(words) == n:
            break
        f = feature_names[i]
        if "token" in f or all(p in ENGLISH_STOP_WORDS for p in f.split()):
            continue
        words.append(f)
    return words


def analyze(msg):
    p = float(model.predict_proba(vec.transform([clean_text(msg)]))[0][1])
    flags = get_flags(msg)
    level = "HIGH" if p >= 0.5 else "MEDIUM" if p >= 0.3 else "LOW"
    if level == "MEDIUM" and len(flags) >= 2:
        level = "HIGH"
    if level == "LOW" and len(flags) >= 3:
        level = "MEDIUM"
    return {"score": round(p, 3), "level": level, "flags": flags,
            "words": top_words(msg), "advice": ADVICE[level]}
