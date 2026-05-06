import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.colors as pc
import plotly.express as px
import numpy as np

product_kpi = pd.read_csv("data/product_kpi.csv")
division_kpi = pd.read_csv("data/division_kpi.csv")

st.set_page_config(
    page_title="Nassau Candy | Profitability Analysis",
    page_icon="📊",
    layout="wide",
)
st.title("🍬 Nassau Candy Profitability Dashboard")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ================= DESIGN SYSTEM (GLOBAL TOKENS) ================ */
:root {
    --bg0: #07091A;
    --bg1: #0B0E24;
    --bg2: #10152E;

    --card: rgba(255,255,255,0.04);
    --border: rgba(255,255,255,0.07);

    --text: #E6EAF2;     /* slightly brighter */
    --muted: #8B9BB4;    /* better contrast */

    --primary: #A78BFA;
    --cyan: #2DD4BF;
    --red: #FF6B6B;
    --yellow: #FFB347;

    --radius-sm: 10px;
    --radius-md: 14px;
    --radius-lg: 18px;
}
/* ============ GLOBAL APP BACKGROUND ============== */
html, body {
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

/* Apply ONLY to UI, NOT charts */
.stMarkdown, .stText, label, p, span { color: var(--text);}
.stApp {
    background: radial-gradient(circle at top, #0B1220, #070A12 70%);
    color: var(--text);
}
#MainMenu { visibility: visible !important; }
footer { visibility: hidden; }
/* KEEP HEADER (IMPORTANT FIX) */
header { background: transparent !important; }
header [data-testid="stToolbar"] * { color: white !important;}
header button * { color: white !important;}
header svg {  fill: white !important; }

/* =========== MAIN LAYOUT SPACING==============*/
.block-container {
    padding: 1.2rem 1.8rem;
    max-width: 100% !important;
}

/* CLEAN TAG STYLE (LIKE RIGHT DASHBOARD) */
[data-baseweb="tag"] {
    background: rgba(167,139,250,0.25) !important;
    color: #c8d0e8 !important;

    font-size: 1rem !important;   /* 🔥 FIXED */
    font-weight: 500;

    border-radius: 6px !important;

    padding: 4px 10px !important;  /* balanced */
    margin: 3px !important;

    border: 1px solid rgba(167,139,250,0.35) !important;
    box-shadow: none !important;
}
/* ── CLEAN PREMIUM SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1120 0%, #0d1525 100%);
    border-right: 1px solid rgba(167,139,250,0.15);
    width: 320px ;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0px 6px 0px 12px !important;
    margin: 0 !important;
}
/* Text hierarchy */
section[data-testid="stSidebar"] label {
    font-size: 0.75rem;
    color: #8a94b2 !important;
    margin-bottom: 2px !important;
}
/* Inputs */
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] .stDateInput input {
    background: #111827 !important;
    border: 1px solid rgba(167,139,250,0.25) !important;
    border-radius: 8px !important;
    color: #c8d0e8 !important;
}
/* Multiselect box */
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #111827 !important;
    border: 1px solid rgba(167,139,250,0.25) !important;
    border-radius: 8px !important;
    width: 100% !important;
    min-width: 100% !important;
}
section[data-testid="stSidebar"] input[role="combobox"] {
    opacity: 0.1 !important;
    color: transparent !important;
    caret-color: transparent !important;
}
/* Spacing */
section[data-testid="stSidebar"] .stDateInput,
section[data-testid="stSidebar"] .stSlider {
    margin-bottom: 10px !important;
}
/* FORCE FULL WIDTH SELECT */
section[data-testid="stSidebar"] .stMultiSelect {
    width: 100% !important;
    margin-bottom:8px !important;
}
/* remove inner shrinking */
section[data-testid="stSidebar"] [data-baseweb="select"] {
    width: 100% !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 4px !important;
}
/* 🧠 SIDEBAR TITLE*/
section[data-testid="stSidebar"] h1 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #E2E8F0 !important;

    /*  glow highlight */
    text-shadow: 0 0 8px rgba(167,139,250,0.35);
}
/*  LABELS (clean hierarchy)*/
section[data-testid="stSidebar"] input:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 6px rgba(167,139,250,0.25);
}
/* Tight spacing like premium dashboards */
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stDateInput,
section[data-testid="stSidebar"] .stSlider {
    margin-bottom: 10px !important;
}
/*  REMOVE INNER LIMITING CONTAINER */
section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div {
    width: 100% !important;
    min-width: 100% !important;
}
/*SECTION SPACING (BIG IMPROVEMENT) */
section[data-testid="stSidebar"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stSlider {
    margin-bottom: 10px !important;
}
section[data-testid="stSidebar"] .stMultiSelect,
section[data-testid="stSidebar"] .stDateInput {
    margin-bottom: 12px !important;
}

/*============📊 KPI CARDS (CLEAN SAAS STYLE)============*/
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    transition: transform 0.2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
}
[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    color: var(--muted) !important;
}

/*==========📊 CHART CONTAINERS (FIX SCROLL + CLIPPING)=========*/
[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 10px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);

    /* FIX SCROLL ISSUES */
    overflow: hidden !important;
    max-height:  100% !important ;
}
.main .block-container {
    max-width: 100% !important;
}
/* Plotly internal fix */
.js-plotly-plot .plotly {
    overflow: hidden !important;
}
/*TABS (CLEAN MODERN STYLE)*/
button[data-baseweb="tab"] {
    font-size: 0.82rem !important;
    font-weight: 500;
    padding: 6px 10px !important;
    margin-right: 6px;
}
button[data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 2px solid #A78BFA !important;
}
g.slicetext text {
    font-size: 11px !important;
    font-weight: 600 !important;
}
g.slicetext {
    word-break: break-word !important;
}
.css-1kyxreq, .css-1v0mbdj {
    gap: 0.6rem !important;
}

@media (max-width: 1200px) {
    .block-container {
        padding: 1rem;
    }
    section[data-testid="stSidebar"] {
        width: 280px !important;
    }
}
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1rem 0;
}
.stPlotlyChart {
    overflow: hidden !important;
}
[data-testid="stPlotlyChart"] {
    min-width: 0 !important;
    overflow: hidden !important;
}
.js-plotly-plot {
    width: 100% !important;
}
* {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ======= INSIGHT BOX (STABLE VERSION) ======= */
.insight-box {
    padding: 14px 16px;
    border-radius: 12px;
    margin-top: 12px;
    font-size: 13px;
    line-height: 1.5;
    color: #cbd5e1;
    border-left: 4px solid;
}
.insight-label {
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 4px;
    text-transform: uppercase;
}
/* TYPES */
.insight-info {
    border-color: #A78BFA;
    background: rgba(167,139,250,0.10);
}
.insight-good {
    border-color: #00F5D4;
    background: rgba(0,245,212,0.10);
}
.insight-warning {
    border-color: #FFD166;
    background: rgba(255,209,102,0.10);
}
.insight-danger {
    border-color: #FF4D6D;
    background: rgba(255,77,109,0.10);
}
/* ========== DATAFRAME CLEAN LOOK ========== */
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.05);
}
/* Reduce vertical gaps */
.stMarkdown {
    margin-bottom: 4px !important;
}

