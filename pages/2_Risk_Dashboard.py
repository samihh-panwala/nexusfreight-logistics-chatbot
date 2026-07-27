import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="NexusFreight Risk Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "https://nexusfreight-api.onrender.com"

# ==========================================================
# MODERN CSS (SAME AS AI ASSISTANT)
# ==========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ==========================================================
GENERAL
========================================================== */

html,
body,
[class*="css"]{

font-family:'Inter',sans-serif;

}

.stApp{

background:#F5F7F2;

}

#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

div[data-testid="stSidebarNav"]{
display:none;
}

.block-container{

padding-top:25px;
padding-left:45px;
padding-right:45px;
padding-bottom:20px;

}

/* ==========================================================
SIDEBAR
========================================================== */

section[data-testid="stSidebar"]{

background:#FCFDFB;

width:320px !important;

border-right:1px solid #D8E2D1;

}

/* ==========================================================
LOGO
========================================================== */

.logo-card{

background:linear-gradient(
135deg,
#6D8B74,
#8AA58A
);

padding:28px;

border-radius:22px;

margin-bottom:35px;

box-shadow:0 12px 28px rgba(109,139,116,.28);

}

.logo-title{

font-size:30px;

font-weight:700;

color:white;

margin-bottom:8px;

}

.logo-sub{

font-size:14px;

color:rgba(255,255,255,.92);

line-height:1.6;

}

/* ==========================================================
NAVIGATION
========================================================== */

.nav-title{

font-size:24px;

font-weight:700;

color:#5F7161;

letter-spacing:.4px;

margin-bottom:18px;

}

/* ==========================================================
BUTTONS
========================================================== */

.stButton>button{

width:100%;

height:78px;

background:#F7FAF5;

border:1px solid #D6E1D2;

border-radius:18px;

padding-left:22px;

transition:.25s;

box-shadow:0 5px 16px rgba(0,0,0,.04);

}

.stButton>button p{

font-size:20px !important;

font-weight:700 !important;

color:#4B5D4B !important;

text-align:left;

margin:0;

}

.stButton>button:hover{

background:#E7F1E4;

border-color:#6D8B74;

transform:translateY(-3px);

box-shadow:0 10px 22px rgba(109,139,116,.18);

}

/* Download Button */

div[data-testid="stDownloadButton"]>button{

width:100%;

height:78px;

background:#F7FAF5;

border:1px solid #D6E1D2;

border-radius:18px;

transition:.25s;

box-shadow:0 5px 16px rgba(0,0,0,.04);

}

div[data-testid="stDownloadButton"]>button p{

font-size:20px !important;

font-weight:700 !important;

color:#4B5D4B !important;

}

div[data-testid="stDownloadButton"]>button:hover{

background:#E7F1E4;

border-color:#6D8B74;

transform:translateY(-3px);

}

/* ==========================================================
STATUS CARD
========================================================== */

.status-card{

background:#FBFCFA;

padding:18px;

border-radius:18px;

border:1px solid #D7E2D1;

margin-top:20px;

box-shadow:0 6px 18px rgba(0,0,0,.03);

}

.status-title{

font-size:16px;

font-weight:700;

color:#4D644F;

margin-bottom:12px;

}

.status-item{

font-size:15px;

padding:7px 0;

color:#667566;

}

/* ==========================================================
HERO
========================================================== */

.hero{

background:#FCFDFB;

padding:42px;

border-radius:28px;

border:1px solid #D6E2D2;

box-shadow:0 12px 30px rgba(0,0,0,.05);

margin-bottom:35px;

}

.hero h1{

font-size:46px;

font-weight:700;

color:#4D644F;

margin-bottom:12px;

}

.hero p{

font-size:19px;

color:#667566;

line-height:1.8;

}

/* ==========================================================
SECTION TITLES
========================================================== */

.section-title{

font-size:30px;

font-weight:700;

color:#5F7161;

margin-top:15px;

margin-bottom:25px;

}


