import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="SAP Business Data Cloud Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# Custom CSS Styling
# ---------------------------------------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #eaf2ff 0%, #f8fbff 50%, #eef7f3 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #0b1f3a, #1e3a5f);
        color: white;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .main-title {
        text-align: center;
        color: #14213d;
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }

    .sub-title {
        text-align: center;
        color: #334155;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .desc-text {
        text-align: center;
        color: #475569;
        font-size: 17px;
        margin-bottom: 28px;
    }

    .metric-card {
        padding: 20px 14px;
        border-radius: 18px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.10);
        text-align: center;
        color: white;
        margin-bottom: 8px;
    }

    .metric-blue {
        background: linear-gradient(135deg, #2563eb, #38bdf8);
    }

    .metric-purple {
        background: linear-gradient(135deg, #7c3aed, #c084fc);
    }

    .metric-green {
        background: linear-gradient(135deg, #059669, #34d399);
    }

    .metric-orange {
        background: linear-gradient(135deg, #ea580c, #fb923c);
    }

    .metric-pink {
        background: linear-gradient(135deg, #db2777, #f472b6);
    }

    .metric-card h4 {
        font-size: 16px;
        margin-bottom: 10px;
        opacity: 0.95;
    }

    .metric-card h2 {
        font-size: 32px;
        margin: 0;
        font-weight: 800;
    }

    .section-box {
        background: rgba(255,255,255,0.88);
        backdrop-filter: blur(6px);
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
        margin-bottom: 20px;
        border: 1px solid rgba(148,163,184,0.12);
    }

    .insight-box {
        background: linear-gradient(135deg, #eff6ff, #f8fafc);
        padding: 18px;
        border-radius: 16px;
        border-left: 6px solid #2563eb;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.06);
    }

    .footer-note {
        text-align: center;
        color: #64748b;
        font-size: 14px;
        margin-top: 10px;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #cbd5e1, transparent);
        margin-top: 24px;
        margin-bottom: 24px;
    }

    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #2563eb, #0ea5e9);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-weight: 600;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        opacity: 0.92;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df.columns = df.columns.str.strip()

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce", dayfirst=False)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce", dayfirst=False)
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

    df = df.dropna(subset=["Order Date", "Sales"])

    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order Date"].dt.year
    df["Order Day"] = df["Order Date"].dt.day_name()

    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df.loc[(df["Shipping Days"] < 0) | (df["Shipping Days"] > 30), "Shipping Days"] = np.nan

    return df

df = load_data()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
st.sidebar.markdown("## 🎛 Filter Panel")

region_options = sorted(df["Region"].dropna().unique().tolist())
category_options = sorted(df["Category"].dropna().unique().tolist())
segment_options = sorted(df["Segment"].dropna().unique().tolist())
year_options = sorted(df["Year"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect("Select Region", region_options, default=region_options)
selected_categories = st.sidebar.multiselect("Select Category", category_options, default=category_options)
selected_segments = st.sidebar.multiselect("Select Segment", segment_options, default=segment_options)
selected_years = st.sidebar.multiselect("Select Year", year_options, default=year_options)

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories)) &
    (df["Segment"].isin(selected_segments)) &
    (df["Year"].isin(selected_years))
]

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.markdown("<div class='main-title'>📊 Sales Analytics Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>SAP Business Data Cloud Architecture (Simulated)</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='desc-text'>This project simulates a Business Data Cloud workflow: "
    "<b>Data Source → Data Processing → Business Analytics → Dashboard Insights</b></div>",
    unsafe_allow_html=True
)

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------------------------------------------------
# KPI Calculations
# ---------------------------------------------------
total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()
avg_order_value = total_sales / total_orders if total_orders else 0
avg_shipping_days = filtered_df["Shipping Days"].dropna().mean()
avg_shipping_days = round(avg_shipping_days, 2) if not np.isnan(avg_shipping_days) else 0

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"<div class='metric-card metric-blue'><h4>Total Sales</h4><h2>${total_sales:,.2f}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card metric-purple'><h4>Total Orders</h4><h2>{total_orders:,}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card metric-green'><h4>Total Customers</h4><h2>{total_customers:,}</h2></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card metric-orange'><h4>Avg Order Value</h4><h2>${avg_order_value:,.2f}</h2></div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='metric-card metric-pink'><h4>Avg Shipping Days</h4><h2>{avg_shipping_days}</h2></div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------
# Plotly Theme Helper
# ---------------------------------------------------
def style_plotly(fig):
    fig.update_layout(
        plot_bgcolor="rgba(255,255,255,0.95)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#1e293b", size=14),
        margin=dict(l=20, r=20, t=30, b=20),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial"
        ),
        xaxis=dict(
            showgrid=False,
            linecolor="#cbd5e1",
            tickfont=dict(color="#475569")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#e2e8f0",
            zeroline=False,
            tickfont=dict(color="#475569")
        )
    )
    return fig

# ---------------------------------------------------
# Monthly Sales Trend
# ---------------------------------------------------
st.markdown("## 📈 Monthly Sales Trend")
st.markdown("<div class='section-box'>", unsafe_allow_html=True)

monthly_sales = filtered_df.groupby("Month", as_index=False)["Sales"].sum().sort_values("Month")

fig_month = go.Figure()
fig_month.add_trace(go.Scatter(
    x=monthly_sales["Month"],
    y=monthly_sales["Sales"],
    mode="lines+markers",
    line=dict(color="#2563eb", width=4, shape="spline"),
    marker=dict(size=8, color="#38bdf8"),
    fill="tozeroy",
    fillcolor="rgba(37, 99, 235, 0.10)",
    hovertemplate="<b>Month:</b> %{x}<br><b>Sales:</b> %{y:,.2f}<extra></extra>"
))
fig_month = style_plotly(fig_month)
st.plotly_chart(fig_month, width="stretch")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Region and Category
# ---------------------------------------------------
col6, col7 = st.columns(2)

with col6:
    st.markdown("## 🌍 Sales by Region")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    region_sales = filtered_df.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        text_auto=".2s",
        color="Region",
        color_discrete_sequence=["#2563eb", "#0ea5e9", "#38bdf8", "#7dd3fc"]
    )
    fig_region = style_plotly(fig_region)
    fig_region.update_layout(showlegend=False)
    st.plotly_chart(fig_region, width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

with col7:
    st.markdown("## 📦 Sales by Category")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    category_sales = filtered_df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.48,
        color="Category",
        color_discrete_sequence=["#7c3aed", "#a855f7", "#c084fc"]
    )
    fig_category.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Sales: %{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )
    fig_category.update_layout(
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#1e293b", size=14),
        margin=dict(l=20, r=20, t=20, b=20),
        legend_title_text=""
    )
    st.plotly_chart(fig_category, width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Segment and State
# ---------------------------------------------------
col8, col9 = st.columns(2)

with col8:
    st.markdown("## 🧑‍💼 Sales by Segment")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    segment_sales = filtered_df.groupby("Segment", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig_segment = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        hole=0.45,
        color="Segment",
        color_discrete_sequence=["#10b981", "#34d399", "#6ee7b7"]
    )
    fig_segment.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Sales: %{value:,.2f}<br>Share: %{percent}<extra></extra>"
    )
    fig_segment.update_layout(
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(color="#1e293b", size=14),
        margin=dict(l=20, r=20, t=20, b=20),
        legend_title_text=""
    )
    st.plotly_chart(fig_segment, width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

with col9:
    st.markdown("## 🗺 Top 10 States by Sales")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    state_sales = filtered_df.groupby("State", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False).head(10)
    fig_state = px.bar(
        state_sales,
        x="Sales",
        y="State",
        orientation="h",
        text_auto=".2s",
        color="Sales",
        color_continuous_scale="Sunset"
    )
    fig_state = style_plotly(fig_state)
    fig_state.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig_state, width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Top Customers and Products
# ---------------------------------------------------
col10, col11 = st.columns(2)

with col10:
    st.markdown("## 👥 Top 10 Customers by Sales")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    top_customers = (
        filtered_df.groupby(["Customer ID", "Customer Name"], as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    st.dataframe(top_customers, width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

with col11:
    st.markdown("## 🛒 Top 10 Products by Sales")
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)

    top_products = (
        filtered_df.groupby(["Product Name"], as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    fig_products = px.bar(
        top_products.sort_values("Sales", ascending=True),
        x="Sales",
        y="Product Name",
        orientation="h",
        text_auto=".2s",
        color="Sales",
        color_continuous_scale="Blues"
    )
    fig_products = style_plotly(fig_products)
    st.plotly_chart(fig_products, width="stretch")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Detailed Data
# ---------------------------------------------------
st.markdown("## 📋 Detailed Sales Data")
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.dataframe(filtered_df, width="stretch")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Download
# ---------------------------------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇ Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# Insights
# ---------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("## 💡 Business Insights")

top_region = region_sales.iloc[0]["Region"] if not region_sales.empty else "N/A"
top_category = category_sales.iloc[0]["Category"] if not category_sales.empty else "N/A"
top_segment = segment_sales.iloc[0]["Segment"] if not segment_sales.empty else "N/A"

st.markdown("<div class='insight-box'>", unsafe_allow_html=True)
st.write(f"• The highest sales contribution comes from the **{top_region}** region.")
st.write(f"• The best performing category is **{top_category}**.")
st.write(f"• The strongest customer segment is **{top_segment}**.")
st.write("• The dashboard helps analyze sales patterns, customer distribution, regional performance, product demand, and decision-making priorities.")
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='footer-note'>Developed as a simulated SAP Business Data Cloud project using Python, Plotly, and Streamlit.</div>", unsafe_allow_html=True)