/* ======= DATE INPUT DARK STYLE ======= */
section[data-testid="stSidebar"] .stDateInput input {
    background: #111827 !important;   /* dark bg */
    color: #c8d0e8 !important;       /* text color */
    border: 1px solid rgba(167,139,250,0.25) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] {
    box-shadow: inset 0 0 40px rgba(167,139,250,0.05);
}
/* calendar popup */
section[data-testid="stSidebar"] .stDateInput {
    color: #c8d0e8 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

@st.cache_data
def load_data(path="data/cleaned_data.csv"):

    df = pd.read_csv(path)

    # 🧹 CLEANING
    df.columns = df.columns.str.strip()

    # Date handling (important)
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Order Date"])

    # 🔤 PRODUCT NORMALIZATION
    df["Product Name Clean"] = df["Product Name"].astype(str).str.strip().str.lower()

    # 📊 CORE METRICS
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0)
    df["Cost"] = pd.to_numeric(df["Cost"], errors="coerce").fillna(0)
    df["Gross Profit"] = pd.to_numeric(df["Gross Profit"], errors="coerce").fillna(0)
    df["Units"] = pd.to_numeric(df["Units"], errors="coerce").fillna(0)

    # Avoid divide-by-zero
    df = df[df["Sales"] > 0]
    df["Units"] = df["Units"].fillna(0)

    df["Gross Margin %"] = np.where(
        df["Sales"] > 0, (df["Gross Profit"] / df["Sales"]) * 100, 0
    )
    # 📦 FINAL SAFETY
    df = df.replace([float("inf"), -float("inf")], 0)

    return df

def get_chart_theme(mode="dark"):

    T = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=36, l=40, r=42),
        font=dict(family="Inter", color="#CBD5F5", size=12),
        title_font=dict(size=14, color="#FFFFFF", family="Inter"),
        hoverlabel=dict(
            bgcolor="#0B1220", bordercolor="#A78BFA", font_size=12, font_family="Inter"
        ),
    )
    # PAL = [
    # "#A78BFA",  "#34D399",   "#FF6B6B", "#FBBF24",   
    # "#38BDF8",   "#F472B6",   "#818CF8",  "#2DD4BF",   ]
    PAL=["#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF","#FFFFFF"]
    return T, PAL

def sfig(fig, T, xtitle="", ytitle="", height=420, title=""):
    fig.update_layout(**T, height=height)

    if title:
        fig.update_layout(
            title=dict(
                text=title,
                x=0.02,
                xanchor="left",
                font=dict(size=14, color="#E6EAF2", family="Inter"),
            )
        )
    if xtitle:
        fig.update_xaxes(title_text=xtitle)
    if ytitle:
        fig.update_yaxes(title_text=ytitle)

    fig.update_xaxes(showgrid=False, zeroline=False, color="#6b7280")

    fig.update_yaxes(
        showgrid=True,
        gridcolor=(
            "rgba(255,255,255,0.05)" if T["template"] == "plotly_dark" else "#E5E7EB"
        ),
        zeroline=False,
        color="#8B9BB4",
    )

    return fig

