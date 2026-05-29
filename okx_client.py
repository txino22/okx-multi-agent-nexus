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
mode = os.environ.get("OKX_MODE", "demo").lower()

def get_timestamp():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def sign(message, secret):
    mac = hmac.new(bytes(secret, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    return base64.b64encode(mac.digest()).decode('utf-8')

def get_headers(method, path, body=''):
    if not api_key or not secret_key or not passphrase:
        return None
    timestamp = get_timestamp()
    message = timestamp + method + path + body
    try:
        signature = sign(message, secret_key)
    except Exception:
        return None
        
    headers = {
        'Content-Type': 'application/json',
        'OK-ACCESS-KEY': api_key,
        'OK-ACCESS-SIGN': signature,
        'OK-ACCESS-TIMESTAMP': timestamp,
        'OK-ACCESS-PASSPHRASE': passphrase,
    }
    if mode == "demo":
        headers['x-simulated-option'] = '1'
    return headers

def get_okx_balance():
    """Fetches real account balance from OKX, with simulated fallback if keys are missing/invalid."""
    headers = get_headers("GET", "/api/v5/account/balance")
    if headers:
        try:
            url = "https://www.okx.com/api/v5/account/balance"
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get("code") == "0":
                    details = data["data"][0]["details"]
                    # Sum up values
                    total_eq = float(data["data"][0].get("totalEq", 0))
                    assets = []
                    for item in details:
                        eq = float(item.get("eq", 0))
                        if eq > 0:
                            assets.append({
                                "ccy": item["ccy"],
                                "eq": eq,
                                "eqUsd": float(item.get("eqUsd", 0))
                            })
                    if not assets: # If empty list, put fallback
                        raise ValueError("No assets found")
                    return {"total_eq": total_eq, "assets": assets, "is_mock": False}
        except Exception:
            pass
            
    # Mock Fallback
    return {
        "total_eq": 42150.80,
        "assets": [
            {"ccy": "BTC", "eq": 0.452, "eqUsd": 19052.16, "change": "+1.2%"},
            {"ccy": "ETH", "eq": 4.20, "eqUsd": 9450.00, "change": "+3.4%"},
            {"ccy": "SOL", "eq": 120.5, "eqUsd": 2410.00, "change": "-0.5%"},
            {"ccy": "USDT", "eq": 11238.64, "eqUsd": 11238.64, "change": "0.0%"}
        ],
        "is_mock": True
    }

def get_okx_active_bots():
    """Fetches active algorithm orders (Grid & DCA bots) from OKX, with simulated fallback."""
    # We query active algo orders endpoint
    headers = get_headers("GET", "/api/v5/grid/active-algo-algo-orders?algoOrdType=grid")
    if headers:
        try:
            url = "https://www.okx.com/api/v5/grid/active-algo-algo-orders?algoOrdType=grid"
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get("code") == "0":
                    raw_orders = data.get("data", [])
                    bots = []
                    for o in raw_orders:
                        bots.append({
                            "algoId": o.get("algoId"),
                            "algoOrdType": o.get("algoOrdType"),
                            "instId": o.get("instId"),
                            "state": o.get("state").upper(),
                            "upl": float(o.get("upl", 0)),
                            "gridNum": o.get("gridNum"),
                            "maxPrice": o.get("maxPrice"),
                            "minPrice": o.get("minPrice"),
                            "lever": o.get("lever")
                        })
                    return {"bots": bots, "is_mock": False}
        except Exception:
            pass

    # Mock Fallback
    return {
        "bots": [
            {
                "algoId": "012",
                "algoOrdType": "grid",
                "instId": "BTC-USDT",
                "state": "RUNNING",
                "upl": 152.40,
                "uplRatio": "+1.84%",
                "gridNum": "20",
                "minPrice": "68,000",
                "maxPrice": "72,000",
                "investment": "100 USDT"
            },
            {
                "algoId": "005",
                "algoOrdType": "dca",
                "instId": "ETH-USDT",
                "state": "RUNNING",
                "upl": 84.10,
                "uplRatio": "+2.12%",
                "steps": "3 Pasos",
                "multiplier": "1.5x",
                "investment": "150 USDT"
            },
            {
                "algoId": "009",
                "algoOrdType": "grid",
                "instId": "SOL-USDT",
                "state": "PAUSED",
                "upl": -10.50,
                "uplRatio": "-0.45%",
                "gridNum": "15",
                "minPrice": "140",
                "maxPrice": "180",
                "investment": "50 USDT"
            }
        ],
        "is_mock": True
    }