/* ==========================================================
PLOTLY CHART CARDS
========================================================== */

.element-container:has(.js-plotly-plot){

background:#FCFDFB;

padding:22px;

border-radius:22px;

border:1px solid #D7E2D1;

box-shadow:0 8px 22px rgba(109,139,116,.08);

margin-bottom:28px;

}

/* ==========================================================
METRIC CARDS
========================================================== */

/* ======================================
PREMIUM KPI CARDS
====================================== */

[data-testid="metric-container"]{

background:linear-gradient(
180deg,
#FCFDFB,
#F3F8F0
);

border:1px solid #D6E1D2;

border-radius:22px;

padding:25px;

box-shadow:0 12px 28px rgba(109,139,116,.12);

transition:.25s;

min-height:140px;

display:flex;

flex-direction:column;

justify-content:center;

}

[data-testid="metric-container"]:hover{

transform:translateY(-6px);

border-color:#7D9B80;

box-shadow:0 18px 38px rgba(109,139,116,.22);

}

[data-testid="metric-container"] label{

font-size:20px !important;

font-weight:700 !important;

color:#4D644F !important;

}

[data-testid="metric-container"] [data-testid="stMetricValue"]{

font-size:44px !important;

font-weight:800;

color:#37543B;

}

/* Space between KPI cards */

div[data-testid="column"]{

padding:6px;

}

/* ==========================================================
FILTER CARD
========================================================== */

div[data-testid="stVerticalBlockBorderWrapper"]{

background:#FCFDFB;

border-radius:22px;

border:1px solid #D7E2D1;

padding:22px;

box-shadow:0 8px 20px rgba(109,139,116,.08);

}

/* ==========================================================
SELECT BOX
========================================================== */

div[data-baseweb="select"]{

background:#F7FAF5 !important;

border-radius:16px !important;

border:1px solid #D7E2D1 !important;

min-height:48px;

}

div[data-baseweb="select"]:hover{

border-color:#6D8B74 !important;

}

/* Dropdown Selected Text */

div[data-baseweb="select"] span{

font-size:17px !important;

font-weight:600 !important;

color:#4D644F !important;

}

/* Dropdown Menu Items */

div[role="listbox"] div{

font-size:17px !important;

font-weight:500;

}

/* ==========================================================
TEXT INPUT
========================================================== */

.stTextInput label{

font-size:18px !important;

font-weight:700 !important;

color:#4D644F !important;

}

.stTextInput input{

background:#FCFDFB;

border:1px solid #D7E2D1;

border-radius:16px;

font-size:17px;

padding:14px;

color:#4D644F;

}

.stTextInput input:focus{

border-color:#6D8B74;

box-shadow:0 0 0 2px rgba(109,139,116,.12);

}

/* ==========================================================
DATAFRAME
========================================================== */

[data-testid="stDataFrame"]{

border-radius:20px;

border:1px solid #D7E2D1;

overflow:hidden;

background:#FCFDFB;

box-shadow:0 8px 20px rgba(109,139,116,.08);

}

/* ==========================================================
TABLE CONTAINER
========================================================== */

div[data-testid="stVerticalBlockBorderWrapper"] table{

font-size:14px;

}

thead tr{

background:#EDF4E8 !important;

}

thead th{

color:#4D644F !important;

font-weight:700 !important;

}

tbody tr:nth-child(even){

background:#FAFCF9;

}

/* ==========================================================
SPINNER
========================================================== */

div[data-testid="stSpinner"]{

background:#FCFDFB;

border-radius:18px;

padding:12px;

}

/* ==========================================================
INFO / SUCCESS / WARNING / ERROR
========================================================== */

div[data-testid="stAlert"]{

border-radius:18px;

font-size:16px;

padding:18px;

border:1px solid #D7E2D1;

}

/* ==========================================================
EXPANDER
========================================================== */