def insight_box(text, type="info"):

    label_map = {
        "info": "Insight",
        "good": "Strong Signal",
        "warning": "Watch Area",
        "danger": "Risk Area",
    }
    label = label_map.get(type, "Insight")
    
    st.markdown(
        f"""
        <div class="insight-box insight-{type}">
            <div class="insight-label">{label}</div>
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def simple_hover(name, sales=None, profit=None, margin=None):
    text = f"<b>{name}</b><br>"
    if sales is not None:
        text += f"Sales: ₹{sales:,.0f}<br>"
    if profit is not None:
        text += f"Profit: ₹{profit:,.0f}<br>"
    if margin is not None:
        text += f"Margin: {margin:.2f}%"
    return text


def add_median_lines(fig, x=None, y=None, color="#A78BFA", opacity=0.7):
    if x is not None:
        fig.add_vline(x=x, line_dash="dash", line_color=color, opacity=opacity)
    if y is not None:
        fig.add_hline(y=y, line_dash="dash", line_color=color, opacity=opacity)


def render_sidebar(df):
    st.sidebar.markdown(
        """
### 🧠 Segment Filters
<span style='color:#8a94b2;font-size:12px;'></span>
""",
        unsafe_allow_html=True,
    )

    # DATE
    min_date = df["Order Date"].min()
    max_date = df["Order Date"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if len(date_range) != 2:
        st.warning("Select valid date range")
        st.stop()

    # DIVISION
    selected_divisions = st.sidebar.multiselect(
        "Select Division",
        options=sorted(df["Division"].dropna().unique()),
        default=sorted(df["Division"].dropna().unique()),
    )

    # PRODUCT
    product_list = sorted(df["Product Name Clean"].dropna().unique())

    name_map = dict(zip(df["Product Name Clean"], df["Product Name"]))

    selected_products = st.sidebar.multiselect(
        "Select Products",
        options=product_list,
        default=product_list,
        format_func=lambda x: name_map.get(x, x).title(),
    )

    # 📊 MARGIN
    margin_range = st.sidebar.slider(
        "Margin % Range",
        float(df["Gross Margin %"].min()),
        float(df["Gross Margin %"].max()),
        (
            float(df["Gross Margin %"].min()),
            float(df["Gross Margin %"].max()),
        ),
    )

    def map_factory(name):
        name = str(name).lower()

        if "wonka bar" in name:
            if "milk chocolate" in name or "triple dazzle caramel" in name:
                return "Wicked Choccy's"
            else:
                return "Lot's O' Nuts"

        elif any(x in name for x in ["nerds", "sweetarts", "fun dip", "fizzy"]):
            return "Sugar Shack"

        elif any(x in name for x in ["gobstopper", "wonka gum", "lickable"]):
            return "Secret Factory"

        elif any(x in name for x in ["kazookles", "hair toffee"]):
            return "The Other Factory"

        return "Unknown"

    df["Factory"] = df["Product Name Clean"].apply(map_factory)

    # fallback using contains (important 🔥)
    df.loc[
        df["Factory"].isna() & df["Product Name Clean"].str.contains("chocolate"),
        "Factory",
    ] = "Wicked Choccy's"

    df["Factory"] = df["Factory"].fillna("Unknown")
    factory_options = sorted(df["Factory"].unique())

    selected_factories = st.sidebar.multiselect(
        "Select Factory",
        options=factory_options,
        default=factory_options,
    )

    return {
        "date_range": date_range,
        "divisions": selected_divisions,
        "products": selected_products,
        "margin_range": margin_range,
        "factories": selected_factories,
    }


def apply_filters(df, filters):
    filtered_df = df.copy()

    # DATE
    start, end = filters["date_range"]

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= pd.to_datetime(start))
        & (filtered_df["Order Date"] <= pd.to_datetime(end))
    ]

    # DIVISION
    if filters["divisions"]:
        filtered_df = filtered_df[filtered_df["Division"].isin(filters["divisions"])]

    # FACTORY
    if filters["factories"]:
        filtered_df = filtered_df[filtered_df["Factory"].isin(filters["factories"])]

    # PRODUCT
    if filters["products"]:
        filtered_df = filtered_df[
            filtered_df["Product Name Clean"].isin(filters["products"])
        ]
    # MARGIN
    min_m, max_m = filters["margin_range"]

    filtered_df = filtered_df[
        (filtered_df["Gross Margin %"] >= min_m)
        & (filtered_df["Gross Margin %"] <= max_m)
    ]

    # EMPTY CHECK
    if filtered_df.empty:
        st.warning("No data available for selected filters")
        st.stop()

    return filtered_df


def shorten_product_name(name):
    name = str(name)

    lower = name.lower()

    if lower.startswith("wonka bar -"):
        name = "WK" + name[11:]  # 🔥 removes prefix safely

    # Trim long names
    return name if len(name) <= 18 else name[:16] + "…"


def kpi_section(filtered_df, full_df):

    # SAFE DIVISION
    def safe_div(a, b):
        return a / b if b != 0 else 0

    data = filtered_df

    # ================ KPI CALCULATIONS =================

    # 1. Gross Margin %
    gross_margin = safe_div(data["Gross Profit"].sum(), data["Sales"].sum()) * 100

    # 2. Profit per Unit
    profit_per_unit = safe_div(data["Gross Profit"].sum(), data["Units"].sum())

    # 3. Revenue Contribution (vs FULL DATA)
    revenue_contribution = safe_div(data["Sales"].sum(), full_df["Sales"].sum()) * 100

    # 4. Profit Contribution (vs FULL DATA)
    profit_contribution = (
        safe_div(data["Gross Profit"].sum(), full_df["Gross Profit"].sum()) * 100
    )

    # 5. Margin Volatility
    monthly_margin = data.groupby(pd.Grouper(key="Order Date", freq="ME"))[
        "Gross Margin %"
    ].mean()

    volatility = monthly_margin.std()

    # ===================== KPI DISPLAY =====================
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Gross Margin %", f"{gross_margin:.2f}%")
    col2.metric("Profit per Unit", f"₹{profit_per_unit:.2f}")
    col3.metric("Revenue Contribution", f"{revenue_contribution:.2f}%")
    col4.metric("Profit Contribution", f"{profit_contribution:.2f}%")
    col5.metric("Margin Volatility", f"{volatility:.2f}")


def build_others_hover(df, title="📦 Other Products", value_col="Value", max_items=8):
    if df.empty:
        return "<b>No additional products</b>"

    hover = f"<b>{title}</b><br><br>"

    for i, (_, row) in enumerate(df.iterrows()):
        if i < max_items:
            hover += f"• {row['Product Name']} → " f"₹{row[value_col]:,.0f}<br>"

    if len(df) > max_items:
        hover += f"<br>+{len(df)-max_items} more..."

    return hover


T, PAL = get_chart_theme("dark")

df = load_data()

sidebar = render_sidebar(df)  # get filters
filtered_df = apply_filters(df, sidebar)  # apply filters


def subtab1_leaderboard(filtered_df, T, PAL):
    st.markdown("## 🏆 Product Leaderboard & Contribution")

    # 🔹 DATA PREP
    product_summary = (
        filtered_df.groupby("Product Name")
        .agg({"Sales": "sum", "Gross Profit": "sum"})
        .reset_index()
    )

    product_summary["Margin %"] = (
        product_summary["Gross Profit"] / product_summary["Sales"] * 100
    )

    # Safety
    product_summary = product_summary.replace([np.inf, -np.inf], 0).fillna(0)

    top_n = min(5, len(product_summary))

    top_products = product_summary.sort_values(by="Gross Profit", ascending=False).head(
        top_n
    )

    bottom_products = product_summary.sort_values(
        by="Gross Profit", ascending=True
    ).head(top_n)
    col1, col2 = st.columns(2)

    # 🔝 TOP PRODUCTS
    # 🎯 SMART COLOR BASED ON PROFIT INTENSITY
    colors_top = []
    q75 = top_products["Gross Profit"].quantile(0.75)
    q40 = top_products["Gross Profit"].quantile(0.40)

    for val in top_products["Gross Profit"]:
        if val >= q75:
            colors_top.append("#34D399")
        elif val >= q40:
            colors_top.append("#FBBF24")
        else:
            colors_top.append("#FF6B6B")

    fig_top = go.Figure()

    fig_top.add_bar(
        y=top_products["Product Name"],  # ✅ FIXED
        x=top_products["Gross Profit"],  # ✅ FIXED
        orientation="h",
        marker=dict(
            color=colors_top,
            line=dict(width=1.5, color="#0B1220"),
            cornerradius=6,
        ),
        text=[f"₹{v:,.0f}" for v in top_products["Gross Profit"]],
        textposition="outside",
        textfont=dict(size=12, family="Inter"),
        customdata=top_products[["Sales", "Margin %"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Profit: ₹%{x:,.0f}<br>"
            "Sales: ₹%{customdata[0]:,.0f}<br>"
            "Margin: %{customdata[1]:.2f}%<extra></extra>"
        ),
    )

    fig_top.update_layout(
        yaxis=dict(autorange="reversed"),
        title_y=0.98,
        **T,
    )
    fig_top.update_traces(cliponaxis=False)  # 🚀 allows text to go outside safely

    fig_top = sfig(fig_top, T, "Profit", "", title="🏆 Top Profit Drivers")
    col1.plotly_chart(fig_top, use_container_width=True)

    # ------ bottom -----
    colors_bottom = []
    q30 = bottom_products["Gross Profit"].quantile(0.30)

    for val in bottom_products["Gross Profit"]:
        if val < 0:
            colors_bottom.append("#FF6B6B")
        elif val < q30:
            colors_bottom.append("#FF6B6B")
        else:
            colors_bottom.append("#FBBF24")

    fig_bottom = go.Figure()

    fig_bottom.add_bar(
        y=bottom_products["Product Name"],  # ✅ FIXED
        x=bottom_products["Gross Profit"],  # ✅ FIXED
        orientation="h",
        marker=dict(
            color=colors_bottom, line=dict(width=1.5, color="#0B1220"), cornerradius=6
        ),
        text=[f"₹{v:,.0f}" for v in bottom_products["Gross Profit"]],
        textposition="outside",
        textfont=dict(size=12, family="Inter"),
        customdata=bottom_products[["Sales", "Margin %"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Profit: ₹%{x:,.0f}<br>"
            "Sales: ₹%{customdata[0]:,.0f}<br>"
            "Margin: %{customdata[1]:.2f}%<extra></extra>"
        ),
    )

    fig_bottom.update_layout(
        yaxis=dict(autorange="reversed"),
        **T,
    )
    fig_bottom.update_traces(cliponaxis=False)  # 🚀 allows text to go outside safely

    fig_bottom = sfig(
        fig_bottom, T, "Profit", "", title="🔻 Low Profit / Risk Products"
    )
    col2.plotly_chart(fig_bottom, use_container_width=True)
    insight_box(
        "Top products drive majority of profit. Protect them while improving weaker ones.",
        "good",
    )

    # =============  REVENUE vs PROFIT GAP ==============
    gap_df = (
        filtered_df.groupby("Product Name")
        .agg({"Sales": "sum", "Gross Profit": "sum"})
        .reset_index()
    )

    gap_df = gap_df.sort_values(by="Gross Profit", ascending=False)

    top_n = 5
    top_df = gap_df.head(top_n)
    others_df = gap_df.iloc[top_n:]

    top_df = top_df.copy()

    # HOVER TEXT
    top_df["Hover"] = top_df.apply(
        lambda x: simple_hover(
            x["Product Name"].title(),
            sales=x["Sales"],
            profit=x["Gross Profit"],
            margin=(x["Gross Profit"] / x["Sales"]) * 100,
        ),
        axis=1,
    )

    if not others_df.empty:
        others_list = [
            f"{row['Product Name'].title()} → ₹{row['Gross Profit']:,.0f} ({(row['Gross Profit']/row['Sales'])*100:.1f}%)"
            for _, row in others_df.iterrows()
        ]

        others_hover = "<b>Others</b><br><br>" + "<br>".join(others_list)

        others_row = pd.DataFrame(
            {
                "Product Name": ["Others"],
                "Sales": [others_df["Sales"].sum()],
                "Gross Profit": [others_df["Gross Profit"].sum()],
                "Hover": [others_hover],
            }
        )

        gap_df = pd.concat([top_df, others_row], ignore_index=True)
    else:
        gap_df = top_df.copy()

    # PROFIT RATIO + COLORS 🎯
    gap_df["Profit Ratio"] = gap_df["Gross Profit"] / gap_df["Sales"]

    gap_df["Short Name"] = gap_df["Product Name"].apply(shorten_product_name)

    # CHANGE:
    def get_color(r):
        if r < 0.2:   return "#F87171"
        elif r < 0.4: return "#FBBF24"
        else:         return "#34D399"
    
    colors = [get_color(r) for r in gap_df["Profit Ratio"]]

    # BAR POSITIONS
    bar_width = 0.35
    labels = gap_df["Short Name"].tolist()
    x = np.arange(len(labels))

    x_rev = x - bar_width / 2
    x_profit = x + bar_width / 2

    # FIGURE
    fig = go.Figure()

    # 🔹 Revenue (neutral tone)
    fig.add_bar(
        x=x_rev,
        y=gap_df["Sales"],
        width=bar_width,
        text=[f"₹{v:,.0f}" for v in gap_df["Sales"]],
        textposition="outside",
        name="Revenue",
        marker=dict(
            color="#94A3B8",  # solid modern grey
            opacity=0.35,  # 🔥 subtle neutral
            line=dict(width=0),
            cornerradius=6,
        ),
        customdata=gap_df["Hover"],
        hovertemplate="%{customdata}<extra></extra>",
    )

    # 🔹 Profit (highlight)
    fig.add_bar(
        x=x_profit,
        y=gap_df["Gross Profit"],
        width=bar_width,
        name="Profit",
        marker=dict(
            color=colors,
            line=dict(width=0),
            cornerradius=6,  # 🔥 modern UI
        ),
        text=[f"₹{v:,.0f}" for v in gap_df["Gross Profit"]],
        textposition="outside",
        cliponaxis=False,
        customdata=gap_df["Hover"],
        hovertemplate="%{customdata}<extra></extra>",
    )

    # AXIS CONTROL
    fig.update_xaxes(
        tickmode="array",
        tickvals=x,
        ticktext=labels,
        categoryorder="array",
        categoryarray=labels,
    )

    # LAYOUT (USING YOUR THEME)
    fig.update_layout(
        barmode="overlay",
        bargap=0.20,
        bargroupgap=0.05,
        showlegend=True,
        xaxis=dict(tickangle=0, tickfont=dict(size=11)),
        legend=dict(
            font=dict(color="#8a94b2", size=11),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            y=1.05,
            x=0.4,
        ),
        **T,
    )

    fig = sfig(
        fig,
        T,
        "Product",
        "Amount (₹)",
        title="💰 Revenue vs Profit Reality Check",
    )
    st.plotly_chart(fig, use_container_width=True)

    insight_box(
        "High revenue but low profit = pricing inefficiency. Focus on cost optimization.",
        "warning",
    )
    
    #  ======= PROFIT CONTRIBUTION (UPGRADED DONUT) ======
    donut_data = filtered_df.groupby("Product Name")["Gross Profit"].sum().reset_index()

    total_profit = donut_data["Gross Profit"].sum()

    # STEP 1: % CONTRIBUTION
    donut_data["Contribution %"] = donut_data["Gross Profit"] / total_profit * 100

    # STEP 2: GROUP SMALL VALUES
    threshold = 1.0

    small = donut_data[donut_data["Contribution %"] < threshold]
    large = donut_data[donut_data["Contribution %"] >= threshold].copy()

    # 🔹 NORMAL HOVER
    large["Hover"] = large.apply(
        lambda x: (
            f"<b>{x['Product Name']}</b><br>"
            f"Profit: ₹{x['Gross Profit']:,.0f}<br>"
            f"Share: {x['Contribution %']:.2f}%"
        ),
        axis=1,
    )

    # 🔥 OTHER HOVER (DETAILED)
    if not small.empty:

        other_profit = small["Gross Profit"].sum()
        other_share = (other_profit / total_profit) * 100

        other_hover = "<b>📦 Other Products:</b><br><br>"

        for _, row in small.iterrows():
            other_hover += (
                f"• {row['Product Name']} → ₹{row['Gross Profit']:,.0f} "
                f"({row['Contribution %']:.2f}%)<br>"
            )

        other_row = pd.DataFrame(
            {
                "Product Name": ["Other"],
                "Gross Profit": [other_profit],
                "Contribution %": [other_share],
                "Hover": [other_hover],
            }
        )

        donut_data = pd.concat([large, other_row], ignore_index=True)

    else:
        donut_data = large.copy()

    # SORT
    donut_data = donut_data.sort_values(by="Gross Profit", ascending=False)

    # BRIGHT COLOR PALETTE (FIXED)
    colors = [
    "#34D399",   
    "#A78BFA",   
    "#FBBF24",   
    "#38BDF8",   
    "#F472B6",   
    "#818CF8",   
    "#2DD4BF",   
    "#FF6B6B",   
]
    # PLOT
    fig_donut = go.Figure()

    fig_donut.add_pie(
        labels=donut_data["Product Name"],
        values=donut_data["Gross Profit"],
        hole=0.68,  
        marker=dict(
            colors=colors[: len(donut_data)],
            line=dict(color="#0f172a", width=2),  # clean separation
        ),
        textinfo="percent",
        textfont=dict(size=12, family="Inter", color="white"),
        customdata=donut_data["Hover"],
        hovertemplate="%{customdata}<extra></extra>",
    )

    # LAYOUT FIX (IMPORTANT)
    fig_donut.update_layout(
        height=420,
        title="🍩 Profit Contribution",
        showlegend=True,
        legend=dict(
            orientation="v",
            x=1.02,
            y=0.5,
            font=dict(size=11, color="#8a94b2"),),
        **T,)

    # 🧠 CENTER TEXT (PRO TOUCH)
    fig_donut.add_annotation(
        text=f"<b>Total</b><br>₹{total_profit:,.0f}",
        x=0.5,
        y=0.5,
        font=dict(size=14),
        showarrow=False,
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    insight_box(
        "A few products dominate profit . Focus on scaling these.",
        "info",
    )

    # ================= PRODUCT MIX (UPGRADED) =================
    tree_data = (
        filtered_df.groupby(["Division", "Product Name"])
        .agg({"Sales": "sum", "Gross Profit": "sum"})
        .reset_index()
    )

    # METRICS
    tree_data["Contribution %"] = tree_data["Sales"] / tree_data["Sales"].sum() * 100

    tree_data["Margin %"] = tree_data["Gross Profit"] / tree_data["Sales"] * 100

    # BRIGHT COLOR SCALE (DARK UI)
    def color_scale(m):
        if m < 20:   return "#FF6B6B"   # coral red
        elif m < 40: return "#FBBF24"   # amber
        elif m < 60: return "#FBBF24"   # amber (mid)
        elif m < 75: return "#38BDF8"   # sky blue
        else:        return "#34D399"   # emerald

    tree_data["Color"] = tree_data["Margin %"].apply(color_scale)  # 🟢 neon green

    # ---------- BUILD HIERARCHY -----------
    labels, parents, values, colors, hover_text = [], [], [], [], []

    # 🔹 DIVISION LEVEL (glass look)
    for div in tree_data["Division"].unique():
        div_df = tree_data[tree_data["Division"] == div]

        labels.append(f"📦 {div}")
        parents.append("")
        values.append(div_df["Sales"].sum())
        colors.append("#1E1B4B")  # dark tile (glass feel)

        hover_text.append(
            f"<b>{div}</b><br>"
            f"Sales: ₹{div_df['Sales'].sum():,.0f}<br>"
            f"Products: {len(div_df)}"
        )

    # 🔹 PRODUCT LEVEL
    for _, row in tree_data.iterrows():
        labels.append(row["Product Name"])
        parents.append(f"{row['Division']}")
        values.append(row["Sales"])
        colors.append(row["Color"])

        hover_text.append(
            f"<b>{row['Product Name']}</b><br>"
            f"Sales: ₹{row['Sales']:,.0f}<br>"
            f"Margin: {row['Margin %']:.1f}%<br>"
            f"Share: {row['Contribution %']:.2f}%"
        )

    # PLOT
    fig_tree = go.Figure(
        go.Treemap(
            labels=labels,
            parents=parents,
            values=values,
            marker=dict(
                colors=colors,
                line=dict(width=2, color="#070A12"),  # 🔥 clean borders
            ),
            branchvalues="total",
            customdata=hover_text,
            hovertemplate="%{customdata}<extra></extra>",
        )
    )
    # TEXT + LAYOUT FIX
    fig_tree.update_traces(
        textinfo="label+percent parent",
        texttemplate="<b>%{label}</b><br>%{percentParent:.1%}",
        textfont=dict(color="#FFFFFF"),  # 🔥 bigger + bright
        insidetextfont=dict(color="#FFFFFF"),
        marker=dict(line=dict(width=3, color="#070A12")),  
    )

    fig_tree.update_layout(
        height=520,
        legend=dict(font=dict(color="#8a94b2")),
        title="🌳 Product Mix & Margin Structure",
        uniformtext=dict(minsize=11, mode="show"),
        **T,
    )

    st.plotly_chart(fig_tree, use_container_width=True)
    insight_box(
        "Green = high margin, Red = low margin. Optimize red zones for better profitability.",
        "danger",
    )


def subtab2_performance_segmentation(filtered_df, T, PAL):
    st.markdown("## 📈 Product Performance Segmentation")

    view = st.radio(
        "Select Analysis View",
        ["Profit vs Sales", "Margin vs Sales"],
        horizontal=True,
        key="perf_view",
    )

    # 🔹 DATA
    perf = (
        filtered_df.groupby("Product Name")
        .agg({"Sales": "sum", "Gross Profit": "sum", "Gross Margin %": "mean"})
        .reset_index()
    )

    perf = perf[(perf["Sales"] > 0) & (perf["Gross Profit"].notna())]

    # 🔹 MEDIANS
    sales_median = perf["Sales"].median()
    profit_median = perf["Gross Profit"].median()
    margin_median = perf["Gross Margin %"].median()

    # COLOR SYSTEM (USING PAL)
    COLOR_STRONG = PAL[1]  # green
    COLOR_RISK = PAL[2]  # red
    COLOR_OPP = PAL[4]  # blue
    COLOR_WEAK = PAL[3]  # yellow

    def get_color(row):
        if view == "Profit vs Sales":
            if row["Sales"] >= sales_median and row["Gross Profit"] >= profit_median:
                return COLOR_STRONG
            elif row["Sales"] >= sales_median:
                return COLOR_RISK
            elif row["Gross Profit"] >= profit_median:
                return COLOR_OPP
            else:
                return COLOR_WEAK
        else:
            if row["Sales"] >= sales_median and row["Gross Margin %"] >= margin_median:
                return COLOR_STRONG
            elif row["Sales"] >= sales_median:
                return COLOR_RISK
            elif row["Gross Margin %"] >= margin_median:
                return COLOR_OPP
            else:
                return COLOR_WEAK

    # 🔹 SIZE
    size_values = (
        (perf["Sales"] - perf["Sales"].min())
        / (perf["Sales"].max() - perf["Sales"].min() + 1e-9)
    ) * 35 + 12

    size_values = size_values.clip(10, 50)

    # 🔹 FIGURE
    fig = go.Figure()

    if view == "Profit vs Sales":
        fig.add_scatter(
            x=perf["Sales"],
            y=perf["Gross Profit"],
            mode="markers",
            marker=dict(
                size=size_values,
                color=perf.apply(get_color, axis=1),
                line=dict(width=2, color="#0B1220"),
                opacity=0.9,
            ),
            text=perf["Product Name"],
            customdata=perf[["Gross Margin %"]],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Sales: ₹%{x:,.0f}<br>"
                "Profit: ₹%{y:,.0f}<br>"
                "Margin: %{customdata[0]:.2f}%<extra></extra>"
            ),
        )
        fig.update_layout(xaxis_title="Sales", yaxis_title="Gross Profit")

    else:
        fig.add_scatter(
            x=perf["Sales"],
            y=perf["Gross Margin %"],
            mode="markers",
            marker=dict(
                size=size_values,
                color=perf.apply(get_color, axis=1),
                line=dict(width=2, color="#0B1220"),
                opacity=0.9,
            ),
            text=perf["Product Name"],
            customdata=perf[["Gross Profit"]],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Sales: ₹%{x:,.0f}<br>"
                "Margin: %{y:.2f}%<br>"
                "Profit: ₹%{customdata[0]:,.0f}<extra></extra>"
            ),
        )

        fig.update_layout(xaxis_title="Sales", yaxis_title="Margin %")
    add_median_lines(
        fig,
        x=sales_median,
        y=profit_median if view == "Profit vs Sales" else margin_median,
        color=PAL[0],
    )
    # 🔹 APPLY THEME
    fig.update_layout(title=f"📈 {view}", height=520, **T)

    st.plotly_chart(fig, use_container_width=True)

    # 💡 INSIGHT
    insight_box(
        "Colors: Green = Strong, Red = Risk, Blue = Opportunity, Yellow = Weak.",
        "info",
    )

    # ============= COST vs SALES (EFFICIENCY) =============

    cost_df = (
        filtered_df.groupby("Product Name")
        .agg(
            {
                "Sales": "sum",
                "Cost": "sum",
                "Gross Profit": "sum",
                "Gross Margin %": "mean",
            }
        )
        .reset_index()
    )

    cost_df = cost_df[(cost_df["Sales"] > 0) & (cost_df["Cost"] > 0)]

    # SIZE (reused same logic style)
    size_vals = (
        (cost_df["Gross Profit"] - cost_df["Gross Profit"].min())
        / (cost_df["Gross Profit"].max() - cost_df["Gross Profit"].min() + 1e-9)
    ) * 40 + 12

    size_vals = size_vals.clip(10, 55)

    # COLOR BASED ON MARGIN (CONSISTENT WITH YOUR SYSTEM)
    def cost_color(m):
        if m < 20:
            return PAL[2]  # red 
        elif m < 40:
            return PAL[3]  # yellow
        elif m < 60:
            return PAL[4]  # opportunity
        else:
            return PAL[1]  # strong

    colors = cost_df["Gross Margin %"].apply(cost_color)

    # 📊 FIGURE
    fig_cost = go.Figure()

    fig_cost.add_scatter(
        x=cost_df["Cost"],
        y=cost_df["Sales"],
        mode="markers",
        marker=dict(
            size=size_vals,
            color=colors,
            opacity=0.9,
            line=dict(width=1.2, color=PAL[0]),  # glow edge
        ),
        text=cost_df["Product Name"],
        customdata=cost_df[["Gross Profit", "Gross Margin %"]],
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Cost: ₹%{x:,.0f}<br>"
            "Sales: ₹%{y:,.0f}<br>"
            "Profit: ₹%{customdata[0]:,.0f}<br>"
            "Margin: %{customdata[1]:.2f}%<extra></extra>"
        ),
    )

    # MEDIAN LINES 
    cost_median = cost_df["Cost"].median()
    sales_median = cost_df["Sales"].median()

    add_median_lines(fig_cost, cost_median, sales_median, PAL[0], 0.7)

    # FINAL LAYOUT
    fig_cost.update_layout(
        height=520,
        xaxis_title="Cost",
        yaxis_title="Sales",
        **T,
    )

    fig_cost = sfig(
        fig_cost,
        T,
        "Cost",
        "Sales",
        title="💸 Cost vs Sales Efficiency",
    )
    st.plotly_chart(fig_cost, use_container_width=True)

    insight_box(
        "High cost + low sales = inefficiency. Low cost + high sales = scalable winners.",
        "warning",
    )


def subtab3_margin_stability(filtered_df, T, PAL):

    # ============== REVENUE TRAP CHART ===============

    trap_df = (
        filtered_df.groupby("Product Name")
        .agg({"Sales": "sum", "Gross Profit": "sum"})
        .reset_index()
    )

    # Profit Ratio
    trap_df["Profit Ratio"] = trap_df["Gross Profit"] / trap_df["Sales"]

    TOP_N = 7

    trap_df = trap_df.sort_values(by="Sales", ascending=False)

    top_df = trap_df.head(TOP_N).copy()
    others_df = trap_df.iloc[TOP_N:].copy()

    # -------------- HOVER FOR TOP PRODUCTS --------------
    
    top_df["Hover"] = top_df.apply(
        lambda x: simple_hover(
            x["Product Name"],
            sales=x["Sales"],
            profit=x["Gross Profit"],
            margin=(x["Gross Profit"] / x["Sales"]) * 100,
        ),
        axis=1,
    )

    if not others_df.empty:

        other_sales = others_df["Sales"].sum()
        other_profit = others_df["Gross Profit"].sum()
        other_ratio = other_profit / other_sales if other_sales != 0 else 0

        others_hover = "<b>📦 Other Products</b><br><br>"

        for _, row in others_df.iterrows():
            others_hover += (
                f"• {row['Product Name']} → "
                f"₹{row['Sales']:,.0f} | "
                f"{row['Profit Ratio']:.2f}<br>"
            )

        other_row = pd.DataFrame(
            {
                "Product Name": ["Other"],
                "Sales": [other_sales],
                "Gross Profit": [other_profit],
                "Profit Ratio": [other_ratio],
                "Hover": [others_hover],
            }
        )
        # Original order (Top N already sorted by Sales)

        if "Other" in trap_df["Product Name"].values:
            other_row = trap_df[trap_df["Product Name"] == "Other"]
            rest = trap_df[trap_df["Product Name"] != "Other"]

            trap_df = pd.concat([rest, other_row], ignore_index=True)
        else:
            trap_df = pd.concat([top_df, other_row], ignore_index=True)
    else:
        trap_df = top_df.copy()

    # Ratio
    trap_df["Profit Ratio"] = trap_df["Gross Profit"] / trap_df["Sales"]

    trap_df["Short Name"] = trap_df["Product Name"].apply(shorten_product_name)

    # Move "Other" to end manually
    trap_df = trap_df.sort_values(by="Product Name", key=lambda col: col == "Other")

    # COLOR LOGIC (using your design system)
    def trap_color(r):
        if r < 0.2:
            return PAL[2]  # risk
        elif r < 0.4:
            return PAL[3]  # moderate
        else:
            return PAL[1]  # strong

    colors = trap_df["Profit Ratio"].apply(trap_color)

    # FIGURE
    fig_trap = go.Figure()

    fig_trap.add_bar(
        x=trap_df["Short Name"],
        y=trap_df["Sales"],
        marker=dict(color=colors, line=dict(width=0), cornerradius=6),
        text=[f"₹{v:,.0f}" for v in trap_df["Sales"]],
        textposition="outside",
        customdata=trap_df["Hover"],
        hovertemplate="%{customdata}<extra></extra>",
    )
    fig_trap.update_xaxes(
        tickangle=0,
        categoryorder="array",
        categoryarray=trap_df["Short Name"].tolist(),
    )

    # Layout polish
    fig_trap.update_layout(
        xaxis=dict(
            type="category",
            categoryorder="array",
            categoryarray=trap_df["Short Name"].tolist(),
        ),
        height=420,
        **T,
    )
    fig_trap = sfig(
        fig_trap,
        T,
        "Product",
        "Sales (₹)",
        title="🔥 Revenue Trap Analysis (High Sales, Low Profit)",
    )
    fig_trap.update_traces(cliponaxis=False)

    st.plotly_chart(fig_trap, use_container_width=True)

    insight_box(
        "Products with high sales but low profit are revenue traps. "
        "They consume resources without generating value — optimize pricing or reduce costs.",
        "danger",
    )

    # ================= LOW MARGIN PRODUCTS =================

    low_margin = (
        filtered_df.groupby("Product Name")
        .agg({"Sales": "sum", "Gross Profit": "sum"})
        .reset_index()
    )

    low_margin["Margin %"] = (low_margin["Gross Profit"] / low_margin["Sales"]) * 100

    margin_median = low_margin["Margin %"].median()

    # Filter worst performers
    low_margin = low_margin[low_margin["Margin %"] < margin_median].sort_values(
        "Margin %"
    )

    low_margin["Short Name"] = low_margin["Product Name"].apply(shorten_product_name)

    # Color logic (PAL)
    def lm_color(m):
        if m < margin_median * 0.5:
            return PAL[2]  # 🔴 worst
        elif m < margin_median:
            return PAL[3]  # 🟡 weak
        else:
            return PAL[1]

    colors = low_margin["Margin %"].apply(lm_color)

    # Chart
    fig_lm = go.Figure()

    fig_lm.add_bar(
        y=low_margin["Short Name"],
        x=low_margin["Margin %"],
        orientation="h",
        marker=dict(color=colors, cornerradius=6),
        text=[f"{v:.1f}%" for v in low_margin["Margin %"]],
        textposition="outside",
        customdata=low_margin[["Sales", "Gross Profit"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Margin: %{x:.2f}%<br>"
            "Sales: ₹%{customdata[0]:,.0f}<br>"
            "Profit: ₹%{customdata[1]:,.0f}<extra></extra>"
        ),
    )

    fig_lm.update_layout(height=420, **T)

    fig_lm = sfig(
        fig_lm,
        T,
        "Margin (%)",
        "Product",
        title="🔴 Margin Risk Products",
    )

    st.plotly_chart(fig_lm, use_container_width=True)

    insight_box(
        "Products below median margin are at risk of eroding profitability. "
        "Focus on cost control, pricing optimization, or portfolio cleanup.",
        "danger",
    )
    # ================= COST EFFICIENCY =================

    eff_df = (
        filtered_df.groupby("Product Name")
        .agg({"Cost": "sum", "Gross Profit": "sum"})
        .reset_index()
    )

    eff_df["Efficiency"] = eff_df["Gross Profit"] / eff_df["Cost"]

    eff_df = eff_df.sort_values(by="Efficiency", ascending=True).tail(10)

    eff_df["Short Name"] = eff_df["Product Name"].apply(shorten_product_name)

    def eff_color(v):
        if v < 0.2:
            return PAL[2]  
        elif v < 0.4:
            return PAL[3]  
        else:
            return PAL[1]  

    colors = eff_df["Efficiency"].apply(eff_color)

    fig_eff = go.Figure()

    fig_eff.add_bar(
        y=eff_df["Short Name"],
        x=eff_df["Efficiency"],
        orientation="h",
        marker=dict(color=colors, cornerradius=6),
        text=[f"{v:.2f}" for v in eff_df["Efficiency"]],
        textposition="outside",
        customdata=eff_df[["Cost", "Gross Profit"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Efficiency: %{x:.2f}<br>"
            "Cost: ₹%{customdata[0]:,.0f}<br>"
            "Profit: ₹%{customdata[1]:,.0f}<extra></extra>"
        ),
    )

    fig_eff = sfig(
        fig_eff,
        T,
        "Efficiency (Profit / Cost)",
        "",
        title="🟣 Cost Efficiency Ranking",
    )

    st.plotly_chart(fig_eff, use_container_width=True)

    insight_box(
        "Higher efficiency = better profit extraction from cost. Focus on scaling these products.",
        "info",
    )

    # MERGED ACTION DATASET

    action_df = (
        filtered_df.groupby("Product Name")
        .agg({"Sales": "sum", "Cost": "sum", "Gross Profit": "sum"})
        .reset_index()
    )

    # Core Metrics
    action_df["Margin %"] = (action_df["Gross Profit"] / action_df["Sales"]) * 100
    action_df["Efficiency"] = action_df["Gross Profit"] / action_df["Cost"]

    # Medians (dynamic benchmark)
    cost_median = action_df["Cost"].median()
    sales_median = action_df["Sales"].median()
    eff_median = action_df["Efficiency"].median()

    # ACTION ENGINE
    def action_logic(row):

        if row["Margin %"] < 40 and row["Cost"] > cost_median:
            return "🔴 Discontinue / Re-engineer"

        elif row["Efficiency"] < eff_median * 0.7:
            return "🟠 Reduce Cost"

        elif row["Margin %"] < 50:
            return "🟡 Reprice Product"

        elif row["Margin %"] > 70 and row["Sales"] > sales_median:
            return "🚀 Scale / Promote"

        else:
            return "🟢 Maintain"

    #  Styling
    def highlight_row(row):
        if "🔴" in row["Action"]:
            return ["background-color: rgba(255, 107, 107, 0.15)"] * len(row)
        elif "🟠" in row["Action"]:
            return ["background-color: rgba(251, 191, 36, 0.12)"] * len(row)
        elif "🟡" in row["Action"]:
            return ["background-color: rgba(251, 191, 36, 0.08)"] * len(row)
        elif "🚀" in row["Action"]:
            return ["background-color: rgba(52, 211, 153, 0.08)"] * len(row)
        else:
            return ["background-color: rgba(148, 163, 184, 0.08)"] * len(row)

    def color_action(val):
        if "🔴" in val:
            return "color: #FF6B6B; font-weight: 600;"
        elif "🟠" in val:
            return "color: #FBBF24; font-weight: 600;"
        elif "🟡" in val:
            return "color: #FBBF24; font-weight: 600;"
        elif "🚀" in val:
            return "color: #34D399; font-weight: 700;"
        else:
            return "color: #94A3B8;"

    # Apply
    action_df["Action"] = action_df.apply(action_logic, axis=1)

    action_df = action_df.sort_values("Margin %").reset_index(drop=True)

    action_df.insert(0, "Rank", action_df.index + 1)
    st.markdown("### 📋 Product Decision Engine")

    # 🎯 FORMAT DISPLAY (clean + professional)
    styled_df = (
        action_df.style.format(
            {
                "Sales": "₹{:,.0f}",
                "Cost": "₹{:,.0f}",
                "Gross Profit": "₹{:,.0f}",
                "Margin %": "{:.1f}%",
                "Efficiency": "{:.2f}",
            }
        )
        .map(color_action, subset=["Action"])
        .apply(highlight_row, axis=1)
        .set_properties(
            **{
                "background-color": "#0E1726",
                "color": "#E2E8F0",
                "border-color": "#1F2937",
            }
        )
    )
    # 🎯 KPI SUMMARY (clean + insightful)
    total = len(action_df)

    crit = (action_df["Action"].str.contains("🔴")).sum()
    cost_issue = (action_df["Action"].str.contains("🟠")).sum()
    scalable = (action_df["Action"].str.contains("🚀")).sum()

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.metric("🔴 Critical", crit, f"{crit/total:.0%} of products")

    with col2:
        st.metric("🟠 Cost Issues", cost_issue, f"{cost_issue/total:.0%} of products")

    with col3:
        st.metric("🚀 Scalable", scalable, f"{scalable/total:.0%} of products")

    st.dataframe(styled_df, use_container_width=True, height=420, hide_index=True)


def tab2_division_insights(filtered_df, T, PAL):
    div = (
        filtered_df.groupby("Division")
        .agg({"Sales": "sum", "Gross Profit": "sum", "Gross Margin %": "mean"})
        .reset_index()
    )

    div["Efficiency"] = div["Gross Profit"] / div["Sales"]
    div["Gap ₹"] = div["Sales"] - div["Gross Profit"]
    div["Margin %"] = (df["Gross Profit"] / df["Sales"]) * 100

    # =========== 1. REVENUE vs PROFIT ============
    fig = go.Figure()

    # 🔹 Revenue (neutral glass tone)
    fig.add_bar(
        x=div["Division"],
        y=div["Sales"],
        name="Revenue",
        marker=dict(
            color="rgba(203,213,225,0.25)",
            line=dict(width=0),
            cornerradius=6,
        ),
        customdata=div[["Gross Profit", "Gap ₹"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: ₹%{y:,.0f}<br>"
            "Profit: ₹%{customdata[0]:,.0f}<br>"
            "Gap: ₹%{customdata[1]:,.0f}"
            "<extra></extra>"
        ),
        text=[f"₹{v:,.0f}" for v in div["Sales"]],
        textposition="outside",
    )

    # 🔹 Profit (highlight)
    fig.add_bar(
        x=div["Division"],
        y=div["Gross Profit"],
        name="Profit",
        marker=dict(
            color=PAL[1],  # neon green
            line=dict(width=0),
            cornerradius=6,
        ),
        customdata=div[["Sales", "Gap ₹"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Profit: ₹%{y:,.0f}<br>"
            "Revenue: ₹%{customdata[0]:,.0f}<br>"
            "Gap: ₹%{customdata[1]:,.0f}<extra></extra>"
        ),
        text=[f"₹{v:,.0f}" for v in div["Gross Profit"]],
        textposition="outside",
    )

    fig.update_layout(
        barmode="group",
        legend=dict(orientation="h", y=1.05, x=0.4),
        **T,
    )

    fig = sfig(
        fig, T, "Division", "Amount (₹)", title="📊 Revenue vs Profit by Division"
    )
    fig.update_traces(cliponaxis=False)

    st.plotly_chart(fig, use_container_width=True)

    insight_box(
        "Divisions with high revenue but lower profit need pricing or cost optimization.",
        "warning",
    )

    # ============= 2. MARGIN EFFICIENCY ===============

    # 🎨 Smart color logic (no dull gradient)
    colors = []
    for m in div["Gross Margin %"]:
        if m < 30:
            colors.append(PAL[2])  # red
        elif m < 50:
            colors.append(PAL[3])  # yellow
        else:
            colors.append(PAL[1])  # green

    fig = go.Figure()

    fig.add_bar(
        x=div["Division"],
        y=div["Gross Margin %"],
        marker=dict(color=colors, line=dict(width=0), cornerradius=6),
        text=[f"{v:.1f}%" for v in div["Gross Margin %"]],
        textposition="outside",
        customdata=div[["Sales", "Gross Profit"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Margin: %{y:.2f}%<br>"
            "Profit: ₹%{customdata[1]:,.0f}<br>"
            "Sales: ₹%{customdata[0]:,.0f}<extra></extra>"
        ),
    )

    fig.update_layout(**T)

    fig = sfig(fig, T, "Division", "Margin %", title="💹 Margin Efficiency by Division")
    fig.update_traces(cliponaxis=False)

    st.plotly_chart(fig, use_container_width=True)

    insight_box(
        "Green divisions = high margin efficiency. Red zones need cost control.",
        "good",
    )

    # ================ 3. EFFICIENCY RANKING ===============
    div_sorted = div.sort_values("Efficiency")

    # 🎨 Gradient using PAL
    colors = []
    for val in div_sorted["Efficiency"]:
        if val < 0.25:
            colors.append(PAL[2])  # red
        elif val < 0.4:
            colors.append(PAL[3])  # yellow
        else:
            colors.append(PAL[1])  # green

    fig = go.Figure()

    fig.add_bar(
        y=div_sorted["Division"],
        x=div_sorted["Efficiency"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0), cornerradius=6),
        text=[f"{v:.2f}" for v in div_sorted["Efficiency"]],
        textposition="outside",
        customdata=div_sorted[["Sales", "Gross Profit"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Efficiency: %{x:.2f}<br>"
            "Profit: ₹%{customdata[1]:,.0f}<br>"
            "Sales: ₹%{customdata[0]:,.0f}<extra></extra>"
        ),
    )

    fig.update_layout(**T)

    fig = sfig(
        fig, T, "Efficiency (Profit/Sales)", "", title="⚙️ Division Efficiency Ranking"
    )
    fig.update_traces(cliponaxis=False)

    st.plotly_chart(fig, use_container_width=True)

    insight_box(
        "Higher efficiency = better profit extraction from revenue. Focus on scaling these divisions.",
        "info",
    )


def tab3_B(filtered_df, T, PAL):
    # ============ linechart over time ==============
    trend = (
        filtered_df.groupby(pd.Grouper(key="Order Date", freq="ME"))["Gross Margin %"]
        .mean()
        .reset_index()
    )

    trend["Month"] = trend["Order Date"].dt.strftime("%b %Y")
    trend["Prev"] = trend["Gross Margin %"].shift(1)
    trend["Change"] = trend["Gross Margin %"] - trend["Prev"]

    volatility = trend["Gross Margin %"].std()

    # 🔥 HOVER
    trend["Hover"] = trend.apply(
        lambda x: (
            # f"<b>{x['Month']}</b><br>"
            f"📈 Margin: {x['Gross Margin %']:.2f}%<br>"
            + (
                f"{'🟢 Increased' if x['Change']>0 else '🔴 Decreased'} "
                f"{abs(x['Change']):.2f}%"
                if pd.notnull(x["Change"])
                else ""
            )
        ),
        axis=1,
    )
    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        risk = "High" if volatility > 5 else "Moderate" if volatility > 3 else "Stable"

        st.metric(
            "📉 Volatility",
            f"{volatility:.2f}",
            delta=risk,
            delta_color="inverse" if volatility > 5 else "normal",
        )
    # 📊 CHART
    fig = go.Figure()

    # 🔹 LINE + MARKERS
    fig.add_scatter(
        x=trend["Order Date"],
        y=trend["Gross Margin %"],
        mode="lines+markers",
        line=dict(color=PAL[1], width=3),
        marker=dict(
            size=7,
            color=trend["Gross Margin %"],
            colorscale=[[0, PAL[2]], [0.5, PAL[3]], [1, PAL[1]]],
            line=dict(width=1, color="#0f172a"),
        ),
        customdata=trend["Hover"],
        hovertemplate="%{customdata}<extra></extra>",
    )

    # AREA FILL (premium feel)
    fig.add_scatter(
        x=trend["Order Date"],
        y=trend["Gross Margin %"],
        fill="tozeroy",
        mode="none",
        fillcolor="rgba(52,211,153,0.08)",
        hoverinfo="skip",
    )

    # 📏 AVG LINE
    avg_margin = trend["Gross Margin %"].mean()

    fig.add_hline(
        y=avg_margin,
        line_dash="dot",
        line_color=PAL[0],
        opacity=0.6,
        annotation_text="Avg",
        annotation_position="top right",
    )

    fig.update_layout(
        height=420,
        hovermode="x unified",
        xaxis_title="",
        yaxis_title="Margin %",
        **T,
    )

    fig = sfig(fig, T, "", "Margin %", title="📉 Margin Stability Over Time")

    st.plotly_chart(fig, use_container_width=True)

    insight_box(
        f"Margin volatility is {volatility:.2f}. "
        + (
            "High fluctuation → unstable pricing or cost structure."
            if volatility > 5
            else "Margins are stable over time."
        ),
        "info",
    )
    # ===== PARETO =======

    metric = st.radio(
        "Select Metric",
        ["Gross Profit", "Sales"],
        horizontal=True,
        key="pareto_metric",
    )

    # DATA PREP
    pareto = (
        filtered_df.groupby("Product Name")[metric]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    pareto.columns = ["Product Name", "Value"]

    # Cumulative %
    pareto["Contribution %"] = pareto["Value"] / pareto["Value"].sum() * 100
    pareto["Cumulative %"] = pareto["Value"].cumsum() / pareto["Value"].sum()

    # 80% SPLIT
    top_80 = pareto[pareto["Cumulative %"] <= 0.8]

    if len(top_80) < len(pareto):
        top_80 = pareto.iloc[: len(top_80) + 1]

    remaining = pareto.iloc[len(top_80) :]
    # GROUP OTHERS
    if not remaining.empty:
        others_value = remaining["Value"].sum()

        others_hover = "<b>📦 Other Products</b><br><br>"
        for _, row in remaining.iterrows():
            others_hover += f"• {row['Product Name']} → ₹{row['Value']:,.0f}<br>"

        others_row = pd.DataFrame(
            {
                "Product Name": [f"Others ({len(remaining)})"],
                "Value": [others_value],
                "Hover": [others_hover],
            }
        )

        top_80["Hover"] = top_80.apply(
            lambda x: (
                f"<b>{x['Product Name']}</b><br>"
                f"Value: ₹{x['Value']:,.0f}<br>"
                f"Contribution: {x['Contribution %']:.1f}%<br>"
                f"Cumulative: {x['Cumulative %']:.1f}%"
            ),
            axis=1,
        )

        final_df = pd.concat([top_80, others_row], ignore_index=True)

    else:
        final_df = top_80.copy()
        final_df["Hover"] = final_df.apply(
            lambda x: (
                f"<b>{x['Product Name']}</b><br>"
                f"Value: ₹{x['Value']:,.0f}<br>"
                f"Contribution: {x['Contribution %']:.1f}%<br>"
                f"Cumulative: {x['Cumulative %']:.1f}%"
            ),
            axis=1,
        )

    final_df["Cumulative %"] = final_df["Contribution %"].cumsum()
    final_df["Short Name"] = final_df["Product Name"].apply(shorten_product_name)

    # COLORS (Your Design System)
    colors = [
        PAL[1] if "Others" not in p else "#9CA3AF" for p in final_df["Product Name"]
    ]

    final_df["Cumulative %"] = final_df["Contribution %"].cumsum()

    # FIGURE
    x = np.arange(len(final_df))

    fig = go.Figure()

    fig.add_bar(
        x=x,
        y=final_df["Value"],
        marker=dict(color=colors, line=dict(width=0), cornerradius=6),
        text=[f"₹{v:,.0f}" for v in final_df["Value"]],
        textposition="outside",
        customdata=final_df["Hover"],
        hovertemplate="%{customdata}<extra></extra>",
        name=metric,
    )

    # 🔹 Cumulative Line
    fig.add_scatter(
        x=x,
        y=final_df["Cumulative %"],
        yaxis="y2",
        mode="lines+markers",
        customdata=final_df[["Product Name"]],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>" "Cumulative: %{y:.1f}%<extra></extra>"
        ),
        line=dict(color=PAL[0], width=3),
        name="Cumulative %",
    )

    # 🔹 80% Line
    fig.add_hline(
        y=0.8,
        line_dash="dash",
        line_color=PAL[2],
        opacity=0.7,
    )

    labels = final_df["Short Name"].tolist()

    fig.update_xaxes(
        tickmode="array",
        tickvals=x,
        ticktext=labels,
        tickangle=0,
    )

    # 🧱 LAYOUT (MATCH YOUR SYSTEM)
    fig.update_layout(
        height=460,
        yaxis=dict(title=metric),
        yaxis2=dict(
            overlaying="y",
            side="right",
            tickformat=".0%",
            title="Cumulative %",
        ),
        legend=dict(
            orientation="h",
            y=1.05,
            x=0.35,
        ),
        **T,
    )

    fig = sfig(fig, T, "Product", metric, title="📊 Pareto Analysis (80/20 Rule)")

    st.plotly_chart(fig, use_container_width=True)

    # 🧠 INSIGHT
    insight_box(
        f"{len(top_80)} products drive ~80% of {metric.lower()}. "
        + ("High dependency risk." if len(top_80) <= 5 else "Moderate concentration."),
        "info",
    )


tab1, tab2, tab3 = st.tabs(
    [
        "📊 Product Performance",
        "🏢 Division Insights",
        "📈 Business Stability & Risk Insights",
    ]
)

with tab1:
    kpi_section(filtered_df, df)
    tab1_sub1, tab1_sub2, tab1_sub3 = st.tabs(
        [
            "🏆 Leaderboard & Contribution",
            "💰 Cost vs Margin Diagnostics",
            "⚠️ Risk & Optimization",
        ]
    )
with tab1_sub1:
    subtab1_leaderboard(filtered_df, T, PAL)
with tab1_sub2:
    subtab2_performance_segmentation(filtered_df, T, PAL)
with tab1_sub3:
    subtab3_margin_stability(filtered_df, T, PAL)
with tab2:
    tab2_division_insights(filtered_df, T, PAL)
with tab3:
    tab3_B(filtered_df, T, PAL)
