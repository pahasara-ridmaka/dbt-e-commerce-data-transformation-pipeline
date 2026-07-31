import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import random

# Set page config
st.set_page_config(
    page_title="E-commerce Analytics Dashboard", page_icon="📊", layout="wide"
)


@st.cache_data
def load_data():
    # Generate sample data for users, products, promotions, and orders
    # Create engine for duckdb
    import os

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.abspath(os.path.join(base_dir, "../dbt/dev.duckdb"))
    engine = create_engine(f"duckdb:////{db_path}")

    # Load data from DuckDB

    orders = pd.read_sql("SELECT * FROM fct_orders", engine)
    users = pd.read_sql("SELECT * FROM dim_users", engine)
    products = pd.read_sql("SELECT * FROM dim_products", engine)
    promotions = pd.read_sql("SELECT * FROM dim_promotions", engine)

    return users, products, promotions, orders


# Load data
users, products, promotions, orders = load_data()

print(
    f"Users: {len(users)}, Products: {len(products)}, Promotions: {len(promotions)}, Orders: {len(orders)}"
)


# Sidebar filters
st.sidebar.title("🎛️ Filters")

# Date range filter
min_date = orders["order_date"].min()
max_date = orders["order_date"].max()
date_range = st.sidebar.date_input(
    "Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

# Region filter - using region_name for display
region_options = orders["region"].unique()
regions = st.sidebar.multiselect(
    "Region", options=region_options, default=region_options
)

# Category filter
category_options = products["category"].unique()
categories = st.sidebar.multiselect(
    "Category", options=category_options, default=category_options
)

# Date range filter
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date

# Price Range Filter
min_price = float(orders["total_amount"].min())
max_price = float(orders["total_amount"].max())
price_range = st.sidebar.slider(
    "Total Amount Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=1.0,
)


# Apply filters
filtered_data = orders[
    # use between
    (orders["order_date"].between(start_date, end_date))
    & (orders["region"].isin(regions))
    & (orders["category"].isin(categories))
    & (orders["total_amount"].between(price_range[0], price_range[1]))
]

# Check if filtered_data is empty
if len(filtered_data) == 0:
    st.warning("No data matches the selected filters. Please adjust your filters.")
    st.stop()

# Main Dashboard
st.title("📊 E-commerce Analytics Dashboard")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        f"{len(filtered_data):,}",
        # delta to compare with total revenue
        delta=f"{len(filtered_data) - len(orders):,} from total orders",
    )

with col2:
    total_revenue = filtered_data["total_amount"].sum()
    st.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}",
        # delta compare with total revenue as a percentage
        delta=f"{((total_revenue - orders['total_amount'].sum()) / orders['total_amount'].sum() * 100):.1f}% vs total",
    )

with col3:
    avg_order_value = filtered_data["total_amount"].mean()
    st.metric(
        "Avg Order Value",
        f"${avg_order_value:.2f}",
        # compare delta with average in numerical format
        delta=f"{(avg_order_value - orders['total_amount'].mean()):,.2f}",
    )

