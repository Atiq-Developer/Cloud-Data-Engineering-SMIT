import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Banggood Product Analysis Dashboard")

# Load Data
df = pd.read_csv("cleaned_banggood_products.csv")

# Clean numeric fields
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["review_count"] = df["reviews"].astype(str).str.extract(r"(\d+)").astype(float)

# Derived features
df["value_score"] = df["rating"] / df["price"]
df["price_per_review"] = df["price"] / (df["review_count"] + 1)

# Sidebar filters
st.sidebar.header("Filters")
min_price, max_price = st.sidebar.slider(
    "Select Price Range",
    float(df["price"].min()),
    float(df["price"].max()),
    (float(df["price"].min()), float(df["price"].max()))
)

filtered_df = df[(df["price"] >= min_price) & (df["price"] <= max_price)]

st.subheader("Filtered Dataset")
st.dataframe(filtered_df)

# -------------------------------
# 1. Price Distribution
# -------------------------------
st.header("1. Price Distribution")
fig1 = px.box(filtered_df, x="price", points="all")
st.plotly_chart(fig1)

# -------------------------------
# 2. Rating vs Price
# -------------------------------
st.header("2. Rating vs Price")
fig2 = px.scatter(filtered_df, x="price", y="rating", size="review_count",
                  hover_name="product_name")
st.plotly_chart(fig2)

# -------------------------------
# 3. Top Reviewed Products
# -------------------------------
st.header("3. Top Reviewed Products")
top_reviewed = filtered_df.nlargest(10, "review_count")
st.table(top_reviewed[["product_name", "review_count", "price", "rating"]])

# -------------------------------
# 4. Best Value Score per Category
# -------------------------------
st.header("4. Best Value Score per Category")
best_value = (
    df.groupby("category_url")["value_score"]
      .mean()
      .sort_values(ascending=False)
      .reset_index()
)
fig4 = px.bar(best_value, x="category_url", y="value_score")
st.plotly_chart(fig4)

# -------------------------------
# 5. Review Count Distribution
# -------------------------------
st.header("5. Stock Availability (Review Count Distribution)")
fig5 = px.histogram(filtered_df, x="review_count", nbins=20)
st.plotly_chart(fig5)
