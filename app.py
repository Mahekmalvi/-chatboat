from flask import Flask, render_template, request, jsonify
import requests, uuid, re

app = Flask(__name__)
STORE = "https://muskbliss.com"

# -------- Fetch product from Shopify --------
def fetch_product(handle):
    url = f"{STORE}/products/{handle}.json"
    r = requests.get(url, timeout=8)
    if r.status_code != 200:
        return None
    p = r.json()["product"]
    v = p["variants"][0]
    return {
        "title": p["title"],
        "subtitle": (p.get("body_html") or "")[:100] + "...",
        "price": f"₹{v['price']}",
        "image": p["images"][0]["src"] if p["images"] else "",
        "url": f"{STORE}/products/{handle}?utm_source=chatbot",
        "pay": f"{STORE}/cart/add?id={v['id']}&quantity=1"
    }

# -------- Sample product handles (add your own) --------
PRODUCTS = ["rose-eden", "citrus-spark", "amber-ember", "ocean-mist"]

def recommend(gender, age, occasion, notes=None):
    # TODO: add real logic; here just return all products for demo
    return [fetch_product(h) for h in PRODUCTS]

# -------- Memory store --------
SESSIONS = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.post("/chat")
def chat():
    data = request.json
    cid = data.get("cid") or str(uuid.uuid4())
    msg = (data.get("msg") or "").lower().strip()
    sess = SESSIONS.setdefault(cid, {"step": "gender", "answers": {}, "history": []})

    reply, cards, step = None, [], sess["step"]

    if step == "gender":
        sess["answers"]["gender"] = msg
        sess["step"] = "age"
        reply = "Please enter your age (numbers only)."

    elif step == "age":
        if not re.fullmatch(r"\d{1,3}", msg):
            reply = "Age must be numbers only. Try again."
        else:
            sess["answers"]["age"] = int(msg)
            sess["step"] = "occasion"
            reply = "Great! What's the occasion? (Office, Festive, Romantic date, etc.)"

    elif step == "occasion":
        sess["answers"]["occasion"] = msg
        sess["step"] = "notes"
        reply = "Any preferred notes? (e.g., Floral, Citrus) or type Skip."

    elif step == "notes":
        if msg != "skip":
            sess["answers"]["notes"] = msg.split(",")
        reply = "Here are my suggestions for you:"
        cards = recommend(**sess["answers"])
        sess["step"] = "done"

    else:
        reply = "You can say: Find fragrance, Best perfume, or Seasonal picks."

    sess["history"].append({"user": msg, "bot": reply})
    return jsonify({"cid": cid, "reply": reply, "cards": cards, "history": sess["history"]})
