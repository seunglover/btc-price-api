from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/get_btc_price", methods=["GET"])
def get_btc_price():
    url = "https://api.upbit.com/v1/ticker"
    params = {"markets": "KRW-BTC"}
    res = requests.get(url, params=params)

    if res.status_code == 200:
        data = res.json()[0]
        return jsonify({
            "price": data["trade_price"],
            "change": round(data["signed_change_rate"] * 100, 2),
            "volume": round(data["acc_trade_volume_24h"], 2)
        })
    else:
        return jsonify({"error": "시세 조회 실패"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
