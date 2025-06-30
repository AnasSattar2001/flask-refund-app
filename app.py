from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>حاسبة الاسترجاع</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #fff;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background: #fff;
            padding: 40px 60px;
            border-radius: 16px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.2);
            text-align: center;
            width: 100%;
            max-width: 500px;
        }
        h2 {
            color: #c40000;
            margin-bottom: 30px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            text-align: right;
        }
        input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 16px;
            background-color: #f9f9f9;
        }
        input[type="submit"] {
            background-color: #c40000;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #ff3333;
        }
        .result {
            margin-top: 30px;
            background-color: #fff1f1;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #c40000;
            color: #b00000;
            font-size: 18px;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>حاسبة الاسترجاع</h2>
    <form method="post">
        <label>المبيعات بالدولار (USD):</label>
        <input type="number" step="0.01" name="sales_usd" required value="{{ values.sales_usd or '' }}">

        <label>المبيعات بالدينار (IQD):</label>
        <input type="number" step="1" name="sales_iqd" required value="{{ values.sales_iqd or '' }}">

        <label>الاسترجاع بالدولار (USD):</label>
        <input type="number" step="0.01" name="refund_usd" required value="{{ values.refund_usd or '' }}">

        <input type="submit" value="احسب الاسترجاع">
    </form>

    {% if result %}
        <div class="result">
            <p>💱 سعر الصرف: {{ result.exchange_rate }}</p>
            <p>📉 سعر الصرف المعدل: {{ result.adjusted_rate }}</p>
            <p>💰 الاسترجاع بالدينار: <strong>{{ result.refund_iqd }}</strong></p>
        </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def refund_calculator():
    result = None
    values = {"sales_usd": "", "sales_iqd": "", "refund_usd": ""}

    if request.method == "POST":
        try:
            sales_usd = float(request.form["sales_usd"])
            sales_iqd = float(request.form["sales_iqd"])
            refund_usd = float(request.form["refund_usd"])

            exchange_rate = sales_iqd / sales_usd if sales_usd != 0 else 0
            adjusted_rate = exchange_rate - 20
            refund_iqd = refund_usd * adjusted_rate

            result = {
                "exchange_rate": f"{exchange_rate:.2f}",
                "adjusted_rate": f"{adjusted_rate:.2f}",
                "refund_iqd": f"IQD {refund_iqd:,.0f} دينار"
            }

            # نحتفظ بالقيم اللي دخلها المستخدم
            values = {
                "sales_usd": request.form["sales_usd"],
                "sales_iqd": request.form["sales_iqd"],
                "refund_usd": request.form["refund_usd"]
            }

        except Exception as e:
            result = {"exchange_rate": "0", "adjusted_rate": "0", "refund_iqd": f"خطأ: {str(e)}"}

    return render_template_string(template, result=result, values=values)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
