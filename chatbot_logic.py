from scraper import search_products

def get_initial_state():
    # Initial message: centered, no input box, only quick replies for gender
    return {
        "bot_message": "Welcome to Muskbliss!<br>How can I help you?",
        "session": {},
        "products": [],
        "options": [
            {"text": "Male", "value": "male"},
            {"text": "Female", "value": "female"},
            {"text": "Unisex", "value": "unisex"}
        ],
        "centered": True,
        "show_input": False
    }

def get_next_prompt(user_message, session):
    # 1. Gender
    if not session.get("gender"):
        gender = user_message.strip().lower()
        if gender not in ["male", "female", "unisex"]:
            return ("Please choose: Male, Female, or Unisex.", session, [], [
                {"text": "Male", "value": "male"},
                {"text": "Female", "value": "female"},
                {"text": "Unisex", "value": "unisex"}
            ], False, False)
        session["gender"] = gender
        return ("Great! May I know your age?", session, [], None, False, True)

    # 2. Age
    if not session.get("age"):
        try:
            age = int(user_message.strip())
            if age < 1 or age > 100:
                raise ValueError
            session["age"] = age
            return ("What is the occasion or vibe?", session, [], [
                {"text": "Romantic", "value": "romantic"},
                {"text": "Date", "value": "date"},
                {"text": "Festival", "value": "festival"},
                {"text": "Summer", "value": "summer"},
                {"text": "Winter", "value": "winter"}
            ], False, False)
        except Exception:
            return ("Please enter a valid age (e.g., 22).", session, [], None, False, True)

    # 3. Occasion
    if not session.get("occasion"):
        occasion = user_message.strip().lower()
        valid_occasions = ["romantic", "date", "festival", "summer", "winter"]
        if occasion not in valid_occasions:
            return ("Choose an occasion:", session, [], [
                {"text": "Romantic", "value": "romantic"},
                {"text": "Date", "value": "date"},
                {"text": "Festival", "value": "festival"},
                {"text": "Summer", "value": "summer"},
                {"text": "Winter", "value": "winter"}
            ], False, False)
        session["occasion"] = occasion
        # Show typing effect:
        return ("Let me find the perfect fragrances for you...", session, [], None, False, False)

    # 4. Suggest products
    products = recommend_products(session)
    msg = "Here are some fragrances recommended for you!"
    if not products:
        note = session.get("occasion", "")
        search_link = f"https://muskbliss.com/search?q={note}"
        msg = f"Sorry, I couldn't find products for your preferences.<br>Try browsing here: <a href='{search_link}' target='_blank'>{search_link}</a>"
    return (msg, session, products, None, False, False)

def recommend_products(session):
    gender = session.get("gender")
    occasion = session.get("occasion")
    return search_products(gender, occasion)    