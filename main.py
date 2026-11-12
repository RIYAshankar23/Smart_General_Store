
# ============================================================
# MARKET BASKET INTELLIGENCE
# Instacart Dataset | Data Preprocessing + Apriori Algorithm
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import json
from pathlib import Path

from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


# ============================================================
# 1. PROJECT PATHS AND CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_SIZE = 100000
TOP_N_PRODUCTS = 100

MIN_SUPPORT = 0.003
MIN_CONFIDENCE = 0.10
MIN_LIFT = 1.0
MAX_ITEMSET_SIZE = 3

RANDOM_STATE = 42


# ============================================================
# 2. LOAD DATASETS
# ============================================================

print("\n========== LOADING DATASETS ==========\n")

orders = pd.read_csv(
    RAW_DIR / "orders.csv",
    usecols=[
        "order_id",
        "user_id",
        "eval_set",
        "order_number",
        "days_since_prior_order"
    ]
)

products = pd.read_csv(
    RAW_DIR / "products.csv"
)

prior_path = RAW_DIR / "order_products__prior.csv"

aisles = pd.read_csv(
    RAW_DIR / "aisles.csv"
)

departments = pd.read_csv(
    RAW_DIR / "departments.csv"
)

# Train data is retained for possible future evaluation.
# It is not used to train our Apriori model.

train_path = RAW_DIR / "order_products__train.csv"

print("All datasets loaded successfully!")


# ============================================================
# 3. INITIAL DATA EXPLORATION
# ============================================================

print("\n========== DATASET DIMENSIONS ==========\n")

datasets = {
    "Orders": orders,
    "Products": products,
    "Aisles": aisles,
    "Departments": departments
}

