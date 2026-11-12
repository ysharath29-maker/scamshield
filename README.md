# 🛡️ ScamShield: AI-Based Fake UPI / SMS Scam Detector

ScamShield checks whether an SMS or payment message looks like a scam. It gives a risk level (Low / Medium / High), a scam probability, the red flags it found, and advice on what to do.

## Problem
Millions of people in India receive fake KYC, lottery, refund and UPI "collect request" messages every day. Most users cannot tell a genuine message from a fake one, and they lose money in seconds.

## How it works
1. **Clean** the text (lowercase, replace links, phone numbers and amounts with placeholders).
2. **Model:** TF-IDF (word and word-pair features) + Logistic Regression gives a scam probability.
3. **Rules:** regex checks for suspicious links, OTP/PIN requests, urgency, prizes, upfront fees and KYC/Aadhaar/PAN updates.
4. **Hybrid risk score:** the probability and the rule flags are combined into Low / Medium / High.

## Data
- Public SMS Spam Collection (UK/US style messages).
- About 120 hand-written Indian-style scam and genuine messages (bank alerts, OTPs, delivery updates, fake KYC, UPI scams).

## Results (5-fold cross-validation)
- UK/US messages: F1 about 0.93.
- Indian messages: about 91% accuracy, 1 of 60 scams missed, 10 of 60 genuine messages falsely flagged.

## Limitations
- Only about 120 Indian messages, so the Indian score is an estimate and slightly optimistic.
- Some genuine bank credit alerts may get a Medium score.
- It is a learning project and should be used as a helper, not as the final word.

## Files
- `main.py` and `engine.py`: FastAPI website and the scam-checking logic
- `static/`: the web page (works on phones and can be installed like an app)
- `app.py`: optional Streamlit demo (needs `pip install streamlit`)
- `scamshield_model_v3.pkl`, `scamshield_vectorizer_v3.pkl`: trained model and vectorizer
- `requirements.txt`: libraries (scikit-learn is pinned to the version used for training)

## Run it
```
pip install -r requirements.txt
uvicorn main:app --reload
```
Use Python 3.12 or lower, because very new Python versions may not support the pinned scikit-learn.

## Tech
Python, pandas, scikit-learn, FastAPI, HTML/CSS/JS, Google Colab.
