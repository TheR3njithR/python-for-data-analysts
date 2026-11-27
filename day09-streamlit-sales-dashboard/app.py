import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sales dashboard", layout="wide")


@st.cache_data
def load_data(path="data/sales.csv"):
    df = pd.read_csv(path, parse_dates=["order_date"])
    df["month"] = df["order_date"].dt.strftime("%Y-%m")
    return df


df = load_data()
st.title("Godavari Traders: sales dashboard")
st.caption("Synthetic demo data, Jan to Sep 2026")

with st.sidebar:
    st.header("Filters")
    all_cities = sorted(df["city"].unique())
    cities = st.multiselect("City", all_cities, default=all_cities)
    all_cats = sorted(df["category"].unique())
    cats = st.multiselect("Category", all_cats, default=all_cats)
    channel = st.radio("Channel", ["All", "Online", "Store"])

view = df[df["city"].isin(cities) & df["category"].isin(cats)]
if channel != "All":
    view = view[view["channel"] == channel]
if view.empty:
    st.warning("No orders match these filters.")
    st.stop()

revenue = view["revenue"].sum()
orders = len(view)
c1, c2, c3 = st.columns(3)
c1.metric("Revenue", f"₹{revenue / 1e5:,.2f} lakh")
c2.metric("Orders", f"{orders:,}")
c3.metric("Average order value", f"₹{revenue / orders:,.0f}")

left, right = st.columns(2)
left.subheader("Revenue by month")
left.line_chart(view.groupby("month")["revenue"].sum())
right.subheader("Revenue by category")
right.bar_chart(view.groupby("category")["revenue"].sum())

st.subheader("Top 5 products")
top = (view.groupby("product", as_index=False)["revenue"].sum()
       .nlargest(5, "revenue"))
st.dataframe(top, hide_index=True)
st.download_button("Download these rows (CSV)", view.to_csv(index=False),
                   file_name="filtered_sales.csv")