for name, df in datasets.items():

    print(f"\n{name}")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

    print("\nFirst five records:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)


# ============================================================
# 4. MISSING VALUE ANALYSIS
# ============================================================

print("\n========== MISSING VALUE ANALYSIS ==========\n")

for name, df in datasets.items():

    print(f"\n{name}")

    print(
        df.isnull().sum()
    )


# days_since_prior_order contains NaN values
# for customers' first orders.
# We retain these values because they are meaningful.

# Remove records without essential identifiers.

orders = orders.dropna(
    subset=["order_id", "eval_set"]
)

products = products.dropna(
    subset=["product_id", "product_name"]
)


# ============================================================
# 5. DUPLICATE ANALYSIS
# ============================================================

print("\n========== DUPLICATE ANALYSIS ==========\n")

for name, df in datasets.items():

    print(
        name,
        "Duplicate rows:",
        df.duplicated().sum()
    )

print(
    "\nDuplicate order IDs:",
    orders["order_id"].duplicated().sum()
)

print(
    "Duplicate product IDs:",
    products["product_id"].duplicated().sum()
)

# IDs in master tables should be unique.

assert orders["order_id"].is_unique, \
    "Duplicate order IDs found!"

assert products["product_id"].is_unique, \
    "Duplicate product IDs found!"


# ============================================================
# 6. DATA CONSISTENCY CHECKS
# ============================================================

print("\n========== DATA CONSISTENCY ==========\n")

print(
    orders["eval_set"].value_counts()
)

print(
    "\nNumber of unique products:",
    products["product_id"].nunique()
)

print(
    "Number of unique orders:",
    orders["order_id"].nunique()
)


# ============================================================
# 7. MERGE PRODUCT INFORMATION
# ============================================================

print("\n========== MERGING PRODUCT INFORMATION ==========\n")

product_details = products.merge(
    aisles,
    on="aisle_id",
    how="left",
    validate="many_to_one"
)

product_details = product_details.merge(
    departments,
    on="department_id",
    how="left",
    validate="many_to_one"
)

print(product_details.head())

print(
    "\nMissing product details:",
    product_details[
        ["aisle", "department"]
    ].isnull().sum()
)


# ============================================================
# 8. SELECT PRIOR ORDERS
# ============================================================

print("\n========== SELECTING PRIOR ORDERS ==========\n")

prior_order_ids = orders.loc[
    orders["eval_set"] == "prior",
    "order_id"
].to_numpy()

print(
    "Total prior orders:",
    len(prior_order_ids)
)

# Reproducible random sampling.

rng = np.random.default_rng(RANDOM_STATE)

sampled_order_ids = rng.choice(
    prior_order_ids,
    size=min(SAMPLE_SIZE, len(prior_order_ids)),
    replace=False
)

sampled_order_ids = np.sort(sampled_order_ids)

sampled_order_set = set(sampled_order_ids)

print(
    "Sampled orders:",
    len(sampled_order_ids)
)


# ============================================================
# 9. LOAD PRIOR TRANSACTIONS IN CHUNKS
# ============================================================

print("\n========== READING PRIOR TRANSACTIONS ==========\n")

chunks = []

for chunk in pd.read_csv(
    prior_path,
    usecols=["order_id", "product_id"],
    dtype={
        "order_id": "int32",
        "product_id": "int32"
    },
    chunksize=1000000
):

    selected = chunk[
        chunk["order_id"].isin(sampled_order_set)
    ]

    if not selected.empty:
        chunks.append(selected)

if not chunks:
    raise ValueError("No matching prior transactions found.")

prior_sample = pd.concat(
    chunks,
    ignore_index=True
)

print(
    "Sampled transaction-product rows:",
    prior_sample.shape
)

# Remove records with missing identifiers.

prior_sample = prior_sample.dropna(
    subset=["order_id", "product_id"]
)

# Check duplicate transaction-product combinations.

print(
    "Duplicate order-product pairs:",
    prior_sample.duplicated(
        subset=["order_id", "product_id"]
    ).sum()
)

prior_sample = prior_sample.drop_duplicates(
    subset=["order_id", "product_id"]
)

# Validate product IDs.

valid_product_ids = set(
    products["product_id"]
)

invalid_products = (
    set(prior_sample["product_id"])
    - valid_product_ids
)

print(
    "Invalid product IDs:",
    len(invalid_products)
)

prior_sample = prior_sample[
    prior_sample["product_id"].isin(
        valid_product_ids
    )
].copy()

print(
    "Cleaned transaction-product rows:",
    prior_sample.shape
)


# ============================================================
# 10. PRODUCT FREQUENCY ANALYSIS
# ============================================================

print("\n========== PRODUCT FREQUENCY ANALYSIS ==========\n")

product_frequency = (
    prior_sample["product_id"]
    .value_counts()
    .reset_index()
)

product_frequency.columns = [
    "product_id",
    "purchase_count"
]

# Add readable product names.

product_frequency = product_frequency.merge(
    product_details[
        ["product_id", "product_name", "aisle", "department"]
    ],
    on="product_id",
    how="left"
)

print(
    "\nTop 15 purchased products:"
)

print(
    product_frequency.head(15)
)

# Visualize the top 15 products.

top_15 = product_frequency.head(15)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_15,
    x="purchase_count",
    y="product_name"
)

plt.title("Top 15 Frequently Purchased Products")
plt.xlabel("Purchase Count")
plt.ylabel("Product Name")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_products_visualization.png"
)

plt.close()


# ============================================================
# 11. SELECT TOP N PRODUCTS
# ============================================================

print("\n========== SELECTING FREQUENT PRODUCTS ==========\n")

top_product_ids = (
    product_frequency
    .head(TOP_N_PRODUCTS)["product_id"]
    .to_numpy()
)

print(
    "Selected products:",
    len(top_product_ids)
)


# ============================================================
# 12. FILTER TRANSACTIONS
# ============================================================

print("\n========== FILTERING TRANSACTIONS ==========\n")

filtered_transactions = prior_sample[
    prior_sample["product_id"].isin(
        top_product_ids
    )
].copy()

print(
    "Rows before filtering:",
    len(prior_sample)
)

print(
    "Rows after filtering:",
    len(filtered_transactions)
)


# ============================================================
# 13. CREATE TRANSACTION GROUPS
# ============================================================

print("\n========== CREATING TRANSACTION GROUPS ==========\n")

transactions = (
    filtered_transactions
    .groupby("order_id")["product_id"]
    .agg(list)
    .reset_index()
)

transactions.columns = [
    "order_id",
    "products"
]

# Exclude baskets with fewer than two selected products.
# These cannot produce multi-product associations.