details{

border-radius:18px;

border:1px solid #D7E2D1;

background:#FCFDFB;

padding:10px;

}

/* ==========================================================
PLOTLY TOOLBAR
========================================================== */

.modebar{

background:transparent !important;

}

/* ==========================================================
SCROLLBAR
========================================================== */

::-webkit-scrollbar{

width:10px;

height:10px;

}

::-webkit-scrollbar-track{

background:#EEF4EB;

border-radius:10px;

}

::-webkit-scrollbar-thumb{

background:#B6C7B0;

border-radius:10px;

}

::-webkit-scrollbar-thumb:hover{

background:#90AA8B;

}

/* ==========================================================
DOWNLOAD BUTTON (PREMIUM)
========================================================== */

div[data-testid="stDownloadButton"]{

margin-top:10px;

}

div[data-testid="stDownloadButton"] > button{

width:100%;

height:78px;

background:#F7FAF5;

border:1px solid #D6E1D2;

border-radius:18px;

transition:.25s;

box-shadow:0 5px 16px rgba(0,0,0,.04);

}

div[data-testid="stDownloadButton"] > button p{

font-size:20px !important;

font-weight:700 !important;

color:#4B5D4B !important;

}

div[data-testid="stDownloadButton"] > button:hover{

background:#E7F1E4;

border-color:#6D8B74;

transform:translateY(-3px);

box-shadow:0 10px 22px rgba(109,139,116,.18);

}

/* ==========================================================
BUTTON ANIMATION
========================================================== */

.stButton>button,
div[data-testid="stDownloadButton"]>button{

transition:all .25s ease;

}

.stButton>button:active,
div[data-testid="stDownloadButton"]>button:active{

transform:scale(.98);

}

/* ==========================================================
CHART TITLES
========================================================== */

.js-plotly-plot .gtitle{

font-family:'Inter',sans-serif !important;

font-size:18px !important;

font-weight:700 !important;

fill:#4D644F !important;

}

/* ==========================================================
PLOTLY LEGENDS
========================================================== */

.js-plotly-plot text{

font-family:'Inter',sans-serif !important;

}

/* ==========================================================
CONTAINERS
========================================================== */

div[data-testid="stHorizontalBlock"]{

gap:1.2rem;

}

/* ==============================
FILTER LABELS
============================== */

label{

font-size:18px !important;

font-weight:700 !important;

color:#4D644F !important;

letter-spacing:0.3px;

}

/* ==========================================================
MARKDOWN HEADINGS
========================================================== */

h1{

color:#4D644F;

}

h2{

color:#5F7161;

}

h3{

color:#667566;

}

/* ==========================================================
LINKS
========================================================== */

a{

color:#6D8B74;

text-decoration:none;

}

a:hover{

color:#4D644F;

}

/* ==========================================================
FOOTER
========================================================== */

.footer{

text-align:center;

color:#708670;

font-size:14px;

margin-top:45px;

line-height:1.8;

}

.footer b{

color:#4D644F;

}

/* ==========================================================
SMOOTH FADE
========================================================== */

.stApp{

animation:fadeIn .35s ease-in-out;

}

@keyframes fadeIn{

from{

opacity:0;

transform:translateY(6px);

}

to{

opacity:1;

transform:translateY(0);

}

}

/* ==========================================================
REMOVE EXTRA STREAMLIT PADDING
========================================================== */

div[data-testid="stVerticalBlock"]{

gap:1rem;

}

/* ==========================================================
END
========================================================== */

</style>

""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("""

<div class="logo-card">

<div class="logo-title">

🚚 NexusFreight

</div>

<div class="logo-sub">

Enterprise Logistics Intelligence Platform

</div>

</div>

""", unsafe_allow_html=True)

    st.markdown(
        "<div class='nav-title'>Navigation</div>",
        unsafe_allow_html=True
    )

    if st.button(
        "🤖   AI Assistant",
        use_container_width=True
    ):
        st.switch_page("streamlit_app.py")

    if st.button(
        "📊   Risk Dashboard",
        use_container_width=True
    ):
        st.switch_page("pages/2_Risk_Dashboard.py")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""

