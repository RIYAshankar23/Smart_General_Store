import ast
from pathlib import Path

import pandas as pd
import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart General Store",
    page_icon="🛒",
    layout="wide",
)

# =========================================================
# CSS DESIGN
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@600;700;800;900&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Nunito', sans-serif;
}

/* ---------- Background ---------- */
.stApp {
    background: linear-gradient(135deg, #fff7d6 0%, #dcfce7 30%, #dbeafe 65%, #fce7f3 100%);
    background-attachment: fixed;
}
.block-container {
    max-width: 1400px;
    padding-top: 24px;
    padding-bottom: 60px;
}

/* ---------- Headings ---------- */
h1, h2, h3, h4 {
    font-family: 'Fredoka', sans-serif !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    line-height: 1.3 !important;
}

/* ---------- HERO BANNER ---------- */
.hero {
    background: linear-gradient(120deg, #16a34a 0%, #84cc16 25%, #f59e0b 50%, #ef4444 75%, #8b5cf6 100%);
    border-radius: 32px;
    padding: 34px 24px 28px 24px;
    text-align: center;
    box-shadow: 0 14px 40px rgba(22, 163, 74, 0.35);
    margin-bottom: 22px;
    border: 4px solid rgba(255, 255, 255, 0.7);
}
.store-title {
    font-family: 'Fredoka', sans-serif;
    font-size: clamp(2.6rem, 7vw, 5.6rem);
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
    letter-spacing: 1px;
    text-shadow: 4px 4px 0 rgba(0, 0, 0, 0.22);
    margin: 0;
}
.store-subtitle {
    font-size: clamp(1.1rem, 2.2vw, 1.7rem);
    font-weight: 800;
    color: #ffffff;
    margin-top: 10px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}
.chip-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    margin-top: 18px;
}
.chip {
    background: #ffffff;
    color: #0f172a;
    font-size: 1.15rem;
    font-weight: 900;
    padding: 8px 20px;
    border-radius: 999px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* ---------- Section titles ---------- */
.section-title {
    font-family: 'Fredoka', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #14532d;
    margin: 6px 0 4px 0;
}
.sub-title {
    font-size: 22px;
    font-weight: 800;
    color: #0f172a;
    margin: 4px 0;
}

/* ---------- Category icon strip ---------- */
.cat-strip {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 14px;
    margin: 6px 0 22px 0;
}
.cat-tile {
    border-radius: 22px;
    padding: 14px 6px 10px 6px;
    text-align: center;
    color: #ffffff;
    font-weight: 900;
    font-size: 1.05rem;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.18);
    transition: transform 0.2s;
}
.cat-tile:hover { transform: translateY(-4px) scale(1.05); }
.cat-icon { font-size: 3.4rem; line-height: 1.1; display: block; }
.cat-1 { background: linear-gradient(135deg, #22c55e, #15803d); }
.cat-2 { background: linear-gradient(135deg, #f97316, #c2410c); }
.cat-3 { background: linear-gradient(135deg, #38bdf8, #0369a1); }
.cat-4 { background: linear-gradient(135deg, #f472b6, #be185d); }
.cat-5 { background: linear-gradient(135deg, #facc15, #ca8a04); }
.cat-6 { background: linear-gradient(135deg, #a78bfa, #6d28d9); }
.cat-7 { background: linear-gradient(135deg, #fb7185, #be123c); }

/* ---------- BIG SEARCH BAR ---------- */
.stTextInput label p {
    font-size: 28px !important;
    font-weight: 900 !important;
    color: #14532d !important;
}
div[data-baseweb="input"] {
    border-radius: 999px !important;
    border: 4px solid #16a34a !important;
    background: #ffffff !important;
    box-shadow: 0 8px 22px rgba(22, 163, 74, 0.35);
    overflow: hidden;
}
.stTextInput input {
    font-size: 26px !important;
    font-weight: 700 !important;
    min-height: 76px !important;
    padding: 12px 30px !important;
    color: #0f172a !important;
    background: #ffffff !important;
}
.stTextInput input::placeholder {
    font-size: 24px !important;
    color: #94a3b8 !important;
}

/* ---------- Buttons (general) ---------- */
.stButton button {
    font-size: 19px !important;
    font-weight: 900 !important;
    min-height: 56px;
    border-radius: 16px !important;
    white-space: nowrap;
    border: none !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #22c55e, #15803d) !important;
    box-shadow: 0 5px 14px rgba(0, 0, 0, 0.22);
    transition: all 0.18s ease;
}
.stButton button p { font-size: 19px !important; font-weight: 900 !important; }
.stButton button:hover {
    transform: translateY(-3px) scale(1.03);
    background: linear-gradient(135deg, #f97316, #ef4444) !important;
    color: #ffffff !important;
}

/* ---------- GO TO CART (extra big) ---------- */
.st-key-go_cart button {
    min-height: 84px !important;
    font-size: 30px !important;
    border-radius: 22px !important;
    background: linear-gradient(135deg, #f59e0b, #ef4444) !important;
    box-shadow: 0 10px 24px rgba(239, 68, 68, 0.45);
    animation: cartPulse 2.4s ease-in-out infinite;
}
.st-key-go_cart button p { font-size: 30px !important; font-weight: 900 !important; }
.st-key-go_cart button:hover {
    background: linear-gradient(135deg, #7c3aed, #db2777) !important;
}
@keyframes cartPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.04); }
}
@media (prefers-reduced-motion: reduce) {
    .st-key-go_cart button { animation: none; }
}

/* Continue shopping button */
.st-key-continue_shop button {
    min-height: 84px !important;
    background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
}
.st-key-continue_shop button p { font-size: 24px !important; }

/* Remove + clear buttons in red */
[class*="st-key-remove_"] button,
.st-key-clear_cart button {
    background: linear-gradient(135deg, #f87171, #dc2626) !important;
}
.st-key-clear_cart button { min-height: 68px !important; }
.st-key-clear_cart button p { font-size: 24px !important; }

/* Plus / minus buttons */
[class*="st-key-minus_"] button,
[class*="st-key-plus_"] button {
    min-height: 60px;
    font-size: 26px !important;
    background: linear-gradient(135deg, #38bdf8, #2563eb) !important;
}

/* Add to cart buttons */
[class*="st-key-add_"] button,
[class*="st-key-recommend_"] button {
    background: linear-gradient(135deg, #22c55e, #059669) !important;
}

/* ---------- Product / recommendation cards ---------- */
.card {
    padding: 18px 20px;
    border-radius: 22px;
    border: 3px solid #ffffff;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.14);
    margin-bottom: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
}
.card-product { height: 210px; }
.card-reco { height: 250px; }

.card-green  { background: linear-gradient(145deg, #dcfce7, #86efac); }
.card-orange { background: linear-gradient(145deg, #ffedd5, #fdba74); }
.card-blue   { background: linear-gradient(145deg, #e0f2fe, #7dd3fc); }
.card-pink   { background: linear-gradient(145deg, #fce7f3, #f9a8d4); }
.card-yellow { background: linear-gradient(145deg, #fef9c3, #fde047); }
.card-purple { background: linear-gradient(145deg, #ede9fe, #c4b5fd); }

.card-icon {
    font-size: 3.6rem;
    line-height: 1;
}
.card-name {
    font-size: 19px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    word-break: break-word;
}
.card-price {
    display: inline-block;
    align-self: flex-start;
    font-family: 'Fredoka', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: #ffffff;
    background: #15803d;
    padding: 2px 18px;
    border-radius: 999px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.25);
}
.card-meta {
    font-size: 15px;
    font-weight: 800;
    color: #1e293b;
}

/* ---------- Cart rows ---------- */
.cart-name {
    font-size: 22px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.3;
    word-break: break-word;
    padding-top: 4px;
}
.cart-num {
    font-size: 26px;
    font-weight: 900;
    color: #0f172a;
    text-align: center;
    padding-top: 8px;
}
.cart-head {
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
    background: linear-gradient(90deg, #16a34a, #0ea5e9);
    padding: 10px 14px;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #ffffff, #dcfce7);
    border: 3px solid #86efac;
    padding: 24px;
    border-radius: 22px;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}
[data-testid="stMetricLabel"] p {
    font-size: 22px !important;
    font-weight: 900 !important;
    color: #0f172a !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Fredoka', sans-serif !important;
    font-size: 44px !important;
    font-weight: 700 !important;
    color: #15803d !important;
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {
    border-radius: 18px;
    font-size: 20px;
    font-weight: 800;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# LOAD DATA (paths relative to this file)
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
PROCESSED = BASE_DIR / "data" / "processed"


@st.cache_data
def load_data():
    products = pd.read_csv(PROCESSED / "product_lookup.csv")
    rules = pd.read_csv(PROCESSED / "association_rules.csv")
    return products, rules


try:
    products, rules = load_data()
except FileNotFoundError as e:
    st.error(
        f"Could not find a data file: {e}. Run main.py first so that "
        "data/processed/ contains product_lookup.csv and association_rules.csv."
    )
    st.stop()

products = products.copy()
products["product_id"] = products["product_id"].astype(int)
products["product_name"] = products["product_name"].astype(str).str.strip()
products = products.drop_duplicates(subset=["product_id"]).reset_index(drop=True)

# Demo prices
products["price"] = products["product_id"].apply(lambda pid: 30 + (int(pid) % 171))

# Fast lookups
ID_TO_ROW = products.set_index("product_id").to_dict("index")
NAME_TO_ID = {}
for _pid, _name in zip(products["product_id"], products["product_name"]):
    NAME_TO_ID.setdefault(_name.lower(), _pid)

# =========================================================
# LOOK & FEEL HELPERS (emoji + card colours)
# =========================================================

CARD_COLORS = ["green", "orange", "blue", "pink", "yellow", "purple"]

EMOJI_KEYWORDS = [
    (("banana",), "🍌"),
    (("apple",), "🍎"),
    (("strawberr", "berry", "berries"), "🍓"),
    (("grape",), "🍇"),
    (("lemon", "lime"), "🍋"),
    (("orange", "citrus"), "🍊"),
    (("avocado",), "🥑"),
    (("tomato",), "🍅"),
    (("onion", "garlic"), "🧅"),
    (("potato",), "🥔"),
    (("carrot",), "🥕"),
    (("pepper", "capsicum"), "🫑"),
    (("spinach", "lettuce", "salad", "kale", "greens", "herb", "cilantro"), "🥬"),
    (("cucumber", "zucchini"), "🥒"),
    (("broccoli",), "🥦"),
    (("corn",), "🌽"),
    (("milk", "cream", "yogurt", "yoghurt", "dairy"), "🥛"),
    (("cheese",), "🧀"),
    (("egg",), "🥚"),
    (("butter",), "🧈"),
    (("bread", "bagel", "bun", "bakery", "roll"), "🍞"),
    (("cake", "cookie", "biscuit", "cracker", "brownie"), "🍪"),
    (("chocolate", "candy", "sweet"), "🍫"),
    (("ice cream", "frozen", "gelato"), "🍨"),
    (("chicken", "poultry"), "🍗"),
    (("beef", "meat", "steak", "sausage", "bacon", "ham"), "🥩"),
    (("fish", "salmon", "tuna", "shrimp", "seafood"), "🐟"),
    (("rice",), "🍚"),
    (("pasta", "noodle", "spaghetti", "macaroni"), "🍝"),
    (("chips", "snack", "popcorn", "pretzel"), "🍿"),
    (("juice", "soda", "drink", "cola", "beverage", "water"), "🧃"),
    (("coffee",), "☕"),
    (("tea",), "🍵"),
    (("wine", "beer"), "🍷"),
    (("oil", "vinegar", "sauce", "dressing", "ketchup"), "🫙"),
    (("soap", "shampoo", "detergent", "clean", "tissue", "paper", "towel"), "🧼"),
    (("baby", "diaper"), "🍼"),
    (("dog", "cat", "pet"), "🐾"),
    (("nut", "almond", "peanut", "cashew"), "🥜"),
    (("honey", "jam", "syrup"), "🍯"),
]


def product_emoji(name):
    n = str(name).lower()
    for keys, emoji in EMOJI_KEYWORDS:
        if any(k in n for k in keys):
            return emoji
    return "🛍️"


def card_color(pid):
    return CARD_COLORS[int(pid) % len(CARD_COLORS)]


# =========================================================
# RULE PARSING (handles frozenset(...), lists, plain text)
# =========================================================


def parse_items(text):
    """Turn a rule cell into a list of item names."""
    text = str(text).strip()
    if not text or text.lower() == "nan":
        return []

    s = text
    if s.startswith("frozenset(") and s.endswith(")"):
        s = s[len("frozenset("):-1]
    try:
        value = ast.literal_eval(s)
        if isinstance(value, (set, frozenset, list, tuple)):
            return [str(v).strip() for v in value]
        if isinstance(value, str):
            return [value.strip()]
    except (ValueError, SyntaxError):
        pass

    # Fallback: comma-separated, but re-join pieces that form a known name
    # (some product names contain commas).
    tokens = [t.strip() for t in text.split(",")]
    items, i = [], 0
    while i < len(tokens):
        matched = False
        for j in range(len(tokens), i, -1):
            candidate = ", ".join(tokens[i:j])
            if candidate.lower() in NAME_TO_ID:
                items.append(candidate)
                i = j
                matched = True
                break
        if not matched:
            items.append(tokens[i])
            i += 1
    return [x for x in items if x]


@st.cache_data
def prepare_rules(rules_df):
    ante_col = "antecedents_names" if "antecedents_names" in rules_df.columns else "antecedents"
    cons_col = "consequents_names" if "consequents_names" in rules_df.columns else "consequents"

    parsed = []
    for _, r in rules_df.iterrows():
        ante = frozenset(i.lower() for i in parse_items(r[ante_col]))
        cons = [i for i in parse_items(r[cons_col])]
        if not ante or not cons:
            continue
        parsed.append(
            {
                "ante": ante,
                "cons": cons,
                "confidence": float(r["confidence"]),
                "lift": float(r["lift"]),
                "support": float(r["support"]),
            }
        )
    return parsed


PARSED_RULES = prepare_rules(rules)

# =========================================================
# APRIORI RECOMMENDATION FUNCTION
# =========================================================


def get_recommendations(cart, top_n=6):
    if not cart:
        return pd.DataFrame()

    cart_names = set()
    for pid in cart.keys():
        info = ID_TO_ROW.get(int(pid))
        if info:
            cart_names.add(str(info["product_name"]).strip().lower())

    rows = []
    for rule in PARSED_RULES:
        if rule["ante"].issubset(cart_names):
            for name in rule["cons"]:
                if name.lower() not in cart_names and name.lower() in NAME_TO_ID:
                    rows.append(
                        {
                            "product_id": NAME_TO_ID[name.lower()],
                            "confidence": rule["confidence"],
                            "lift": rule["lift"],
                            "support": rule["support"],
                        }
                    )

    if not rows:
        return pd.DataFrame()

    return (
        pd.DataFrame(rows)
        .sort_values(by=["lift", "confidence"], ascending=False)
        .drop_duplicates(subset=["product_id"])
        .head(top_n)
        .reset_index(drop=True)
    )


# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "page" not in st.session_state:
    st.session_state.page = "home"


def add_to_cart(pid, name):
    pid = int(pid)
    st.session_state.cart[pid] = st.session_state.cart.get(pid, 0) + 1
    st.toast(f"✅ {name} added to cart!")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="hero">'
    '<div class="store-title">🛒 Smart General Store 🛍️</div>'
    '<div class="store-subtitle">Shop your favourite products and get smart '
    "recommendations using Market Basket Analysis (Apriori).</div>"
    '<div class="chip-row">'
    '<span class="chip">🥦 Fresh</span>'
    '<span class="chip">🍎 Healthy</span>'
    '<span class="chip">💰 Affordable</span>'
    '<span class="chip">🚚 Quick Picks</span>'
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.page == "home":

    # Big colourful category icons
    st.markdown(
        '<div class="cat-strip">'
        '<div class="cat-tile cat-1"><span class="cat-icon">🥦</span>Vegetables</div>'
        '<div class="cat-tile cat-2"><span class="cat-icon">🍎</span>Fruits</div>'
        '<div class="cat-tile cat-3"><span class="cat-icon">🥛</span>Dairy</div>'
        '<div class="cat-tile cat-4"><span class="cat-icon">🍞</span>Bakery</div>'
        '<div class="cat-tile cat-5"><span class="cat-icon">🍿</span>Snacks</div>'
        '<div class="cat-tile cat-6"><span class="cat-icon">🧃</span>Drinks</div>'
        '<div class="cat-tile cat-7"><span class="cat-icon">🍗</span>Meat</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    search = st.text_input("🔍 Search Products", placeholder="Search banana, milk, bread...")

    if search:
        filtered = products[
            products["product_name"].str.contains(search, case=False, na=False, regex=False)
        ]
    else:
        filtered = products

    filtered = filtered.head(24)
    total_items = sum(st.session_state.cart.values())

    head_col, cart_col = st.columns([3, 2])
    with head_col:
        st.markdown('<div class="section-title">🛍️ Products</div>', unsafe_allow_html=True)
    with cart_col:
        if st.button(
            f"🛒 Go to Cart ({total_items})",
            key="go_cart",
            use_container_width=True,
        ):
            st.session_state.page = "cart"
            st.rerun()

    if filtered.empty:
        st.warning("No products found.")
    else:
        for start in range(0, len(filtered), 4):
            cols = st.columns(4)
            chunk = filtered.iloc[start:start + 4]

            for col, (_, p) in zip(cols, chunk.iterrows()):
                pid = int(p["product_id"])
                name = str(p["product_name"])
                price = float(p["price"])

                with col:
                    st.markdown(
                        f'<div class="card card-product card-{card_color(pid)}">'
                        f'<div class="card-icon">{product_emoji(name)}</div>'
                        f'<div class="card-name">{name}</div>'
                        f'<div class="card-price">₹{price:.0f}</div>'
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    if st.button("🛒 Add to Cart", key=f"add_{pid}", use_container_width=True):
                        add_to_cart(pid, name)
                        st.rerun()

# =========================================================
# CART PAGE
# =========================================================

elif st.session_state.page == "cart":

    header_col, home_col = st.columns([3, 2])
    with header_col:
        st.markdown('<div class="section-title">🛒 Your Shopping Cart</div>', unsafe_allow_html=True)
    with home_col:
        if st.button("🏠 Continue Shopping", key="continue_shop", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.divider()

    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("🛍️ Start Shopping", key="start_shopping"):
            st.session_state.page = "home"
            st.rerun()

    else:
        grand_total = 0.0

        h1, h2, h3, h4 = st.columns([4, 3, 1.5, 1.5])
        h1.markdown('<div class="cart-head">Product</div>', unsafe_allow_html=True)
        h2.markdown('<div class="cart-head">Quantity</div>', unsafe_allow_html=True)
        h3.markdown('<div class="cart-head">Price</div>', unsafe_allow_html=True)
        h4.markdown('<div class="cart-head">Subtotal</div>', unsafe_allow_html=True)
        st.divider()

        for pid, qty in list(st.session_state.cart.items()):
            info = ID_TO_ROW.get(int(pid))
            if not info:
                continue

            name = str(info["product_name"])
            price = float(info["price"])
            subtotal = price * qty
            grand_total += subtotal

            c_name, c_qty, c_price, c_sub = st.columns([4, 3, 1.5, 1.5])

            with c_name:
                st.markdown(
                    f'<div class="cart-name">{product_emoji(name)} {name}</div>',
                    unsafe_allow_html=True,
                )
                if st.button("🗑️ Remove", key=f"remove_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()

            with c_qty:
                m, n, pl = st.columns([1, 1, 1])
                with m:
                    if st.button("➖", key=f"minus_{pid}", use_container_width=True):
                        st.session_state.cart[pid] -= 1
                        if st.session_state.cart[pid] <= 0:
                            del st.session_state.cart[pid]
                        st.rerun()
                with n:
                    st.markdown(f'<div class="cart-num">{qty}</div>', unsafe_allow_html=True)
                with pl:
                    if st.button("➕", key=f"plus_{pid}", use_container_width=True):
                        st.session_state.cart[pid] += 1
                        st.rerun()

            with c_price:
                st.markdown(f'<div class="cart-num" style="text-align:left">₹{price:.0f}</div>', unsafe_allow_html=True)
            with c_sub:
                st.markdown(f'<div class="cart-num" style="text-align:left">₹{subtotal:.0f}</div>', unsafe_allow_html=True)

            st.divider()

        # ---------------- BILL SUMMARY ----------------
        st.markdown('<div class="section-title">💰 Bill Summary</div>', unsafe_allow_html=True)

        total_items = sum(st.session_state.cart.values())
        b1, b2 = st.columns(2)
        with b1:
            st.metric("🛒 Total Items", total_items)
        with b2:
            st.metric("💳 Total Bill", f"₹{grand_total:.0f}")

        st.success(f"🧾 Total payable amount: ₹{grand_total:.0f}")

        # ---------------- RECOMMENDATIONS (after billing) ----------------
        st.divider()
        st.markdown('<div class="section-title">✨ Recommended for Your Cart</div>', unsafe_allow_html=True)
        st.write(
            "Generated from Apriori association rules based on the products "
            "currently in your cart."
        )

        recs = get_recommendations(st.session_state.cart, top_n=6)

        if recs.empty:
            st.info("No recommendations are available for the current products.")
        else:
            for start in range(0, len(recs), 3):
                cols = st.columns(3)
                chunk = recs.iloc[start:start + 3]

                for col, (_, r) in zip(cols, chunk.iterrows()):
                    rid = int(r["product_id"])
                    info = ID_TO_ROW[rid]
                    rname = str(info["product_name"])
                    rprice = float(info["price"])

                    with col:
                        st.markdown(
                            f'<div class="card card-reco card-{card_color(rid)}">'
                            f'<div class="card-icon">{product_emoji(rname)}</div>'
                            f'<div class="card-name">✨ {rname}</div>'
                            f'<div class="card-price">₹{rprice:.0f}</div>'
                            f'<div class="card-meta">Confidence: {r["confidence"] * 100:.1f}%'
                            f' &nbsp;|&nbsp; Lift: {r["lift"]:.2f}</div>'
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                        if st.button("➕ Add to Cart", key=f"recommend_{rid}", use_container_width=True):
                            add_to_cart(rid, rname)
                            st.rerun()

        # ---------------- CLEAR CART ----------------
        st.divider()
        if st.button("🗑️ Clear Entire Cart", key="clear_cart", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()