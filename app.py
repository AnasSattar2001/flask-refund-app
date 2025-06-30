from flask import Flask, request, render_template_string

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Refund Calculator</title>
</head>
<body>
    <h2>حاسبة الاسترجاع</h2>
    <form method="post">
        <label>المبيعات بالدولار (USD):</label><br>
        <input type="number" step="0.01" name="sales_usd"><br><br>
        
        <label>المبيعات بالدينار (IQD):</label><br>
        <input type="number" step="1" name="sales_iqd"><br><br>
        
        <label>الاسترجاع المطلوب بالدولار (USD):</label><br>
        <input type="number" step="0.01" name="refund_usd"><br><br>
        
        <input type="submit" value="احسب الاسترجاع"><br><br>
    </form>

    {% if result %}
        <h3>النتائج:</h3>
        <p>سعر الصرف: {{ result.exchange_rate }}</p>
        <p>سعر الصرف المعدل: {{ result.adjusted_rate }}</p>
        <p>الاسترجاع بالدينار: <strong>{{ result.refund_iqd }}</strong></p>
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
            result = {"error": str(e)}

    return render_template_string(template, result=result)

if __name__ == "__main__":
    app.run(debug=True)