transactions = transactions[
    transactions["products"].apply(len) >= 2
].reset_index(drop=True)

print(
    "Usable transactions:",
    len(transactions)
)

print(
    transactions.head()
)


# ============================================================
# 14. ONE-HOT ENCODING
# ============================================================

print("\n========== ONE-HOT ENCODING ==========\n")

# Every sampled order gets a row.
# Orders with no selected top-N products remain all-zero rows.
# This preserves the correct support denominator.

order_index = pd.Index(sampled_order_ids)

product_index = pd.Index(top_product_ids)

row_indices = order_index.get_indexer(
    filtered_transactions["order_id"]
)

column_indices = product_index.get_indexer(
    filtered_transactions["product_id"]
)

if (row_indices < 0).any() or (column_indices < 0).any():
    raise ValueError("Invalid order or product index encountered.")

# Dense boolean matrix: manageable at 100,000 x 100.

basket_array = np.zeros(
    (
        len(sampled_order_ids),
        len(top_product_ids)
    ),
    dtype=bool
)

basket_array[
    row_indices,
    column_indices
] = True

product_columns = [
    f"P_{pid}" for pid in top_product_ids
]

basket_matrix = pd.DataFrame(
    basket_array,
    index=sampled_order_ids,
    columns=product_columns
)

print(
    "Basket matrix shape:",
    basket_matrix.shape
)

print(
    basket_matrix.head()
)

print(
    "\nTotal purchased product entries:",
    int(basket_array.sum())
)


# ============================================================
# 15. APPLY APRIORI ALGORITHM
# ============================================================

print("\n========== APPLYING APRIORI ==========\n")

frequent_itemsets = apriori(
    basket_matrix,
    min_support=MIN_SUPPORT,
    use_colnames=True,
    max_len=MAX_ITEMSET_SIZE,
    low_memory=True
)

frequent_itemsets["itemset_length"] = (
    frequent_itemsets["itemsets"].apply(len)
)

frequent_itemsets = frequent_itemsets.sort_values(
    by="support",
    ascending=False
).reset_index(drop=True)

print(
    "Frequent itemsets found:",
    len(frequent_itemsets)
)

print(
    frequent_itemsets.head(20)
)


# ============================================================
# 16. GENERATE ASSOCIATION RULES
# ============================================================

print("\n========== GENERATING ASSOCIATION RULES ==========\n")

if (
    not frequent_itemsets.empty
    and frequent_itemsets["itemset_length"].max() >= 2
):

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=MIN_CONFIDENCE
    )

    # Keep useful product associations.

    filtered_rules = rules[
        (rules["confidence"] >= MIN_CONFIDENCE) &
        (rules["lift"] > MIN_LIFT) &
        (rules["support"] >= MIN_SUPPORT)
    ].copy()

    filtered_rules = filtered_rules.sort_values(
        by=["lift", "confidence"],
        ascending=False
    ).reset_index(drop=True)

else:

    print(
        "Not enough frequent itemsets to generate rules."
    )

    filtered_rules = pd.DataFrame(
        columns=[
            "antecedents",
            "consequents",
            "support",
            "confidence",
            "lift",
            "leverage",
            "conviction"
        ]
    )

print(
    "Association rules generated:",
    len(filtered_rules)
)

print(
    filtered_rules.head(20)
)


# ============================================================
# 17. CONVERT PRODUCT IDS INTO PRODUCT NAMES
# ============================================================

print("\n========== PRODUCT NAME MAPPING ==========\n")

id_to_name = product_details.set_index(
    "product_id"
)["product_name"].to_dict()


def convert_to_names(itemset):

    names = []

    for item in itemset:

        product_id = int(
            item.replace("P_", "")
        )

        names.append(
            id_to_name.get(
                product_id,
                "Unknown Product"
            )
        )

    return ", ".join(sorted(names))


# Convert frequent itemsets.

frequent_itemsets["product_names"] = (
    frequent_itemsets["itemsets"]
    .apply(convert_to_names)
)

# Convert association rules.

if not filtered_rules.empty:

    filtered_rules["antecedents_names"] = (
        filtered_rules["antecedents"]
        .apply(convert_to_names)
    )

    filtered_rules["consequents_names"] = (
        filtered_rules["consequents"]
        .apply(convert_to_names)
    )

