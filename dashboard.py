import streamlit as st
import pandas as pd
import altair as alt
import json

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(page_title="Market Basket Analysis", page_icon="🛒", layout="wide")

# --------------------------------------------------
# CUSTOM CSS  (big fonts, high contrast, colorful)
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

html, body, .stApp, [class*="css"] { font-family: 'Poppins', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #e0f2fe 0%, #fdf4ff 45%, #fff7ed 100%);
}
.block-container { padding-top: 2rem; max-width: 1400px; }

/* ---------- HERO ---------- */
.hero {
    background: linear-gradient(120deg, #1e1b4b 0%, #4338ca 40%, #db2777 100%);
    border-radius: 28px;
    padding: 50px 30px 40px 30px;
    text-align: center;
    box-shadow: 0 18px 45px rgba(79, 70, 229, 0.35);
    margin-bottom: 35px;
}
.main-title {
    font-size: 84px;
    line-height: 1.1;
    font-weight: 900;
    background: linear-gradient(90deg, #fde047, #fb923c, #f472b6, #67e8f9);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 14px;
}
.subtitle {
    font-size: 32px;
    font-weight: 600;
    color: #ffffff;
}

/* ---------- SECTION TITLES ---------- */
.section-title {
    font-size: 46px;
    font-weight: 800;
    color: #ffffff;
    background: linear-gradient(90deg, #4f46e5, #9333ea, #db2777);
    padding: 14px 28px;
    border-radius: 18px;
    margin: 35px 0 20px 0;
    display: inline-block;
    box-shadow: 0 8px 20px rgba(147, 51, 234, 0.30);
}

/* ---------- TEXT ---------- */
.desc {
    font-size: 26px;
    line-height: 1.6;
    font-weight: 500;
    color: #1e293b;
    margin-bottom: 20px;
}
.stMarkdown p, .stMarkdown li { font-size: 24px; color: #1e293b; }

/* ---------- MESSAGE BOXES ---------- */
.ok-box {
    background: #dcfce7;
    border-left: 8px solid #16a34a;
    color: #14532d;
    font-size: 26px;
    font-weight: 700;
    padding: 18px 26px;
    border-radius: 16px;
    margin-bottom: 20px;
}
.warn-box {
    background: #fef3c7;
    border-left: 8px solid #d97706;
    color: #78350f;
    font-size: 26px;
    font-weight: 700;
    padding: 18px 26px;
    border-radius: 16px;
}

/* ---------- METRIC CARDS ---------- */
.metric-card {
    border-radius: 24px;
    padding: 30px 20px;
    text-align: center;
    color: #ffffff;
    box-shadow: 0 12px 28px rgba(0,0,0,0.18);
}
.metric-label { font-size: 26px; font-weight: 700; margin-bottom: 8px; }
.metric-value { font-size: 64px; font-weight: 900; line-height: 1.1; }
.m1 { background: linear-gradient(135deg, #2563eb, #06b6d4); }
.m2 { background: linear-gradient(135deg, #7c3aed, #ec4899); }
.m3 { background: linear-gradient(135deg, #ea580c, #facc15); }
.m4 { background: linear-gradient(135deg, #059669, #84cc16); }

/* ---------- SELECTBOX (force light + large) ---------- */
.stSelectbox label, .stSelectbox label p {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #312e81 !important;
}
.stSelectbox [data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 3px solid #7c3aed !important;
    border-radius: 16px !important;
    min-height: 70px;
}
.stSelectbox [data-baseweb="select"] div,
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] input {
    font-size: 26px !important;
    font-weight: 600 !important;
    color: #0f172a !important;
}
.stSelectbox svg { fill: #7c3aed !important; width: 28px; height: 28px; }
[data-baseweb="popover"] li, [role="option"] {
    font-size: 24px !important;
    color: #0f172a !important;
    background: #ffffff !important;
}
[role="option"]:hover { background: #ede9fe !important; }

/* ---------- RECOMMEND BANNER ---------- */
.rec-banner {
    background: linear-gradient(90deg, #fde68a, #fbcfe8, #c7d2fe);
    border-left: 10px solid #4f46e5;
    border-radius: 20px;
    padding: 26px 30px;
    margin: 25px 0;
    font-size: 32px;
    font-weight: 800;
    color: #1e1b4b;
}

/* ---------- HTML TABLES ---------- */
.table-wrap {
    overflow-x: auto;
    border-radius: 20px;
    border: 3px solid #c7d2fe;
    box-shadow: 0 10px 25px rgba(79,70,229,0.15);
    background: #ffffff;
    max-height: 650px;
    overflow-y: auto;
}
table.fancy { width: 100%; border-collapse: collapse; font-size: 24px; }
table.fancy thead th {
    position: sticky; top: 0;
    background: linear-gradient(90deg, #4f46e5, #9333ea);
    color: #ffffff;
    font-size: 24px;
    font-weight: 800;
    padding: 18px 16px;
    text-align: left;
    white-space: nowrap;
}
table.fancy tbody td {
    padding: 16px;
    color: #0f172a;
    font-weight: 500;
    border-bottom: 1px solid #e2e8f0;
}
table.fancy tbody tr:nth-child(even) { background: #f5f3ff; }
table.fancy tbody tr:nth-child(odd)  { background: #ffffff; }
table.fancy tbody tr:hover { background: #fef3c7; }
table.fancy td:first-child { font-weight: 700; color: #3730a3; }

/* ---------- HOW IT WORKS ---------- */
.step-card {
    border-radius: 24px;
    padding: 30px;
    min-height: 260px;
    color: #ffffff;
    box-shadow: 0 12px 28px rgba(0,0,0,0.18);
}
.step-card h3 { font-size: 36px; font-weight: 800; margin-bottom: 14px; color: #ffffff; }
.step-card p  { font-size: 25px; line-height: 1.55; color: #ffffff !important; }
.s1 { background: linear-gradient(135deg, #2563eb, #7c3aed); }
.s2 { background: linear-gradient(135deg, #db2777, #f97316); }
.s3 { background: linear-gradient(135deg, #059669, #0ea5e9); }

/* ---------- FOOTER ---------- */
.footer {
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
    background: linear-gradient(90deg, #1e1b4b, #4338ca, #db2777);
    padding: 28px;
    border-radius: 22px;
    margin-top: 40px;
}

hr { border: none; height: 4px; background: linear-gradient(90deg,#6366f1,#ec4899,#f59e0b); border-radius: 4px; margin: 35px 0; }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def desc(text):
    st.markdown(f'<div class="desc">{text}</div>', unsafe_allow_html=True)


def html_table(df):
    """Render a dataframe as a big, always-readable HTML table."""
    html = df.to_html(index=False, classes="fancy", border=0, escape=True)
    st.markdown(f'<div class="table-wrap">{html}</div>', unsafe_allow_html=True)


def metric_card(col, cls, label, value):
    col.markdown(
        f'<div class="metric-card {cls}"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
rules = pd.read_csv("data/processed/association_rules.csv")
itemsets = pd.read_csv("data/processed/frequent_itemsets.csv")
products = pd.read_csv("data/processed/product_lookup.csv")
top_products = pd.read_csv("data/processed/top_products.csv")

with open("data/processed/project_summary.json") as f:
    summary = json.load(f)


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="main-title">🛒 Market Basket Analysis</div>
        <div class="subtitle">Product Recommendation System using the Apriori Algorithm</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="ok-box">✅ Dataset and Apriori results loaded successfully!</div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------
section("📊 Project Overview")

c1, c2, c3, c4 = st.columns(4)
metric_card(c1, "m1", "🧾 Orders Analyzed", "100,000")
metric_card(c2, "m2", "📦 Top Products", "100")
metric_card(c3, "m3", "🔍 Frequent Itemsets", f"{len(itemsets):,}")
metric_card(c4, "m4", "🔗 Association Rules", f"{len(rules):,}")

st.divider()


# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------
section("🏆 Top Purchased Products")
desc("These are the most frequently purchased products found in the analyzed shopping baskets.")

top_10 = top_products.head(10)

chart = (
    alt.Chart(top_10)
    .mark_bar(cornerRadiusTopRight=10, cornerRadiusBottomRight=10)
    .encode(
        y=alt.Y(
            "product_name:N",
            sort="-x",
            title=None,
            axis=alt.Axis(labelFontSize=20, labelColor="#0f172a", labelLimit=400),
        ),
        x=alt.X(
            "purchase_count:Q",
            title="Purchase Count",
            axis=alt.Axis(labelFontSize=18, titleFontSize=22, titleColor="#312e81", labelColor="#0f172a"),
        ),
        color=alt.Color("purchase_count:Q", scale=alt.Scale(scheme="plasma"), legend=None),
        tooltip=["product_name", "purchase_count"],
    )
    .properties(height=520)
    .configure(background="#ffffff")
    .configure_view(strokeWidth=0)
)
st.altair_chart(chart, use_container_width=True)

st.divider()


# --------------------------------------------------
# ASSOCIATION RULES
# --------------------------------------------------
section("🔗 Association Rules")
desc(
    "Association rules identify products that are frequently purchased together. "
    "The strength of each relationship is measured using <b>Support, Confidence and Lift</b>."
)

rules_view = rules.copy()
rules_view.columns = [c.replace("_", " ").title() for c in rules_view.columns]
num_cols = rules_view.select_dtypes("number").columns
rules_view[num_cols] = rules_view[num_cols].round(4)
html_table(rules_view)

st.divider()


# --------------------------------------------------
# PRODUCT RECOMMENDATION
# --------------------------------------------------
section("✨ Smart Product Recommender")
desc("Select a product below to discover products that customers commonly purchase with it.")

product_options = sorted(rules["antecedents_names"].dropna().unique())
selected_product = st.selectbox("🛍️ Select a Product", product_options)

recommendations = rules[rules["antecedents_names"] == selected_product].sort_values(
    by=["lift", "confidence"], ascending=False
)

if not recommendations.empty:
    st.markdown(
        f'<div class="rec-banner">🛒 Customers buying <u>{selected_product}</u> may also buy:</div>',
        unsafe_allow_html=True,
    )

    rec = recommendations[["consequents_names", "support", "confidence", "lift"]].head(5).copy()
    rec.columns = ["Recommended Product", "Support (%)", "Confidence (%)", "Lift"]
    rec["Support (%)"] = (rec["Support (%)"] * 100).round(2).map("{:.2f}%".format)
    rec["Confidence (%)"] = (rec["Confidence (%)"] * 100).round(2).map("{:.2f}%".format)
    rec["Lift"] = rec["Lift"].round(2).map("{:.2f}".format)
    html_table(rec)
else:
    st.markdown(
        '<div class="warn-box">⚠️ No recommendations were found for this product.</div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------
st.divider()
section("💡 How Does This System Work?")

a, b, c = st.columns(3)
a.markdown(
    '<div class="step-card s1"><h3>🛒 1. Shopping Baskets</h3>'
    '<p>Customer orders are analyzed to understand which products are purchased together.</p></div>',
    unsafe_allow_html=True,
)
b.markdown(
    '<div class="step-card s2"><h3>🔍 2. Apriori Algorithm</h3>'
    '<p>Apriori discovers combinations of products that frequently occur in the same orders.</p></div>',
    unsafe_allow_html=True,
)
c.markdown(
    '<div class="step-card s3"><h3>🎯 3. Recommendations</h3>'
    '<p>Strong association rules are used to recommend related products to customers.</p></div>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    '<div class="footer">🛒 Market Basket Analysis • Apriori Algorithm • Product Recommendation System</div>',
    unsafe_allow_html=True,
)