<div class="status-card">

<div class="status-title">

System Status

</div>

<div class="status-item">🟢 Backend Connected</div>

<div class="status-item">🧠 Analytics Engine Ready</div>

<div class="status-item">📦 Shipment Data Loaded</div>

<div class="status-item">📊 Dashboard Live</div>

</div>

""", unsafe_allow_html=True)

# ==========================================================
# HERO
# ==========================================================

st.markdown("""

<div class="hero">

<h1> 📊 Shipment Risk Dashboard </h1>

<p>

Monitor shipment risks, delivery performance, warehouse operations,
shipping trends, delay analysis and logistics KPIs in real time.

All charts are powered using Hybrid AI analytics integrated with
PostgreSQL, ChromaDB and FastAPI.

</p>

</div>

""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

try:

    with st.spinner("Loading shipment analytics..."):

        response = requests.get(f"{API_URL}/risk-report")
        response.raise_for_status()

        report = response.json()

        summary = report["summary"]
        df = pd.DataFrame(report["all_shipments"])

except Exception as e:

    st.error(f"""
❌ Unable to connect to FastAPI

{e}
""")
    st.stop()

# ==========================================================
# FILTERS
# ==========================================================

st.markdown(
    "<div class='section-title'>🎯 Dashboard Filters</div>",
    unsafe_allow_html=True
)

filter_card = st.container(border=True)

with filter_card:

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        risk_filter = st.selectbox(
            "Risk Level",
            ["All", "HIGH", "MEDIUM", "LOW"],
            key="risk_filter"
        )

    with col2:

        delivery_options = ["All"]

        if "delivery_status" in df.columns:

            delivery_options += sorted(
                df["delivery_status"]
                .dropna()
                .unique()
                .tolist()
            )

        delivery_filter = st.selectbox(
            "Delivery Status",
            delivery_options,
            key="delivery_filter"
        )

    with col3:

        shipping_options = ["All"]

        if "shipping_mode" in df.columns:

            shipping_options += sorted(
                df["shipping_mode"]
                .dropna()
                .unique()
                .tolist()
            )

        shipping_filter = st.selectbox(
            "Shipping Mode",
            shipping_options,
            key="shipping_filter"
        )

    with col4:

        priority_options = ["All"]

        if "priority" in df.columns:

            priority_options += sorted(
                df["priority"]
                .dropna()
                .unique()
                .tolist()
            )

        priority_filter = st.selectbox(
            "Priority",
            priority_options,
            key="priority_filter"
        )

    search = st.text_input(
        "🔍 Search Shipment / Booking ID",
        placeholder="Example : SHP1025"
    )

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered_df = df.copy()

if (
    risk_filter != "All"
    and "risk_level" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["risk_level"] == risk_filter
    ]

if (
    delivery_filter != "All"
    and "delivery_status" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["delivery_status"] == delivery_filter
    ]

if (
    shipping_filter != "All"
    and "shipping_mode" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["shipping_mode"] == shipping_filter
    ]

if (
    priority_filter != "All"
    and "priority" in filtered_df.columns
):

    filtered_df = filtered_df[
        filtered_df["priority"] == priority_filter
    ]

if search:

    mask = pd.Series(False, index=filtered_df.index)

    if "shipment_id" in filtered_df.columns:

        mask |= filtered_df["shipment_id"].astype(str).str.contains(
            search,
            case=False,
            na=False
        )

    if "booking_id" in filtered_df.columns:

        mask |= filtered_df["booking_id"].astype(str).str.contains(
            search,
            case=False,
            na=False
        )

    filtered_df = filtered_df[mask]

# ==========================================================
# KPI VALUES
# ==========================================================

total_shipments = len(filtered_df)

