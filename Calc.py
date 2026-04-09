from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# EMI Calculation Function
def calculate_emi(p, r, y):
    r = r / (12 * 100)
    n = y * 12
    x = (1 + r) ** n

    emi = (p * r * x) / (x - 1)
    total = emi * n
    interest = total - p

    return emi, interest, total


# Serve Frontend
@app.route('/')
def home():
    return render_template("index.html")


# API Route
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()

        p = float(data['principal'])
        r = float(data['rate'])
        y = float(data['years'])

        emi, interest, total = calculate_emi(p, r, y)

        return jsonify({
            "emi": round(emi, 2),
            "interest": round(interest, 2),
            "total": round(total, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Run App (Render compatible)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))  # Render gives this
    app.run(host="0.0.0.0", port=port)