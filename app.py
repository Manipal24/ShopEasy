from flask import Flask, render_template, jsonify, request, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "shopeasy123"

products = [
    {"id": 1, "name": "Rice (1kg)", "price": 60, "category": "Grocery", "image": "🌾"},
    {"id": 2, "name": "Wheat (1kg)", "price": 45, "category": "Grocery", "image": "🌿"},
    {"id": 3, "name": "Sugar (1kg)", "price": 50, "category": "Grocery", "image": "🍬"},
    {"id": 4, "name": "Mobile Phone", "price": 8999, "category": "Electronics", "image": "📱"},
    {"id": 5, "name": "Headphones", "price": 599, "category": "Electronics", "image": "🎧"},
    {"id": 6, "name": "T-Shirt", "price": 299, "category": "Clothing", "image": "👕"},
]

@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] * item["qty"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

@app.route("/orders")
def orders():
    my_orders = session.get("orders", [])
    my_orders = list(reversed(my_orders))
    return render_template("orders.html", orders=my_orders)

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.json
    cart = session.get("cart", [])
    for item in cart:
        if item["id"] == data["id"]:
            item["qty"] += 1
            session["cart"] = cart
            return jsonify({"success": True, "message": "Quantity updated!"})
    cart.append({
        "id": data["id"],
        "name": data["name"],
        "price": data["price"],
        "qty": 1
    })
    session["cart"] = cart
    return jsonify({"success": True, "message": "Added to cart!"})

@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    data = request.json
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != data["id"]]
    session["cart"] = cart
    return jsonify({"success": True})

@app.route("/place-order", methods=["POST"])
def place_order():
    cart = session.get("cart", [])
    if not cart:
        return jsonify({"success": False, "message": "Cart empty!"})
    
    total = sum(item["price"] * item["qty"] for item in cart)
    
    order = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "products": cart,
        "total": total,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "status": "Confirmed ✅"
    }
    
    orders = session.get("orders", [])
    orders.append(order)
    session["orders"] = orders
    session["cart"] = []
    
    return jsonify({"success": True, "message": "Order placed successfully!"})

if __name__ == "__main__":
    app.run(debug=True)