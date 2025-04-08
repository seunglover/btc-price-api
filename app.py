from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/get_btc_price", methods=["GET"])
def get_btc_price():
    url = "https://api.bybit.com/v5/market/tickers"
    params = {
        "category": "linear",
        "symbol": "BTCUSDT"
    }
    res = requests.get(url, params=params)

    if res.status_code == 200:
        data = res.json()["result"]["list"][0]
        return jsonify({
            "symbol": data["symbol"],
            "price": float(data["lastPrice"]),
            "change": float(data["price24hPcnt"]) * 100,
            "volume": float(data["turnover24h"])
        })
    else:
        return jsonify({"error": "시세 조회 실패"}), 500

@app.route("/")
def serve_static_html():
    # 시세 가져오기
    url = "https://api.bybit.com/v5/market/tickers"
    params = {"category": "linear", "symbol": "BTCUSDT"}
    res = requests.get(url, params=params)

    if res.status_code == 200:
        data = res.json()["result"]["list"][0]
        price = float(data["lastPrice"])
        change = float(data["price24hPcnt"]) * 100
        volume = float(data["turnover24h"])
    else:
        price = change = volume = "ERROR"

    # 서버에서 HTML 직접 렌더링
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head><meta charset="UTF-8"><title>BTC Price (Static)</title></head>
    <body>
        <div id="PRICE">{price}</div>
        <div id="CHANGE">{change}</div>
        <div id="VOLUME">{volume}</div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