high_risk = 0
medium_risk = 0
low_risk = 0

if "risk_level" in filtered_df.columns:

    high_risk = (
        filtered_df["risk_level"] == "HIGH"
    ).sum()

    medium_risk = (
        filtered_df["risk_level"] == "MEDIUM"
    ).sum()

    low_risk = (
        filtered_df["risk_level"] == "LOW"
    ).sum()

delayed_shipments = 0

if "delay_days" in filtered_df.columns:

    delayed_shipments = (
        filtered_df["delay_days"] > 0
    ).sum()

avg_delay = 0

if (
    "delay_days" in filtered_df.columns
    and len(filtered_df) > 0
):

    avg_delay = round(
        filtered_df["delay_days"].mean(),
        1
    )

# ==========================================================
# KPI DASHBOARD
# ==========================================================

st.markdown(
    "<div class='section-title'>📌 Dashboard Overview</div>",
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "📦 Total Shipments",
        total_shipments
    )

with k2:
    st.metric(
        "🚨 High Risk",
        high_risk
    )

with k3:
    st.metric(
        "⏳ Delayed",
        delayed_shipments
    )

with k4:
    st.metric(
        "📅 Avg Delay",
        f"{avg_delay} Days"
    )
    
    
# ==========================================================
# SHIPMENT RISK ANALYTICS
# ==========================================================

st.markdown(
    "<div class='section-title'>📈 Shipment Risk Analytics</div>",
    unsafe_allow_html=True
)

left, right = st.columns(2)

# ----------------------------------------------------------
# DONUT CHART
# ----------------------------------------------------------

with left:

    st.markdown("#### Risk Distribution")

    donut = px.pie(
        names=["High", "Medium", "Low"],
        values=[
            high_risk,
            medium_risk,
            low_risk
        ],
        hole=0.72,
        color=["High", "Medium", "Low"],
        color_discrete_map={
            "High": "#EF4444",
            "Medium": "#F59E0B",
            "Low": "#10B981"
        }
    )

    donut.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title="Risk Level"
    )

    st.plotly_chart(
        donut,
        use_container_width=True
    )

# ----------------------------------------------------------
# AVERAGE DELAY BY SHIPPING MODE
# ----------------------------------------------------------

