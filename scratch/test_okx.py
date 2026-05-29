import os
import hmac
import base64
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OKX_API_KEY", "")
secret_key = os.environ.get("OKX_SECRET_KEY", "")
passphrase = os.environ.get("OKX_PASSPHRASE", "")

def get_timestamp():
    # Format: yyyy-MM-ddTHH:mm:ss.sssZ
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def sign(message, secret_key):
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    return base64.b64encode(mac.digest()).decode('utf-8')

def test_balance(use_demo):
    path = "/api/v5/account/balance"
    timestamp = get_timestamp()
    message = timestamp + "GET" + path
    signature = sign(message, secret_key)
    
    headers = {
        'Content-Type': 'application/json',
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
    }
    if use_demo:
        headers['x-simulated-option'] = '1'
        
    url = f"https://www.okx.com{path}"
    res = requests.get(url, headers=headers)
    print(f"Demo={use_demo} - Timestamp: {timestamp} - Status: {res.status_code}")
    try:
        print("Data:", res.json())
    except:
        print("Raw text:", res.text)

if __name__ == "__main__":
    test_balance(use_demo=True)
    test_balance(use_demo=False)