with col4:
    unique_customers = filtered_data["user_id"].nunique()
    st.metric(
        "Unique Customers",
        f"{unique_customers:,}",
        delta=f"{unique_customers - orders['user_id'].nunique():,} from total",
    )

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue Over Time")
    revenue_by_date = (
        filtered_data.groupby("order_date")["total_amount"].sum().reset_index()
    )
    fig = px.line(
        revenue_by_date,
        x="order_date",
        y="total_amount",
        title="Daily Revenue Trend",
        labels={"order_date": "Date", "total_amount": "Revenue ($)"},
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏷️ Revenue by Category")
    revenue_by_category = (
        filtered_data.groupby("category")["total_amount"].sum().reset_index()
    )
    fig = px.pie(
        revenue_by_category,
        values="total_amount",
        names="category",
        title="Revenue Distribution by Category",
        hole=0.3,
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Orders by Region")
    orders_by_region = filtered_data["region"].value_counts().reset_index()
    orders_by_region.columns = ["region", "count"]
    fig = px.bar(
        orders_by_region,
        x="region",
        y="count",
        title="Order Distribution by Region",
        color="region",
        text="count",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📦 Top Products by Revenue")
    top_product_df = (
        filtered_data.groupby("product_id")["total_amount"].sum().reset_index()
    )
    top_product_df = top_product_df.merge(
        products[["product_id", "product_name"]], on="product_id", how="left"
    )
    top_products = (
        top_product_df.groupby("product_name")["total_amount"]
        .sum()
        .sort_values(ascending=True)
        .head(10)
    )
    if len(top_products) > 0:
        fig = px.bar(
            x=top_products.values,
            y=top_products.index,
            orientation="h",
            title="Top 10 Products by Revenue",
            labels={"x": "Revenue ($)", "y": "Product"},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No product data available")

# Additional Metrics - Row 3
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Inventory Status")
    inventory_counts = products["inventory_status"].value_counts()
    fig = px.pie(
        values=inventory_counts.values,
        names=inventory_counts.index,
        title="Inventory Status Distribution",
        hole=0.3,
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Promotion Usage")
    # Simulate promotion usage (since we don't have direct link)
    promo_usage = promotions.copy()
    promo_usage["usage_count"] = [
        random.randint(0, 100) for _ in range(len(promotions))
    ]
    fig = px.bar(
        promo_usage,
        x="promotion_code",
        y="usage_count",
        title="Promotion Usage",
        color="discount_percentage",
        labels={"promotion_code": "Promo Code", "usage_count": "Times Used"},
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.subheader("👥 Customer Signups")
    users["signup_date"] = pd.to_datetime(users["signup_date"])
    signup_by_month = (
        users.groupby(users["signup_date"].dt.to_period("M"))
        .size()
        .reset_index(name="count")
    )
    signup_by_month["month"] = signup_by_month["signup_date"].dt.to_timestamp()
    fig = px.line(
        signup_by_month,
        x="month",
        y="count",
        title="Monthly Customer Signups",
        markers=True,
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# Additional Insights - Row 4
st.subheader("📊 Additional Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Revenue by Customer")
    # Top customers by revenue
    top_customers = (
        filtered_data.groupby("user_id")
        .agg({"total_amount": "sum", "full_name": "first"})
        .sort_values("total_amount", ascending=False)
        .head(10)
    )

    fig = px.bar(
        top_customers,
        x="full_name",
        y="total_amount",
        title="Top 10 Customers by Revenue",
        labels={"full_name": "Customer", "total_amount": "Total Revenue ($)"},
        color="total_amount",
        color_continuous_scale="Viridis",
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📦 Product Performance")
    # Product metrics
    product_metrics = (
        filtered_data.groupby("product_id")
        .agg({"total_amount": ["sum", "mean", "count"]})
        .round(2)
    )
    product_metrics.columns = ["Total Revenue", "Avg Order Value", "Number of Orders"]
    product_metrics = product_metrics.sort_values(
        "Total Revenue", ascending=False
    ).head(10)

    st.dataframe(
        product_metrics,
        use_container_width=True,
        column_config={
            "Total Revenue": st.column_config.NumberColumn(
                "Total Revenue", format="$%.2f"
            ),
            "Avg Order Value": st.column_config.NumberColumn(
                "Avg Order Value", format="$%.2f"
            ),
            "Number of Orders": st.column_config.NumberColumn(
                "Number of Orders", format="%d"
            ),
        },
    )

# Detailed Data Table
st.subheader("📋 Order Details")
st.dataframe(
    filtered_data.sort_values("order_date", ascending=False).head(100),
    use_container_width=True,
    hide_index=True,
    column_config={
        "order_id": "Order ID",
        "user_id": "User ID",
        "full_name": "Customer",
        "region": "Region Code",
        "region_name": "Region",
        "product_id": "Product ID",
        "product_name": "Product",
        "category": "Category",
        "order_date": st.column_config.DateColumn("Order Date"),
        "total_amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
        "emali": "Email",
        "signup_date": st.column_config.DateColumn("Signup Date"),
    },
)

# Download button for filtered data
csv = filtered_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name=f"filtered_orders_data_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)

# Footer
st.markdown("---")
st.markdown(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