print(
    frequent_itemsets.head()
)


# ============================================================
# 18. PRODUCT RECOMMENDATION FUNCTION
# ============================================================

def recommend_products(product_name, top_n=5):

    matched_products = products[
        products["product_name"].str.lower()
        == product_name.lower()
    ]

    if matched_products.empty:

        return "Product not found."

    product_id = int(
        matched_products.iloc[0]["product_id"]
    )

    product_code = f"P_{product_id}"

    if filtered_rules.empty:

        return "No association rules available."

    # Find rules where the selected product is
    # the only antecedent.

    recommendations = filtered_rules[
        filtered_rules["antecedents"].apply(
            lambda x: x == frozenset([product_code])
        )
    ].copy()

    recommendations = recommendations.sort_values(
        by=["lift", "confidence"],
        ascending=False
    )

    if recommendations.empty:

        return "No recommendations found for this product."

    return recommendations[
        [
            "consequents_names",
            "support",
            "confidence",
            "lift"
        ]
    ].head(top_n)


# Example:
# print(recommend_products("Banana", top_n=5))


# ============================================================
# 19. EXPORT PROCESSED DATASETS
# ============================================================

print("\n========== EXPORTING RESULTS ==========\n")

# Export frequent itemsets.

frequent_export = frequent_itemsets.copy()

frequent_export["itemsets"] = (
    frequent_export["itemsets"]
    .apply(lambda x: ", ".join(sorted(x)))
)

frequent_export.to_csv(
    OUTPUT_DIR / "frequent_itemsets.csv",
    index=False
)


# Export association rules.

rules_export_columns = [
    "antecedents_names",
    "consequents_names",
    "support",
    "confidence",
    "lift",
    "leverage",
    "conviction"
]

if filtered_rules.empty:

    rules_export = pd.DataFrame(
        columns=rules_export_columns
    )

else:

    rules_export = filtered_rules[
        rules_export_columns
    ].copy()

rules_export.to_csv(
    OUTPUT_DIR / "association_rules.csv",
    index=False
)


# Export product lookup.

product_details.to_csv(
    OUTPUT_DIR / "product_lookup.csv",
    index=False
)


# Export top products.

product_frequency.head(100).to_csv(
    OUTPUT_DIR / "top_products.csv",
    index=False
)


# Export transaction groups.

transaction_export = transactions.copy()

transaction_export["products"] = (
    transaction_export["products"]
    .apply(
        lambda x: ", ".join(
            id_to_name.get(pid, "Unknown Product")
            for pid in x
        )
    )
)

transaction_export.to_csv(
    OUTPUT_DIR / "sampled_transactions.csv",
    index=False
)


# ============================================================
# 20. SAVE PROJECT SUMMARY
# ============================================================

summary = {
    "total_prior_orders": int(len(prior_order_ids)),
    "sampled_orders": int(len(sampled_order_ids)),
    "sampled_product_rows": int(len(prior_sample)),
    "selected_products": int(len(top_product_ids)),
    "usable_transactions": int(len(transactions)),
    "frequent_itemsets": int(len(frequent_itemsets)),
    "association_rules": int(len(filtered_rules)),
    "minimum_support": MIN_SUPPORT,
    "minimum_confidence": MIN_CONFIDENCE,
    "minimum_lift": MIN_LIFT,
    "maximum_itemset_size": MAX_ITEMSET_SIZE,
    "random_state": RANDOM_STATE
}

with open(
    OUTPUT_DIR / "project_summary.json",
    "w"
) as file:

    json.dump(
        summary,
        file,
        indent=4
    )


# ============================================================
# 21. FINAL RESULTS
# ============================================================

print("\n========================================")
print("       PIPELINE EXECUTION COMPLETE")
print("========================================")

for key, value in summary.items():

    print(f"{key}: {value}")

print("\nGenerated files:")

for file in OUTPUT_DIR.iterdir():

    print(file.name)

print("\nAll results saved successfully!")

print("\nExample recommendation:")

print(
    recommend_products("Banana", top_n=5)
)

print("\n========================================")
print("       READY FOR STREAMLIT")
print("========================================")
