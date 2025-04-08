from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/get_btc_price", methods=["GET"])
def get_btc_price():
    url = "https://api.bybit.com/v2/public/tickers"
    params = {"symbol": "BTCUSDT"}  # 다른 코인: ETHUSDT, XRPUSDT 등
    res = requests.get(url, params=params)

    if res.status_code == 200:
        data = res.json()["result"][0]
        return jsonify({
            "symbol": data["symbol"],
            "price": float(data["last_price"]),
            "change": float(data["percent_change_24h"]),
            "volume": float(data["turnover_24h"])
        })
    else:
        return jsonify({"error": "시세 조회 실패"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