with right:

    st.markdown("#### Average Delay by Shipping Mode")

    if (
        not filtered_df.empty
        and "shipping_mode" in filtered_df.columns
        and "delay_days" in filtered_df.columns
    ):

        delay_mode = (
            filtered_df
            .groupby("shipping_mode")["delay_days"]
            .mean()
            .reset_index()
        )

        delay_mode["delay_days"] = (
            delay_mode["delay_days"]
            .round(1)
        )

        fig = px.bar(
            delay_mode,
            x="shipping_mode",
            y="delay_days",
            text="delay_days",
            color="delay_days",
            color_continuous_scale="Tealgrn"
        )

        fig.update_traces(
            texttemplate="%{text} Days",
            textposition="outside"
        )

        fig.update_layout(
            height=430,
            xaxis_title="Shipping Mode",
            yaxis_title="Average Delay (Days)",
            coloraxis_showscale=False,
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==========================================================
# DELIVERY STATUS
# ==========================================================

if (
    not filtered_df.empty
    and "delivery_status" in filtered_df.columns
):

    st.markdown(
        "<div class='section-title'>📦 Delivery Status</div>",
        unsafe_allow_html=True
    )

    delivery = (
        filtered_df["delivery_status"]
        .value_counts()
        .reset_index()
    )

    delivery.columns = [
        "Status",
        "Count"
    ]

    fig = px.bar(
        delivery,
        x="Status",
        y="Count",
        text="Count",
        color="Status"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# SHIPPING MODE & PRIORITY
# ==========================================================

left, right = st.columns(2)

# ----------------------------------------------------------
# SHIPPING MODE
# ----------------------------------------------------------

with left:

    if (
        not filtered_df.empty
        and "shipping_mode" in filtered_df.columns
    ):

        st.markdown("#### 🚚 Shipping Mode")

        shipping = (
            filtered_df["shipping_mode"]
            .value_counts()
            .reset_index()
        )

        shipping.columns = [
            "Mode",
            "Count"
        ]

        fig = px.pie(
            shipping,
            names="Mode",
            values="Count",
            hole=0.60
        )

        fig.update_layout(
            height=400,
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ----------------------------------------------------------
# PRIORITY
# ----------------------------------------------------------

with right:

    if (
        not filtered_df.empty
        and "priority" in filtered_df.columns
    ):

        st.markdown("#### ⭐ Shipment Priority")

        priority = (
            filtered_df["priority"]
            .value_counts()
            .reset_index()
        )

        priority.columns = [
            "Priority",
            "Count"
        ]

        fig = px.pie(
            priority,
            names="Priority",
            values="Count",
            hole=0.60
        )

        fig.update_layout(
            height=400,
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==========================================================
# DELAY DISTRIBUTION
# ==========================================================

if (
    not filtered_df.empty
    and "delay_days" in filtered_df.columns
):

    st.markdown(
        "<div class='section-title'>⏳ Delay Distribution</div>",
        unsafe_allow_html=True
    )

    delay = px.histogram(
        filtered_df,
        x="delay_days",
        nbins=20,
        color_discrete_sequence=["#2563EB"]
    )

    delay.update_layout(
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Delay (Days)",
        yaxis_title="Shipments"
    )

    st.plotly_chart(
        delay,
        use_container_width=True
    )


# ==========================================================
# SHIPMENT DETAILS
# ==========================================================

st.markdown(
    "<div class='section-title'>📋 Shipment Details</div>",
    unsafe_allow_html=True
)

with st.container(border=True):

    if filtered_df.empty:

        st.warning("No shipments found for the selected filters.")

    else:

        display_columns = [

            "booking_id",
            "shipment_id",
            "shipment_type",
            "shipping_mode",
            "priority",
            "delivery_status",
            "delay_days",
            "risk_level",
            "recommended_action"

        ]

        available_columns = [

            col

            for col in display_columns

            if col in filtered_df.columns

        ]

        st.dataframe(

            filtered_df[available_columns],

            use_container_width=True,

            hide_index=True,

            height=450

        )

# ==========================================================
# TOP DELAYED SHIPMENTS
# ==========================================================

if (

    not filtered_df.empty

    and "delay_days" in filtered_df.columns

):

    st.markdown(
        "<div class='section-title'>🚨 Top Delayed Shipments</div>",
        unsafe_allow_html=True
    )

    delayed = (

        filtered_df

        .sort_values(
            "delay_days",
            ascending=False
        )

        .head(10)

    )

    with st.container(border=True):

        cols = [

            c

            for c in [

                "booking_id",
                "shipment_id",
                "delay_days",
                "risk_level",
                "delivery_status",
                "recommended_action"

            ]

            if c in delayed.columns

        ]

        st.dataframe(

            delayed[cols],

            hide_index=True,

            use_container_width=True,

            height=350

        )

# ==========================================================
# DOWNLOAD / REFRESH
# ==========================================================

left, right = st.columns([1,1])

with left:

    if not filtered_df.empty:

        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(

            "⬇ Download Report",

            csv,

            file_name="shipment_risk_report.csv",

            mime="text/csv",

            use_container_width=True

        )

with right:

    if st.button(

        "🔄 Refresh Dashboard",

        use_container_width=True

    ):

        st.rerun()

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("""

<br>
<br>

<div class="footer">
🚚 <b>NexusFreight AI Assistant</b>
<br>
Enterprise Logistics Platform
<br><br>
Powered by
<b>Hybrid AI</b>
• PostgreSQL • ChromaDB • LLM
</div>

""", unsafe_allow_html=True)

