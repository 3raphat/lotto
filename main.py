import random
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Lottery's Festival Fair</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        .container {
            text-align: center;
            padding: 20px;
        }
        .item {
            font-size: 240px;
            font-weight: bold;
            color: #333;
            margin: 20px 0;
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        @keyframes spin {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
        }
        .spinning {
            animation: spin 0.1s linear infinite;
            overflow: hidden;
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lottery's Festival Fair</h1>
        <div class="item" id="itemDisplay">---</div>
        <button onclick="generateNew()" id="generateBtn">Generate New Item</button>
    </div>

    <script>
        function generateNew() {
            const display = document.getElementById('itemDisplay');
            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            
            // Start spinning animation
            display.classList.add('spinning');
            
            // Generate random numbers during animation
            const interval = setInterval(() => {
                const num = Math.floor(Math.random() * (0x4FF - 0x100 + 1)) + 0x100;
                display.textContent = num.toString(16).toUpperCase();
            }, 50);
            
            // Fetch actual result
            fetch('/get_item')
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        clearInterval(interval);
                        display.classList.remove('spinning');
                        display.textContent = data.item;
                        btn.disabled = false;
                    }, 2000);
                });
        }
    </script>
</body>
</html>
"""


def get_random_item():
    try:
        with open("data.txt", "r") as file:
            except_items = [line.strip() for line in file.readlines()]

        # Generate numbers from 100 to 4FF (hex)
        all_items = [hex(i)[2:].upper() for i in range(0x100, 0x4FF)]

        # Filter out excepted items
        available_items = [item for item in all_items if item not in except_items]

        if not available_items:
            return None

        return random.choice(available_items)
    except FileNotFoundError:
        return None


@app.route("/")
def home():
    item = get_random_item()
    return render_template_string(HTML_TEMPLATE, item=item)


@app.route("/get_item")
def get_item():
    item = get_random_item()
    return jsonify({"item": item if item else "No items available"})


if __name__ == "__main__":
    app.run(debug=True)
