import os, requests

MERCHANT_ID = os.getenv("ZARINPAL_MERCHANT", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
CALLBACK_URL = "http://127.0.0.1:8000/payment/verify/"

SANDBOX_API = "https://sandbox.zarinpal.com/pg/v4/payment"

def request_payment(amount, description, email):
    data = {
        "MerchantID": MERCHANT_ID,
        "Amount": amount,
        "CallbackURL": CALLBACK_URL,
        "Description": description,
        "Email": email,
    }
    r = requests.post(f"{SANDBOX_API}/request.json", json=data, timeout=10)
    r.raise_for_status()
    res = r.json()["data"]
    if res["code"] != 100:
        raise ValueError(f"Zarinpal error code {res['code']}")
    return res["authority"], f"https://sandbox.zarinpal.com/pg/StartPay/{res['authority']}"

def verify_payment(authority, amount):
    data = {"MerchantID": MERCHANT_ID, "Amount": amount, "Authority": authority}
    r = requests.post(f"{SANDBOX_API}/verify.json", json=data, timeout=10)
    r.raise_for_status()
    res = r.json()["data"]
    return res["code"] == 100, res.get("ref_id")
