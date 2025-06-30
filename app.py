from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# HTML Template
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Refund Calculator</title>
    <style>
        body { font-family: Arial; padding: 40px; direction: rtl; }
        label, input { display: block; margin-bottom: 10px; }
        input { padding: 5px; width: 300px; }
        h2, h3 { color: #333; }
    </style>
</head>
<body>
    <h2>حاسبة الاسترجاع</h2>
    <form method="post">
        <label>المبيعات بالدولار (USD):</label>
        <input type="number" step="0.01" name="sales_usd" required>

        <label>المبيعات بالدينار (IQD):</label>
        <input type="number" step="1" name="sales_iqd" required>

        <label>الاسترجاع المطلوب بالدولار (USD):</label>
        <input type="number" step="0.01" name="refund_usd" required>

        <input type="submit" value="احسب الاسترجاع">
    </form>

    {% if result %}
        <h3>النتائج:</h3>
        <p>💱 سعر الصرف: {{ result.exchange_rate }}</p>
        <p>📉 سعر الصرف المعدل: {{ result.adjusted_rate }}</p>
        <p>💰 الاسترجاع بالدينار: <strong>{{ result.refund_iqd }}</strong></p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def refund_calculator():
    result = None
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
        except Exception as e:
            result = {"exchange_rate": "0", "adjusted_rate": "0", "refund_iqd": f"خطأ: {str(e)}"}

    return render_template_string(template, result=result)

# ✅ مطلوب لـ Render حتى يشتغل التطبيق على الإنترنت
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
