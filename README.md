# 🛒 Smart General Store – Market Basket Analysis

A **Market Basket Analysis and Product Recommendation System** built using Python, the **Apriori Algorithm**, Association Rule Mining, and Streamlit.

The project analyzes historical Instacart shopping transactions to discover products that are frequently purchased together. These patterns are then used in an interactive grocery shopping application to recommend relevant products based on the customer's cart.

---

## 📌 Project Overview

Online shopping platforms often recommend products using messages such as:

> **“Customers who bought this item also bought…”**

This project demonstrates how such recommendations can be generated using **Market Basket Analysis**.

The system analyzes previous customer orders and identifies relationships between products using the **Apriori Algorithm**.

For example:

**Organic Cilantro → Limes**

This means customers purchasing **Organic Cilantro** are also likely to purchase **Limes**.

---

## 🎯 Objectives

The main objectives of this project are to:

- Analyze customer shopping transactions
- Identify frequently purchased product combinations
- Generate association rules using Apriori
- Evaluate rules using **Support, Confidence, and Lift**
- Build an interactive analytics dashboard
- Develop a grocery shopping interface
- Recommend products according to items already present in the customer's cart

---

## 📊 Dataset

The project uses the **Instacart Market Basket Analysis dataset**, containing millions of grocery orders and product transactions.

For efficient processing, the analysis focuses on:

- **100,000 sampled orders**
- **Top 100 frequently purchased products**
- **51,502 usable shopping baskets**

---

## 🧠 Apriori Algorithm

The **Apriori Algorithm** identifies groups of products that frequently occur together in customer transactions.

The project considers itemsets containing up to **3 products**.

Example:

```text
Banana
Banana + Organic Baby Spinach
Banana + Organic Baby Spinach + Organic Avocado
```

The resulting frequent itemsets are then used to generate association rules.

---

## 📈 Association Rule Metrics

### Support

Support measures how frequently a product combination occurs across all transactions.

### Confidence

Confidence measures how often product **B** is purchased when product **A** has already been purchased.

### Lift

Lift measures the strength of the relationship between two products.

```text
Lift > 1  → Positive association
Lift = 1  → No significant association
Lift < 1  → Negative association
```

Example rule discovered by the project:

```text
Organic Cilantro → Limes

Support    ≈ 0.00537
Confidence ≈ 24.58%
Lift       ≈ 5.60
```

---

## 📊 Project Results

The analysis generated:

| Metric | Result |
|---|---:|
| Orders Sampled | 100,000 |
| Products Considered | 100 |
| Shopping Baskets Used | 51,502 |
| Frequent Itemsets | 371 |
| Association Rules | 295 |

Only relationships satisfying the selected Support, Confidence, and Lift criteria are retained.

---

## 🏗️ Project Architecture

```text
Instacart Dataset
       │
       ▼
Data Preprocessing
       │
       ▼
Top Product Selection
       │
       ▼
Shopping Basket Creation
       │
       ▼
Apriori Algorithm
       │
       ▼
Frequent Itemsets
       │
       ▼
Association Rules
       │
       ├──────────────► Analytics Dashboard
       │
       ▼
Smart Grocery Store
       │
       ▼
Customer Cart
       │
       ▼
Product Recommendations
```

---

## 🖥️ Analytics Dashboard

The project contains a Streamlit analytics dashboard that displays:

- Project statistics
- Top purchased products
- Frequent itemsets
- Association rules
- Support values
- Confidence values
- Lift values
- Product recommendations

Run the dashboard using:

```bash
streamlit run dashboard.py
```

---

## 🛍️ Smart Grocery Store

The project also contains an interactive shopping interface built using **Streamlit**.

### Features

- 🔍 Search products
- 🛒 Add products to cart
- ➕ Increase quantity
- ➖ Decrease quantity
- 🗑️ Remove products
- 💰 Automatic bill calculation
- ✨ Apriori-based product recommendations
- ➕ Add recommended products directly to the cart

Run the store using:

```bash
streamlit run shop.py
```

---

## ✨ How Recommendations Work

Suppose the customer adds:

```text
Organic Cilantro
```

to their shopping cart.

The system checks the generated association rules and may find:

```text
Organic Cilantro → Limes
Organic Cilantro → Organic Hass Avocado
Organic Cilantro → Organic Avocado
Organic Cilantro → Organic Baby Spinach
```

The strongest matching products are then displayed under:

### ✨ Recommended for Your Cart

Recommendations are ranked using metrics such as **Lift and Confidence**.

Not every product necessarily produces a recommendation because Apriori only retains product relationships that satisfy the association-rule thresholds.

---

## 📁 Project Structure

```text
Smart_General_Store/
│
├── main.py
│   └── Data preprocessing and Apriori analysis
│
├── dashboard.py
│   └── Market Basket Analysis dashboard
│
├── shop.py
│   └── Interactive grocery store and recommendation system
│
├── requirements.txt
│
├── data/
│   └── processed/
│       ├── association_rules.csv
│       ├── frequent_itemsets.csv
│       ├── product_lookup.csv
│       ├── project_summary.json
│       ├── top_products.csv
│       └── top_products_visualization.png
│
└── README.md
```

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- MLxtend
- Apriori Algorithm
- Association Rule Mining
- Streamlit
- Matplotlib
- Altair

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/RIYAshankar23/Smart_General_Store.git
```

Enter the project directory:

```bash
cd Smart_General_Store
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on Linux/WSL:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the shopping application:

```bash
streamlit run shop.py
```

---

## 🔮 Future Improvements

The project can be extended by:

- Analyzing more products
- Processing a larger portion of the Instacart dataset
- Adding product categories and images
- Adding fallback recommendations when no Apriori rule exists
- Creating personalized recommendations using customer history
- Combining Apriori with machine-learning recommendation techniques
- Deploying the application online

---

## 👩‍💻 Development

This project builds on an existing Market Basket Analysis codebase and extends it into an interactive application.

My work on the project includes developing and integrating the **Streamlit analytics dashboard**, **smart grocery shopping interface**, **product search**, **shopping cart**, **quantity management**, **billing system**, and **Apriori association-rule-based recommendation workflow**.

---

## 📚 Key Learning

This project demonstrates how historical transaction data can be transformed into useful business recommendations.

The complete workflow is:

**Customer Transactions → Market Basket Analysis → Apriori → Association Rules → Product Recommendations**

---

## 👩‍🎓 Author

**Riya Shankar**

Data Science / Computer Science Project
