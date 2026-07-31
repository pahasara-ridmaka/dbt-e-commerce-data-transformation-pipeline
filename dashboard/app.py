import streamlit as st
import pandas as pd
from datetime import datetime 
from sqlalchemy import create_engine
from plotly import express as px


st.set_page_config(
    page_title="Project Alpha Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

@st.cache_data
def get_data():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    db_path = os.path.abspath(os.path.join(base_dir, "../project_alpha/dev.duckdb"))

    engine = create_engine(f"duckdb:////{db_path}")

    df_fct_orders = pd.read_sql("SELECT * FROM main.fct_orders", engine)
    return df_fct_orders

# Load dataset
df_fct_orders = get_data()

# ==================== SIDEBAR FILTERS ====================
st.sidebar.title("Filters")

# Date range filter
min_date = df_fct_orders['order_date'].min()
max_date = df_fct_orders['order_date'].max()



date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# Category Filter
categories = st.sidebar.multiselect(
    "Select Product Categories",
    options=df_fct_orders['category'].unique(),
    default=df_fct_orders['category'].unique()
)

# Region Filter
regions = st.sidebar.multiselect(
    "Select Regions",
    options=df_fct_orders['region'].unique(),
    default=df_fct_orders['region'].unique()
)

# Amout Range Filter
min_amount = float(df_fct_orders['total_amount'].min())
max_amount = float(df_fct_orders['total_amount'].max())
amount_range = st.sidebar.slider(
    "Select Total Amount Range",
    min_value=min_amount,
    max_value=max_amount,
    value=(min_amount, max_amount),
    step=5.0
)

# ==================== APPLY FILTERS ====================

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.error("Please select a valid date range.")
    st.stop()

filtered_df = df_fct_orders[
    df_fct_orders['order_date'].between(start_date, end_date) &
    df_fct_orders['category'].isin(categories) &
    df_fct_orders['region'].isin(regions) &
    df_fct_orders['total_amount'].between(amount_range[0], amount_range[1])
]

# ==================== TOP METRIC ROW  ====================
st.title("E-commerce Sales Dashboard")
st.markdown(f"*Showing {len(filtered_df)} orders from   {date_range[0]} to {date_range[1]}*")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['total_amount'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}", delta=f"{((total_revenue - df_fct_orders['total_amount'].sum()) / df_fct_orders['total_amount'].sum() * 100):.1f}% vs total")

with col2:
    avg_order_value = filtered_df['total_amount'].mean()
    st.metric("Average Order Value", f"${avg_order_value:,.2f}")

with col3:
    total_orders = len(filtered_df)
    st.metric("Total Orders", f"{total_orders:,}")

with col4:
    unique_customers = filtered_df['user_id'].unique()
    st.metric("Unique Customers", f"{len(unique_customers):,}")

st.divider()


# ==================== ROW 1. Time Series+ Category Breakdown ====================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Revenue Over Time")
    daily_revenue = filtered_df.groupby("order_date")['total_amount'].sum().reset_index()
    fig_line = px.line(
        daily_revenue,
        x='order_date',
        y='total_amount',
        title='Daily Revenue Trend',
        labels={'order_date': 'Date', 'total_amount': 'Revenue ($)'},
        template='plotly_white'
    )
    fig_line.update_layout(height=400)
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Revenue by Category")
    category_revenue = filtered_df.groupby("category")['total_amount'].sum().sort_values(ascending=True).reset_index()

    fig_bar = px.bar(
        category_revenue,
        x="total_amount",
        y="category",
        orientation='h',
        title="Revenue by Product Category",
        labels={'total_amount': 'Revenue ($)', 'category': ''},
        color = 'total_amount',
        color_continuous_scale='Blues',
        template='plotly_white'
        
    )
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)


# ==================== ROW 2. Regional + Product Analysis ====================

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Region")
    region_revenue = filtered_df.groupby("region")['total_amount'].sum().reset_index()

    fig_pie = px.pie(
        region_revenue,
        values='total_amount',
        names='region',
        title='Regional Revenue Distribution',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Top 10 Products by Revenue")
    top_products = filtered_df.groupby("product_id")['total_amount'].sum().sort_values(ascending=True).head(10).reset_index()

    fig_top = px.bar(
        top_products,
        x='product_id',
        y='total_amount',
        title='Top 10 Products by Revenue',
        labels={'product_id': 'Product ID', 'total_amount': 'Revenue ($)'},
        color='total_amount',
        color_continuous_scale='Viridis',
        template='plotly_white'


    )
    fig_top.update_layout(height=400)
    st.plotly_chart(fig_top, use_container_width=True)


# ==================== ROW 3. Scatter Plot & Data table ====================
st.divider()

col1, col2 = st.columns([3, 2])


with col1:
    st.subheader("Order Value Distribution")

    fig_scatter = px.scatter(
        filtered_df.sample(min(1000, len(filtered_df))),
        x='order_date',
        y='total_amount',
        color='category',
        hover_data=['user_id', 'region'],
        title="Orders: Date vs Amount (Color = Category)",
        labels={'order_date': 'Order Date', 'total_amount': 'Total Amount ($)'},
        template='plotly_white'
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.subheader("Recent Orders")
    # Show last 10 orders
    recent_orders = filtered_df.sort_values(by='order_date', ascending=False).head(10)
    st.dataframe(
        recent_orders[['order_date','full_name', 'region', 'category', 'total_amount']],
        use_container_width=True,
        hide_index=True,
        column_config={
            'order_date': 'Date',
            'full_name': 'Customer',
            'total_amount': st.column_config.NumberColumn("Amount ($)", format="$%.2f"),


    })

    # Download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name= f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )

# ====================  Heatmap (Pivot table) ====================
st.divider()
st.subheader("Revenue Heatmap: Category vs Region Headmap")


# Create pivot table
pivot_df = filtered_df.pivot_table(
    values='total_amount',
    index='category',
    columns='region',
    aggfunc='sum',
    fill_value=0
)

fig_heatmap = px.imshow(
    pivot_df,
    text_auto='.2f',
    aspect='auto',
    title="Revenue Heatmap: Category vs Region",
    labels = dict(x="Region", y="Category", color="Revenue ($)"),
    color_continuous_scale='RdBu_r',
    template='plotly_white'
)
fig_heatmap.update_layout(height=400)
st.plotly_chart(fig_heatmap, use_container_width=True)

# ====================  Footer ====================
st.divider()
st.caption(f"Dashboard last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
