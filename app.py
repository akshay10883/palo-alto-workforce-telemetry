"""
Palo Alto Networks Workforce Telemetry: 3D People Analytics & Organizational Network Science
Tailored for C-suite and HR Analytics | Master Enterprise Specification v2.0
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data_pipeline import clean_and_engineer_features

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Workforce Telemetry: 3D People Analytics & ONA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# High-End Design Blueprint CSS v2.0
# High-contrast Light Sidebar (280px) + Deep Space Navy Canvas (#060913)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Deep Space Navy Canvas */
    .stApp {
        background: radial-gradient(circle at 15% 15%, rgba(14, 165, 233, 0.08) 0%, rgba(6, 9, 19, 0.98) 55%),
                    radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.06) 0%, rgba(6, 9, 19, 0.98) 65%),
                    #060913 !important;
        color: #E2E8F0;
    }

    /* Sidebar: Fixed width ~280px, clean white background for high contrast */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
        min-width: 290px !important;
        max-width: 290px !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.15) !important;
    }
    [data-testid="stSidebar"] * {
        color: #1E293B !important;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #0F172A !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown span {
        color: #475569 !important;
        font-size: 0.86rem !important;
    }

    /* Tag-based chip filters */
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #EFF6FF !important;
        border: 1px solid #BFDBFE !important;
        color: #1D4ED8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #1D4ED8 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #F8FAFC !important;
        border-radius: 10px !important;
        border: 1px solid #CBD5E1 !important;
    }.glass

    /* File uploader in sidebar */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {
        background-color: #F8FAFC !important;
        border: 1px dashed #CBD5E1 !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }

    /* 3D Glassmorphism Metric Cards */
    -card {
       /* 3D Glassmorphism Metric Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.72) 0%, rgba(15, 23, 42, 0.88) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 
            0 12px 28px -4px rgba(0, 0, 0, 0.65),
            0 2px 8px rgba(0, 0, 0, 0.4),
            inset 0 1px 1px rgba(255, 255, 255, 0.12);
        transform: perspective(1000px) translateZ(0);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        margin-bottom: 16px;
    }

    .glass-card:hover {
        transform: perspective(1000px) translateY(-6px) translateZ(8px);
        box-shadow: 
            0 22px 36px -4px rgba(0, 0, 0, 0.8),
            0 0 20px rgba(56, 189, 248, 0.25),
            inset 0 1px 2px rgba(255, 255, 255, 0.2);
    }

    .card-purple::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #7C3AED, #A855F7); border-radius: 16px 16px 0 0; }
    .card-red::after    { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #DC2626, #F87171); border-radius: 16px 16px 0 0; }
    .card-orange::after { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #EA580C, #FB923C); border-radius: 16px 16px 0 0; }
    .card-amber::after  { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #D97706, #FCD34D); border-radius: 16px 16px 0 0; }
    .card-emerald::after{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #059669, #34D399); border-radius: 16px 16px 0 0; }
    .card-sky::after    { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #0284C7, #38BDF8); border-radius: 16px 16px 0 0; }

    .kpi-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94A3B8;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .kpi-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1;
        margin-bottom: 6px;
    }

    .kpi-sub {
        font-size: 0.76rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Animated pulse for critical KPIs */
    @keyframes kpi-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .kpi-alert { animation: kpi-pulse 2.2s ease-in-out infinite; }

    /* Horizontal Glass Tab Bar with Glowing Indicator */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(20px);
        padding: 6px 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.07);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.45);
        overflow-x: auto;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.84rem;
        padding: 9px 16px;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
        border: 1px solid transparent;
        position: relative;
        white-space: nowrap;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC;
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 255, 255, 0.06);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.3) !important;
    }

    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        bottom: 0; left: 15%; right: 15%; height: 2px;
        background: linear-gradient(90deg, #38BDF8, #818CF8);
        border-radius: 2px 2px 0 0;
        box-shadow: 0 0 12px #38BDF8;
    }

    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 8px;
        padding: 12px 16px;
        background: rgba(15, 23, 42, 0.5);
        border-radius: 12px;
        border-left: 3px solid #38BDF8;
        backdrop-filter: blur(8px);
    }

    /* Alert banner */
    .risk-alert {
        background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05));
        border: 1px solid rgba(239,68,68,0.4);
        border-radius: 14px;
        padding: 14px 20px;
        margin-top: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        backdrop-filter: blur(8px);
    }

    /* Metric delta styling */
    [data-testid="stMetricDelta"] { font-weight: 700 !important; }

    /* Dataframe dark theme */
    [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
    iframe { border-radius: 10px; }

    /* Progress bars */
    .stProgress > div > div { background: linear-gradient(90deg, #3B82F6, #8B5CF6) !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Data Engine
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_and_prepare_dataset():
    csv_candidates = ["palo_alto_attrition.csv", "palo_alto_attrition_cleaned.csv"]
    target_csv = None
    for c in csv_candidates:
        if os.path.exists(c):
            target_csv = c
            break

    if target_csv is not None:
        raw_data = pd.read_csv(target_csv)
    else:
        from generate_data import generate_attrition_dataset
        raw_data = generate_attrition_dataset(1470, seed=42)
        raw_data.to_csv("palo_alto_attrition.csv", index=False)

    cleaned_df, telemetry = clean_and_engineer_features(raw_data)
    return cleaned_df, telemetry

with st.spinner("🔄 Loading HR Telemetry engine..."):
    cleaned_df, telemetry = load_and_prepare_dataset()

# ---------------------------------------------------------
# Sidebar: High-Contrast Clean Light Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Palo_Alto_Networks_logo.svg/320px-Palo_Alto_Networks_logo.svg.png",
        width=200
    )
    st.markdown("### Workforce Telemetry")
    st.markdown("<p style='margin-top:-8px;'>3D People Analytics & Organizational Network Science</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("##### 📁 Upload HR Telemetry")
    st.caption("Max file size: 200MB (CSV format)")
    uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    if uploaded is not None:
        try:
            custom_raw = pd.read_csv(uploaded)
            cleaned_df, telemetry = clean_and_engineer_features(custom_raw)
            st.success(f"✅ Loaded {len(cleaned_df):,} records!")
        except Exception as e:
            st.error(f"Upload error: {e}")

    st.markdown("---")
    st.markdown("##### 🎛️ Dynamic Slicers")

    all_depts = sorted(list(cleaned_df["Department"].dropna().unique()))
    sel_depts = st.multiselect("Department", options=all_depts, default=all_depts,
                                help="Filter by operational division")

    valid_roles = sorted(list(
        cleaned_df[cleaned_df["Department"].isin(sel_depts)]["JobRole"].dropna().unique()
    ))
    sel_roles = st.multiselect("Job Roles", options=valid_roles, default=valid_roles,
                                help="Filter by job designation")

    min_t = int(cleaned_df["YearsAtCompany"].min())
    max_t = int(cleaned_df["YearsAtCompany"].max())
    sel_tenure = st.slider("Tenure Horizon (Years)", min_t, max_t, (min_t, max_t))

    sel_ot = st.selectbox(
        "Overtime Status",
        options=["All Staff", "Overtime Required (Yes)", "Standard Hours (No)"],
        index=0
    )

    travel_opts = ["All Travel Tiers"] + sorted(list(cleaned_df["BusinessTravel"].unique()))
    sel_travel = st.selectbox("Business Travel Frequency", options=travel_opts, index=0)

    st.markdown("---")
    st.markdown(
        "<div style='background:#F1F5F9; padding:12px; border-radius:10px; "
        "border-left:3px solid #0284C7; font-size:0.78rem; color:#334155;'>"
        "<b>Benchmark Target:</b> Palo Alto Networks target cyber retention is 85.8% "
        "(max 14.2% turnover).</div>",
        unsafe_allow_html=True
    )
    st.markdown("")
    st.markdown(
        "<div style='background:#FEF2F2; padding:10px 12px; border-radius:10px; "
        "border-left:3px solid #EF4444; font-size:0.76rem; color:#7F1D1D;'>"
        "<b>⚠ Industry Avg:</b> Tech sector voluntary attrition runs 18-22% annually. "
        "Cybersecurity roles carry 1.4× higher exit velocity.</div>",
        unsafe_allow_html=True
    )

# ── Apply all active filters ─────────────────────────────
filtered = cleaned_df[
    (cleaned_df["Department"].isin(sel_depts)) &
    (cleaned_df["JobRole"].isin(sel_roles)) &
    (cleaned_df["YearsAtCompany"].between(sel_tenure[0], sel_tenure[1]))
]

if sel_ot == "Overtime Required (Yes)":
    filtered = filtered[filtered["OverTime"] == "Yes"]
elif sel_ot == "Standard Hours (No)":
    filtered = filtered[filtered["OverTime"] == "No"]

if sel_travel != "All Travel Tiers":
    filtered = filtered[filtered["BusinessTravel"] == sel_travel]

if len(filtered) == 0:
    st.warning("⚠️ No employee records match the active filter criteria. Please broaden your selection.")
    st.stop()


# ---------------------------------------------------------
# Derived KPI Metrics
# ---------------------------------------------------------
total_headcount  = len(filtered)
total_exited     = int(filtered["Attrition_Numeric"].sum())
total_retained   = total_headcount - total_exited
turnover_pct     = (total_exited / total_headcount) * 100 if total_headcount > 0 else 0

ot_df        = filtered[filtered["OverTime"] == "Yes"]
ot_turnover  = (ot_df["Attrition_Numeric"].mean() * 100) if len(ot_df) > 0 else 0

early_df      = filtered[filtered["YearsAtCompany"] <= 2]
early_risk_pct = (early_df["Attrition_Numeric"].mean() * 100) if len(early_df) > 0 else 0

flight_risk_count = int((filtered["Risk_Tier"] == "High Flight Risk (Urgent Action)").sum())
avg_salary        = filtered["MonthlyIncome"].mean()
capital_loss_val  = total_exited * avg_salary * 6


# ---------------------------------------------------------
# Header Section
# ---------------------------------------------------------
st.markdown("""
<div style="display: flex; align-items: center; gap: 14px; margin-bottom: 4px;">
    <span style="font-size: 2.4rem;">🛡️</span>
    <div>
        <h1 style="margin: 0; font-size: 2.0rem; font-weight: 800; letter-spacing: -0.03em; color: #F8FAFC;
                   background: linear-gradient(135deg, #F8FAFC 0%, #94A3B8 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Palo Alto Networks: 3D Workforce &amp; Network Analytics
        </h1>
        <p style="margin: 3px 0 0 0; color: #64748B; font-size: 0.92rem; font-weight: 500;">
            Enterprise Intelligence · 3D Organizational Network Science · Talent Hotspot Telemetry
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# KPI Metric Cards (Grid of 5 Glassmorphism Cards)
# ---------------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="glass-card card-purple">
        <div class="kpi-title">
            <span>MONITORED HEADCOUNT</span>
            <span style="color: #A855F7; font-size: 1.1rem;">🟣</span>
        </div>
        <div class="kpi-num" style="color: #F8FAFC;">{total_headcount:,}</div>
        <div class="kpi-sub" style="color: #C084FC;">
            Retained: {total_retained:,} &nbsp;|&nbsp; Exits: {total_exited:,}
        </div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    alert_cls = "kpi-alert" if turnover_pct > 14.2 else ""
    st.markdown(f"""
    <div class="glass-card card-red">
        <div class="kpi-title">
            <span>TURNOVER RATE</span>
            <span style="color: #EF4444; font-size: 1.1rem;">⚡</span>
        </div>
        <div class="kpi-num {alert_cls}" style="color: #F87171;">{turnover_pct:.1f}%</div>
        <div class="kpi-sub" style="color: #FCA5A5;">
            ▲ {max(0, turnover_pct - 14.2):.1f}% above benchmark
        </div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="glass-card card-orange">
        <div class="kpi-title">
            <span>EARLY-TENURE RISK (≤2Y)</span>
            <span style="color: #F97316; font-size: 1.1rem;">⏳</span>
        </div>
        <div class="kpi-num" style="color: #FB923C;">{early_risk_pct:.1f}%</div>
        <div class="kpi-sub" style="color: #FDBA74;">
            Onboarding Vulnerability
        </div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="glass-card card-amber">
        <div class="kpi-title">
            <span>OVERTIME CHURN RATE</span>
            <span style="color: #F59E0B; font-size: 1.1rem;">🔥</span>
        </div>
        <div class="kpi-num" style="color: #FBBF24;">{ot_turnover:.1f}%</div>
        <div class="kpi-sub" style="color: #FCD34D;">
            Burnout Multiplier Spread
        </div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="glass-card card-emerald">
        <div class="kpi-title">
            <span>CAPITAL LOSS IMPACT</span>
            <span style="color: #10B981; font-size: 1.1rem;">🔋</span>
        </div>
        <div class="kpi-num" style="color: #34D399;">${capital_loss_val / 1_000_000:.2f}M</div>
        <div class="kpi-sub" style="color: #6EE7B7;">
            {flight_risk_count} at immediate flight risk
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Risk Alert Banner (renders when attrition exceeds benchmark)
# ---------------------------------------------------------
if flight_risk_count > 0 and turnover_pct > 20:
    st.markdown(f"""
    <div class="risk-alert">
        <span style="font-size:1.5rem;">🚨</span>
        <div>
            <span style="font-weight:800;font-size:0.88rem;color:#F87171;
                         text-transform:uppercase;letter-spacing:0.06em;">
                Critical Workforce Risk Alert
            </span>
            <p style="margin:3px 0 0 0;font-size:0.82rem;color:#CBD5E1;">
                <b>{flight_risk_count}</b> high-priority flight-risk employees detected in the active filtered cohort.
                Organizational attrition of <b>{turnover_pct:.1f}%</b> is
                <b>{turnover_pct - 14.2:.1f}%</b> above the 14.2% industry benchmark.
                Immediate HR intervention recommended.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Navigation Tabs (Glass Styling with Glowing Indicator)
# ---------------------------------------------------------
tab_ona, tab_overview, tab_hotspots, tab_demographics, tab_tenure_3d, tab_burnout, tab_pipeline, tab_sim = st.tabs([
    "🌌 3D Organizational Network (ONA)",
    "📊 Executive Attrition Overview",
    "🔥 Department & Role Hotspots",
    "👥 Demographic Explorer",
    "⏳ 3D Tenure & Career Trajectories",
    "⚡ Burnout & Workload Matrix",
    "🧪 Data Pipeline & Features",
    "🎯 Policy Risk Simulator"
])


# =========================================================
# TAB 1: 3D ORGANIZATIONAL NETWORK ANALYSIS (ONA)
# =========================================================
with tab_ona:
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.5rem;">🪐</span>
        <h3 style="margin:0;font-size:1.35rem;font-weight:800;color:#F8FAFC;">
            3D Organizational Network Analysis (ONA)
        </h3>
    </div>
    <p style="color:#94A3B8;font-size:0.92rem;margin:10px 0 18px 0;">
        Interactive 3D graph mapping systemic connectivity between organizational divisions,
        job designations, and talent attrition risk nodes.
    </p>
    """, unsafe_allow_html=True)

    col_desc1, col_desc2, col_desc3 = st.columns(3)
    with col_desc1:
        st.markdown("""
        <div class="glass-card card-sky" style="padding:14px 18px;min-height:80px;">
            <div class="kpi-title"><span>X-AXIS DIMENSION</span></div>
            <div style="font-weight:700;color:#38BDF8;font-size:0.95rem;">Departmental Divisions</div>
            <div style="font-size:0.78rem;color:#94A3B8;margin-top:4px;">R&D · Sales · Human Resources</div>
        </div>
        """, unsafe_allow_html=True)
    with col_desc2:
        st.markdown("""
        <div class="glass-card card-purple" style="padding:14px 18px;min-height:80px;">
            <div class="kpi-title"><span>Y-AXIS DIMENSION</span></div>
            <div style="font-weight:700;color:#A855F7;font-size:0.95rem;">Technical Seniority</div>
            <div style="font-size:0.78rem;color:#94A3B8;margin-top:4px;">Level 1 IC → Level 5 Executive</div>
        </div>
        """, unsafe_allow_html=True)
    with col_desc3:
        st.markdown("""
        <div class="glass-card card-red" style="padding:14px 18px;min-height:80px;">
            <div class="kpi-title"><span>Z-AXIS DIMENSION</span></div>
            <div style="font-weight:700;color:#F87171;font-size:0.95rem;">Flight Risk Velocity</div>
            <div style="font-size:0.78rem;color:#94A3B8;margin-top:4px;">Composite risk score 0–100%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    view_style = st.radio("Display Mode", ["🪐 3D Spatial Universe", "🗺️ 2D Relational Flow Map"], horizontal=True)

    if view_style == "🪐 3D Spatial Universe":
        dept_mapping = {"Research & Development": 1.0, "Sales": 2.5, "Human Resources": 4.0}

        role_3d = filtered.groupby(["Department", "JobRole"]).agg(
            Headcount=("Attrition_Numeric", "count"),
            Attrition_Rate=("Attrition_Numeric", lambda x: (x.sum() / len(x)) * 100),
            Avg_Job_Level=("JobLevel", "mean"),
            Avg_Risk_Score=("Risk_Score", "mean"),
            Avg_Salary=("MonthlyIncome", "mean"),
            Overtime_Pct=("OverTime", lambda x: (x == "Yes").mean() * 100)
        ).reset_index()

        rng = np.random.default_rng(seed=7)
        role_3d["X"] = role_3d["Department"].map(dept_mapping) + rng.uniform(-0.12, 0.12, len(role_3d))
        role_3d["Y"] = role_3d["Avg_Job_Level"]
        role_3d["Z"] = role_3d["Avg_Risk_Score"]

        node_hover = [
            f"<b>Role:</b> {r['JobRole']}<br>"
            f"<b>Division:</b> {r['Department']}<br>"
            f"<b>Staff Count:</b> {r['Headcount']}<br>"
            f"<b>Attrition Rate:</b> {r['Attrition_Rate']:.1f}%<br>"
            f"<b>Flight Risk Score:</b> {r['Avg_Risk_Score']:.1f}/100<br>"
            f"<b>Overtime Exposure:</b> {r['Overtime_Pct']:.1f}%<br>"
            f"<b>Average Salary:</b> ${r['Avg_Salary']:,.0f}"
            for _, r in role_3d.iterrows()
        ]

        # Build department hierarchy edges
        edge_x, edge_y, edge_z = [], [], []
        for d in dept_mapping.keys():
            d_sub = role_3d[role_3d["Department"] == d].sort_values("Avg_Job_Level")
            if len(d_sub) > 1:
                coords = d_sub[["X", "Y", "Z"]].values
                for idx in range(len(coords) - 1):
                    edge_x.extend([coords[idx][0], coords[idx + 1][0], None])
                    edge_y.extend([coords[idx][1], coords[idx + 1][1], None])
                    edge_z.extend([coords[idx][2], coords[idx + 1][2], None])

        fig_3d = go.Figure()
        fig_3d.add_trace(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='rgba(56, 189, 248, 0.35)', width=3),
            hoverinfo='none', showlegend=False
        ))
        fig_3d.add_trace(go.Scatter3d(
            x=role_3d["X"], y=role_3d["Y"], z=role_3d["Z"],
            mode='markers+text',
            text=role_3d["JobRole"],
            textposition="top center",
            textfont=dict(size=9.5, color="#E2E8F0"),
            marker=dict(
                size=12 + np.sqrt(role_3d["Headcount"]) * 2.8,
                color=role_3d["Attrition_Rate"],
                colorscale="Turbo",
                colorbar=dict(
                    title=dict(text="Attrition Rate %", font=dict(color="#F8FAFC")),
                    tickfont=dict(color="#F8FAFC"),
                    len=0.75
                ),
                opacity=0.92,
                line=dict(color='#FFFFFF', width=1.5)
            ),
            hovertext=node_hover, hoverinfo='text', name="Job Role"
        ))
        fig_3d.update_layout(
            scene=dict(
                xaxis=dict(
                    title="Departmental Divisions",
                    tickvals=[1.0, 2.5, 4.0],
                    ticktext=["R&D Engineering", "Sales & Field", "Human Resources"],
                    backgroundcolor="rgba(11, 15, 25, 0.6)",
                    gridcolor="rgba(148, 163, 184, 0.15)",
                    showbackground=True
                ),
                yaxis=dict(
                    title="Technical Seniority (Level 1–5)",
                    backgroundcolor="rgba(11, 15, 25, 0.6)",
                    gridcolor="rgba(148, 163, 184, 0.15)",
                    showbackground=True
                ),
                zaxis=dict(
                    title="Flight Risk Score (0–100)",
                    backgroundcolor="rgba(11, 15, 25, 0.6)",
                    gridcolor="rgba(148, 163, 184, 0.15)",
                    showbackground=True
                ),
                camera=dict(eye=dict(x=1.75, y=-1.75, z=1.2))
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"),
            height=660,
            margin=dict(l=0, r=0, t=10, b=10)
        )
        st.plotly_chart(fig_3d, width='stretch')

    else:
        # 2D Relational Flow Map
        dept_nodes = sorted(list(filtered["Department"].unique()))
        role_nodes = sorted(list(filtered["JobRole"].unique()))
        risk_nodes = ["Overtime Burnout", "Frequent Travel Stress", "Tenure Cliff (≤2y)",
                      "Promotion Stagnation", "Low Comp Band"]

        nodes_info = {}
        y_depts = np.linspace(1, 10, len(dept_nodes))
        for i, d in enumerate(dept_nodes):
            d_sub = filtered[filtered["Department"] == d]
            attr_d = (d_sub["Attrition_Numeric"].mean() * 100) if len(d_sub) > 0 else 0
            nodes_info[d] = {"x": 1.0, "y": y_depts[i], "type": "Department",
                              "size": 32, "attrition": attr_d, "headcount": len(d_sub), "color": "#38BDF8"}

        y_roles = np.linspace(0.5, 10.5, len(role_nodes))
        for i, r in enumerate(role_nodes):
            r_sub = filtered[filtered["JobRole"] == r]
            attr_r = (r_sub["Attrition_Numeric"].mean() * 100) if len(r_sub) > 0 else 0
            r_color = "#EF4444" if attr_r >= 22.0 else ("#F59E0B" if attr_r >= 14.0 else "#10B981")
            nodes_info[r] = {"x": 2.5, "y": y_roles[i], "type": "Job Designation",
                              "size": 18 + int(len(r_sub) / 25), "attrition": attr_r,
                              "headcount": len(r_sub), "color": r_color}

        y_risks = np.linspace(1.5, 9.5, len(risk_nodes))
        for i, rk in enumerate(risk_nodes):
            nodes_info[rk] = {"x": 4.0, "y": y_risks[i], "type": "Risk Stressor",
                               "size": 26, "attrition": 32.5, "headcount": 0, "color": "#A855F7"}

        edge_x, edge_y = [], []
        for d in dept_nodes:
            for r in role_nodes:
                sub = filtered[(filtered["Department"] == d) & (filtered["JobRole"] == r)]
                if len(sub) > 0:
                    edge_x.extend([nodes_info[d]["x"], nodes_info[r]["x"], None])
                    edge_y.extend([nodes_info[d]["y"], nodes_info[r]["y"], None])

        for r in role_nodes:
            r_sub = filtered[filtered["JobRole"] == r]
            if len(r_sub) > 0:
                if (r_sub["OverTime"] == "Yes").mean() >= 0.25:
                    edge_x.extend([nodes_info[r]["x"], nodes_info["Overtime Burnout"]["x"], None])
                    edge_y.extend([nodes_info[r]["y"], nodes_info["Overtime Burnout"]["y"], None])
                if (r_sub["BusinessTravel"] == "Travel_Frequently").mean() >= 0.20:
                    edge_x.extend([nodes_info[r]["x"], nodes_info["Frequent Travel Stress"]["x"], None])
                    edge_y.extend([nodes_info[r]["y"], nodes_info["Frequent Travel Stress"]["y"], None])
                if (r_sub["YearsAtCompany"] <= 2).mean() >= 0.35:
                    edge_x.extend([nodes_info[r]["x"], nodes_info["Tenure Cliff (≤2y)"]["x"], None])
                    edge_y.extend([nodes_info[r]["y"], nodes_info["Tenure Cliff (≤2y)"]["y"], None])
                if (r_sub["Promotion_Stagnant"] == "Stagnant (≥3 Yrs)").mean() >= 0.20:
                    edge_x.extend([nodes_info[r]["x"], nodes_info["Promotion Stagnation"]["x"], None])
                    edge_y.extend([nodes_info[r]["y"], nodes_info["Promotion Stagnation"]["y"], None])
                if r_sub["MonthlyIncome"].mean() < 4000:
                    edge_x.extend([nodes_info[r]["x"], nodes_info["Low Comp Band"]["x"], None])
                    edge_y.extend([nodes_info[r]["y"], nodes_info["Low Comp Band"]["y"], None])

        fig_2d = go.Figure()
        fig_2d.add_trace(go.Scatter(
            x=edge_x, y=edge_y, mode="lines",
            line=dict(color="rgba(148, 163, 184, 0.25)", width=1.5),
            hoverinfo="none", showlegend=False
        ))
        node_x = [v["x"] for v in nodes_info.values()]
        node_y = [v["y"] for v in nodes_info.values()]
        node_sizes = [v["size"] for v in nodes_info.values()]
        node_colors = [v["color"] for v in nodes_info.values()]
        node_text = [
            f"<b>{k}</b><br>Type: {v['type']}<br>Staff: {v['headcount']}<br>Attrition Rate: {v['attrition']:.1f}%"
            for k, v in nodes_info.items()
        ]
        fig_2d.add_trace(go.Scatter(
            x=node_x, y=node_y, mode="markers+text",
            text=[k if nodes_info[k]["type"] != "Job Designation" else "" for k in nodes_info.keys()],
            textposition="top center",
            marker=dict(size=node_sizes, color=node_colors, line=dict(color="#0F172A", width=2)),
            hovertext=node_text, hoverinfo="text", showlegend=False
        ))
        fig_2d.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=580, font=dict(color="#F8FAFC")
        )
        st.plotly_chart(fig_2d, width='stretch')

    st.markdown("---")
    st.markdown("#### 🏆 Structural Hubs & Stress Centrality Ranking")

    net_data = []
    for r in filtered["JobRole"].unique():
        sub = filtered[filtered["JobRole"] == r]
        att_r  = (sub["Attrition_Numeric"].mean() * 100)
        ot_p   = (sub["OverTime"] == "Yes").mean() * 100
        early_p= (sub["YearsAtCompany"] <= 2).mean() * 100
        stag_p = (sub["Promotion_Stagnant"] == "Stagnant (≥3 Yrs)").mean() * 100
        active_stresses = sum([ot_p >= 25, early_p >= 35, stag_p >= 20, sub["MonthlyIncome"].mean() < 4000])
        badge = "🔴 CRITICAL RISK" if att_r >= 22.0 else ("🟡 ELEVATED RISK" if att_r >= 14.0 else "🟢 STABLE")
        net_data.append({
            "Job Designation": r,
            "Division": sub["Department"].iloc[0],
            "Staff Count": len(sub),
            "Turnover %": f"{att_r:.1f}%",
            "Overtime %": f"{ot_p:.1f}%",
            "Onboarding Churn %": f"{early_p:.1f}%",
            "Stagnation %": f"{stag_p:.1f}%",
            "Stress Hubs": f"{active_stresses}/4",
            "Risk Tier": badge
        })
    df_net_tab = pd.DataFrame(net_data).sort_values(by="Turnover %", ascending=False)
    st.dataframe(df_net_tab, width='stretch')


# =========================================================
# TAB 2: EXECUTIVE ATTRITION OVERVIEW
# =========================================================
with tab_overview:
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.5rem;">📊</span>
        <h3 style="margin:0;font-size:1.35rem;font-weight:800;color:#F8FAFC;">Executive Workforce Intelligence Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c_pie, c_dept = st.columns([1, 1])

    with c_pie:
        st.markdown("#### Headcount Retention Proportions")
        pie_df = filtered["Attrition_Label"].value_counts().reset_index()
        pie_df.columns = ["Status", "Count"]
        fig_donut = px.pie(
            pie_df, names="Status", values="Count", hole=0.62,
            color="Status", color_discrete_map={"Yes": "#EF4444", "No": "#0284C7"}
        )
        fig_donut.update_traces(
            textposition='inside', textinfo='percent+label',
            marker=dict(line=dict(color='#0F172A', width=2.5))
        )
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"),
            margin=dict(t=20, b=20, l=20, r=20),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"))
        )
        st.plotly_chart(fig_donut, width='stretch')

    with c_dept:
        st.markdown("#### Departmental Turnover Comparison")
        dept_grp = filtered.groupby("Department").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        dept_grp["Rate"] = (dept_grp["Exits"] / dept_grp["Total"]) * 100
        dept_grp["Label"] = dept_grp.apply(lambda r: f"{r['Rate']:.1f}%  ({r['Exits']}/{r['Total']})", axis=1)
        fig_dept = px.bar(
            dept_grp, x="Rate", y="Department", orientation="h",
            color="Rate", color_continuous_scale="Reds", text="Label"
        )
        fig_dept.add_vline(x=14.2, line_dash="dash", line_color="#38BDF8",
                           annotation_text="Benchmark (14.2%)", annotation_font_color="#38BDF8")
        fig_dept.update_traces(textposition="inside", textfont_size=12)
        fig_dept.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), coloraxis_showscale=False
        )
        st.plotly_chart(fig_dept, width='stretch')

    st.markdown("---")
    ov1, ov2 = st.columns(2)

    with ov1:
        st.markdown("#### Job Role Attrition Ranking (Top 10)")
        role_grp = filtered.groupby("JobRole").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        role_grp["Rate"] = (role_grp["Exits"] / role_grp["Total"]) * 100
        role_grp = role_grp.sort_values("Rate", ascending=False).head(10)
        fig_role = px.bar(
            role_grp, x="Rate", y="JobRole", orientation="h",
            color="Rate", color_continuous_scale="Turbo",
            text=[f"{r:.1f}%" for r in role_grp["Rate"]]
        )
        fig_role.add_vline(x=14.2, line_dash="dot", line_color="#38BDF8",
                           annotation_text="Benchmark")
        fig_role.update_traces(textposition="inside")
        fig_role.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), coloraxis_showscale=False, height=420
        )
        st.plotly_chart(fig_role, width='stretch')

    with ov2:
        st.markdown("#### Monthly Attrition Trend (Tenure Cohorts)")
        month_grp = filtered.groupby("Tenure_Horizon", observed=False).agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        month_grp["Rate"] = (month_grp["Exits"] / month_grp["Total"]) * 100
        fig_trend = px.area(
            month_grp, x="Tenure_Horizon", y="Rate",
            labels={"Rate": "Turnover %", "Tenure_Horizon": "Tenure Cohort"},
            color_discrete_sequence=["#EF4444"]
        )
        fig_trend.update_traces(
            fill='tozeroy',
            fillcolor='rgba(239,68,68,0.18)',
            line=dict(color="#EF4444", width=2.5)
        )
        fig_trend.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8",
                            annotation_text="14.2% benchmark")
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), height=420
        )
        st.plotly_chart(fig_trend, width='stretch')

    # Summary metrics row
    st.markdown("---")
    st.markdown("#### 📌 At-a-Glance Summary Metrics")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Overall Attrition", f"{turnover_pct:.1f}%", f"+{turnover_pct-14.2:.1f}% vs benchmark",
                  delta_color="inverse")
    with m2:
        st.metric("Total Exits", f"{total_exited:,}", f"of {total_headcount:,} employees")
    with m3:
        avg_inc_exit = filtered[filtered["Attrition_Label"]=="Yes"]["MonthlyIncome"].mean()
        avg_inc_ret  = filtered[filtered["Attrition_Label"]=="No"]["MonthlyIncome"].mean()
        st.metric("Avg Exit Salary", f"${avg_inc_exit:,.0f}", f"Retained avg: ${avg_inc_ret:,.0f}")
    with m4:
        st.metric("Capital Loss Estimate", f"${capital_loss_val/1e6:.2f}M", "6× monthly replacement cost")


# =========================================================
# TAB 3: DEPARTMENT & ROLE HOTSPOTS
# =========================================================
with tab_hotspots:
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.5rem;">🔥</span>
        <h3 style="margin:0;font-size:1.35rem;font-weight:800;color:#F8FAFC;">
            Department × Job Role Risk Concentration Matrix
        </h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    pivot_heat = filtered.pivot_table(
        index="JobRole", columns="Department", values="Attrition_Numeric",
        aggfunc=lambda x: (x.sum() / len(x)) * 100 if len(x) > 0 else 0
    ).fillna(0)

    fig_h = px.imshow(
        pivot_heat,
        labels=dict(x="Department", y="Role", color="Turnover %"),
        color_continuous_scale="Turbo", text_auto=".1f", aspect="auto"
    )
    fig_h.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"), height=500)
    st.plotly_chart(fig_h, width='stretch')

    st.markdown("---")
    hh1, hh2 = st.columns(2)

    with hh1:
        st.markdown("#### Job Role Size vs Attrition Rate Bubble Chart")
        role_bubble = filtered.groupby("JobRole").agg(
            Headcount=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum"),
            Avg_Income=("MonthlyIncome", "mean")
        ).reset_index()
        role_bubble["Rate"] = (role_bubble["Exits"] / role_bubble["Headcount"]) * 100
        fig_bubble = px.scatter(
            role_bubble, x="Avg_Income", y="Rate", size="Headcount",
            color="Rate", color_continuous_scale="Reds",
            hover_data=["JobRole", "Headcount", "Exits"],
            labels={"Avg_Income": "Avg Monthly Income ($)", "Rate": "Attrition Rate (%)"},
            size_max=50
        )
        fig_bubble.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8",
                             annotation_text="14.2% Benchmark")
        fig_bubble.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), coloraxis_showscale=False
        )
        st.plotly_chart(fig_bubble, width='stretch')

    with hh2:
        st.markdown("#### Job Level Risk Gradient")
        jl_grp = filtered.groupby("JobLevel").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum"),
            Avg_Income=("MonthlyIncome", "mean")
        ).reset_index()
        jl_grp["Rate"] = (jl_grp["Exits"] / jl_grp["Total"]) * 100
        jl_grp["Level_Label"] = jl_grp["JobLevel"].map({
            1: "L1 — Entry", 2: "L2 — Junior", 3: "L3 — Mid",
            4: "L4 — Senior", 5: "L5 — Director"
        })
        fig_jl = go.Figure()
        fig_jl.add_trace(go.Bar(
            x=jl_grp["Level_Label"], y=jl_grp["Rate"],
            marker=dict(
                color=jl_grp["Rate"],
                colorscale="Reds",
                line=dict(color="#0F172A", width=1.5)
            ),
            text=[f"{r:.1f}%" for r in jl_grp["Rate"]],
            textposition="outside", textfont=dict(color="#F8FAFC")
        ))
        fig_jl.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8",
                         annotation_text="Benchmark")
        fig_jl.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), showlegend=False,
            yaxis_title="Attrition Rate (%)"
        )
        st.plotly_chart(fig_jl, width='stretch')


# =========================================================
# TAB 4: DEMOGRAPHIC EXPLORER
# =========================================================
with tab_demographics:
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.5rem;">👥</span>
        <h3 style="margin:0;font-size:1.35rem;font-weight:800;color:#F8FAFC;">
            Demographic Attrition Explorer &amp; Generational Churn Drivers
        </h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        st.markdown("#### Age Cohort Attrition Rates")
        age_grp = filtered.groupby("Age_Group", observed=False).agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        age_grp["Rate"] = (age_grp["Exits"] / age_grp["Total"]) * 100
        fig_a = px.bar(
            age_grp, x="Age_Group", y="Rate", color="Rate",
            color_continuous_scale="Sunsetdark",
            text=[f"{r:.1f}%" for r in age_grp["Rate"]]
        )
        fig_a.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8",
                        annotation_text="Benchmark")
        fig_a.update_traces(textposition="outside", textfont_size=12)
        fig_a.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), coloraxis_showscale=False,
            yaxis_title="Attrition Rate (%)"
        )
        st.plotly_chart(fig_a, width='stretch')

    with d2:
        st.markdown("#### Marital Status × Gender Cross-Tab")
        mg_grp = filtered.groupby(["MaritalStatus", "Gender"]).agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        mg_grp["Rate"] = (mg_grp["Exits"] / mg_grp["Total"]) * 100
        fig_mg = px.bar(
            mg_grp, x="MaritalStatus", y="Rate", color="Gender", barmode="group",
            color_discrete_map={"Male": "#38BDF8", "Female": "#F472B6"},
            text=[f"{r:.1f}%" for r in mg_grp["Rate"]]
        )
        fig_mg.add_hline(y=14.2, line_dash="dash", line_color="#94A3B8")
        fig_mg.update_traces(textposition="outside")
        fig_mg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), yaxis_title="Attrition Rate (%)",
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig_mg, width='stretch')

    st.markdown("---")
    d3, d4 = st.columns(2)

    with d3:
        st.markdown("#### Education Field Attrition Rates")
        ef_grp = filtered.groupby("EducationField").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        ef_grp["Rate"] = (ef_grp["Exits"] / ef_grp["Total"]) * 100
        ef_grp = ef_grp.sort_values("Rate", ascending=True)
        fig_ef = px.bar(
            ef_grp, x="Rate", y="EducationField", orientation="h",
            color="Rate", color_continuous_scale="Magma",
            text=[f"{r:.1f}%" for r in ef_grp["Rate"]]
        )
        fig_ef.add_vline(x=14.2, line_dash="dash", line_color="#38BDF8",
                         annotation_text="Benchmark")
        fig_ef.update_traces(textposition="inside")
        fig_ef.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), coloraxis_showscale=False
        )
        st.plotly_chart(ef_grp["Rate"].max(), width='stretch') if False else st.plotly_chart(fig_ef, width='stretch')

    with d4:
        st.markdown("#### Education Level × Attrition Heatmap")
        el_map = {1: "Below College", 2: "College", 3: "Bachelor", 4: "Master", 5: "Doctor"}
        _eldf = filtered.copy()
        _eldf["Edu_Label"] = _eldf["Education"].map(el_map)
        el_grp = _eldf.groupby(["Edu_Label", "Department"]).agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        el_grp["Rate"] = (el_grp["Exits"] / el_grp["Total"]) * 100
        el_pivot = el_grp.pivot_table(index="Edu_Label", columns="Department",
                                       values="Rate", aggfunc="mean").fillna(0)
        fig_el = px.imshow(
            el_pivot,
            labels=dict(x="Department", y="Education Level", color="Attrition %"),
            color_continuous_scale="Reds", text_auto=".1f", aspect="auto"
        )
        fig_el.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"))
        st.plotly_chart(fig_el, width='stretch')

    st.markdown("---")
    d5, d6 = st.columns(2)

    with d5:
        st.markdown("#### Job Satisfaction vs Attrition")
        js_grp = filtered.groupby("JobSatisfaction").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        js_grp["Rate"] = (js_grp["Exits"] / js_grp["Total"]) * 100
        js_grp["Satisfaction"] = js_grp["JobSatisfaction"].map(
            {1: "1-Low", 2: "2-Fair", 3: "3-Good", 4: "4-High"}
        )
        fig_js = px.line(js_grp, x="Satisfaction", y="Rate", markers=True,
                         labels={"Rate": "Attrition %"})
        fig_js.update_traces(line=dict(color="#EF4444", width=3),
                             marker=dict(size=11, color="#F87171"))
        fig_js.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8")
        fig_js.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC")
        )
        st.plotly_chart(fig_js, width='stretch')

    with d6:
        st.markdown("#### Environment Satisfaction vs Attrition")
        es_grp = filtered.groupby("EnvironmentSatisfaction").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        es_grp["Rate"] = (es_grp["Exits"] / es_grp["Total"]) * 100
        es_grp["Satisfaction"] = es_grp["EnvironmentSatisfaction"].map(
            {1: "1-Low", 2: "2-Fair", 3: "3-Good", 4: "4-High"}
        )
        fig_es = px.bar(
            es_grp, x="Satisfaction", y="Rate", color="Rate",
            color_continuous_scale="RdYlGn_r",
            text=[f"{r:.1f}%" for r in es_grp["Rate"]]
        )
        fig_es.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8")
        fig_es.update_traces(textposition="outside")
        fig_es.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), coloraxis_showscale=False
        )
        st.plotly_chart(fig_es, width='stretch')


# =========================================================
# TAB 5: 3D TENURE & CAREER TRAJECTORIES
# =========================================================
with tab_tenure_3d:
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.5rem;">⏳</span>
        <h3 style="margin:0;font-size:1.35rem;font-weight:800;color:#F8FAFC;">
            3D Career Stagnation &amp; Retention Survival Landscape
        </h3>
    </div>
    <p style="color:#94A3B8;font-size:0.88rem;margin:10px 0 18px 0;">
        Continuous 3D mapping of career velocity — tenure, promotion stagnation, and compensation alignment.
    </p>
    """, unsafe_allow_html=True)

    fig_career_3d = px.scatter_3d(
        filtered,
        x="YearsAtCompany", y="YearsSinceLastPromotion", z="MonthlyIncome",
        color="Attrition_Label",
        color_discrete_map={"Yes": "#EF4444", "No": "#38BDF8"},
        opacity=0.72,
        hover_data=["JobRole", "Age", "Department", "WorkLifeBalance"]
    )
    fig_career_3d.update_layout(
        scene=dict(
            xaxis=dict(title="Tenure (Years)",
                       backgroundcolor="rgba(11,15,25,0.6)", gridcolor="rgba(148,163,184,0.15)"),
            yaxis=dict(title="Years Since Promotion",
                       backgroundcolor="rgba(11,15,25,0.6)", gridcolor="rgba(148,163,184,0.15)"),
            zaxis=dict(title="Monthly Income ($)",
                       backgroundcolor="rgba(11,15,25,0.6)", gridcolor="rgba(148,163,184,0.15)")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"),
        height=640,
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig_career_3d, width='stretch')

    st.markdown("---")
    tc1, tc2 = st.columns(2)

    with tc1:
        st.markdown("#### The Two-Year Onboarding Cliff")
        ten_grp = filtered.groupby("Tenure_Horizon", observed=False).agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        ten_grp["Rate"] = (ten_grp["Exits"] / ten_grp["Total"]) * 100
        fig_t = px.area(
            ten_grp, x="Tenure_Horizon", y="Rate",
            labels={"Rate": "Turnover %", "Tenure_Horizon": "Tenure Cohort"},
            color_discrete_sequence=["#EF4444"]
        )
        fig_t.update_traces(
    mode='lines+markers',
    fill='tozeroy',
    fillcolor='rgba(239,68,68,0.15)',
    line=dict(color="#EF4444", width=2.5),
    marker=dict(size=8)
)
        fig_t.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8",
                        annotation_text="14.2% benchmark")
        fig_t.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC")
        )
        st.plotly_chart(fig_t, width='stretch')

    with tc2:
        st.markdown("#### Promotion Latency Impact on Attrition")
        stag_grp = filtered.groupby("Promotion_Stagnant").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        stag_grp["Rate"] = (stag_grp["Exits"] / stag_grp["Total"]) * 100
        fig_s = px.bar(
            stag_grp, x="Promotion_Stagnant", y="Rate", color="Promotion_Stagnant",
            color_discrete_map={"Stagnant (≥3 Yrs)": "#EF4444", "Active Progression": "#10B981"},
            text=[f"{r:.1f}%  ({e}/{t})" for r, e, t in
                  zip(stag_grp["Rate"], stag_grp["Exits"], stag_grp["Total"])]
        )
        fig_s.update_traces(textposition="outside")
        fig_s.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), showlegend=False,
            yaxis_title="Attrition Rate (%)"
        )
        st.plotly_chart(fig_s, width='stretch')

    st.markdown("---")
    st.markdown("#### Stock Option Level Impact on Retention")
    so_grp = filtered.groupby("StockOptionLevel").agg(
        Total=("Attrition_Numeric", "count"),
        Exits=("Attrition_Numeric", "sum")
    ).reset_index()
    so_grp["Rate"] = (so_grp["Exits"] / so_grp["Total"]) * 100
    so_grp["Level_Label"] = so_grp["StockOptionLevel"].map(
        {0: "Level 0 — None", 1: "Level 1 — Basic", 2: "Level 2 — Standard", 3: "Level 3 — Premium"}
    )
    fig_so = px.bar(
        so_grp, x="Level_Label", y="Rate", color="Rate",
        color_continuous_scale="RdYlGn_r",
        text=[f"{r:.1f}%" for r in so_grp["Rate"]]
    )
    fig_so.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8",
                     annotation_text="Benchmark 14.2%")
    fig_so.update_traces(textposition="outside")
    fig_so.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"), coloraxis_showscale=False,
        xaxis_title="Stock Option Level", yaxis_title="Attrition Rate (%)"
    )
    st.plotly_chart(fig_so, width='stretch')


# =========================================================
# TAB 6: BURNOUT & WORKLOAD MATRIX
# =========================================================
with tab_burnout:
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.5rem;">⚡</span>
        <h3 style="margin:0;font-size:1.35rem;font-weight:800;color:#F8FAFC;">
            Burnout Catalysts: Overtime, Travel Fatigue &amp; Commute Burden
        </h3>
    </div>
    <p style="color:#94A3B8;font-size:0.88rem;margin:10px 0 18px 0;">
        Isolating the highest-leverage environmental stressors driving voluntary departure across operational cohorts.
    </p>
    """, unsafe_allow_html=True)

    w1, w2, w3 = st.columns(3)

    with w1:
        st.markdown("#### Overtime Attrition Multiplier")
        ot_res = filtered.groupby("OverTime").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        ot_res["Rate"] = (ot_res["Exits"] / ot_res["Total"]) * 100
        fig_ot = px.bar(
            ot_res, x="OverTime", y="Rate", color="OverTime",
            color_discrete_map={"Yes": "#EF4444", "No": "#10B981"},
            text=[f"{r:.1f}%" for r in ot_res["Rate"]],
            labels={"Rate": "Attrition %", "OverTime": "Overtime Required"}
        )
        fig_ot.update_traces(textposition="outside", textfont_size=13)
        fig_ot.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), showlegend=False
        )
        st.plotly_chart(fig_ot, width='stretch')

    with w2:
        st.markdown("#### Business Travel Frequency Impact")
        tr_res = filtered.groupby("BusinessTravel").agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        tr_res["Rate"] = (tr_res["Exits"] / tr_res["Total"]) * 100
        fig_tr = px.bar(
            tr_res, x="BusinessTravel", y="Rate", color="Rate",
            color_continuous_scale="Magma",
            text=[f"{r:.1f}%" for r in tr_res["Rate"]],
            labels={"Rate": "Attrition %", "BusinessTravel": "Travel Frequency"}
        )
        fig_tr.update_traces(textposition="outside", textfont_size=13)
        fig_tr.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), coloraxis_showscale=False
        )
        st.plotly_chart(fig_tr, width='stretch')

    with w3:
        st.markdown("#### Commute Distance Burnout Tiers")
        cm_res = filtered.groupby("Commute_Tier", observed=False).agg(
            Total=("Attrition_Numeric", "count"),
            Exits=("Attrition_Numeric", "sum")
        ).reset_index()
        cm_res["Rate"] = (cm_res["Exits"] / cm_res["Total"]) * 100
        fig_cm = px.bar(
            cm_res, x="Commute_Tier", y="Rate", color="Rate",
            color_continuous_scale="Burg",
            text=[f"{r:.1f}%" for r in cm_res["Rate"]],
            labels={"Rate": "Attrition %", "Commute_Tier": "Commute Distance"}
        )
        fig_cm.update_traces(textposition="outside", textfont_size=13)
        fig_cm.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), coloraxis_showscale=False
        )
        st.plotly_chart(fig_cm, width='stretch')

    st.markdown("---")
    burn1, burn2 = st.columns(2)

    with burn1:
        st.markdown("#### Work-Life Balance × Overtime Interaction Heatmap")
        _wlb = filtered.copy()
        _wlb["WLB_Label"] = _wlb["WorkLifeBalance"].map({1: "1-Poor", 2: "2-Fair", 3: "3-Good", 4: "4-Best"})
        wlb_pivot = _wlb.pivot_table(
            index="WLB_Label", columns="OverTime",
            values="Attrition_Numeric", aggfunc=lambda x: (x.sum() / len(x)) * 100
        ).fillna(0)
        fig_wlb = px.imshow(
            wlb_pivot,
            labels=dict(x="Overtime Required", y="Work-Life Balance Score", color="Attrition %"),
            color_continuous_scale="Reds", text_auto=".1f", aspect="auto"
        )
        fig_wlb.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"), height=340)
        st.plotly_chart(fig_wlb, width='stretch')

    with burn2:
        st.markdown("#### Burnout Index Distribution by Attrition Status")
        fig_bi = px.histogram(
            filtered, x="Burnout_Index", color="Attrition_Label",
            nbins=20, barmode="overlay", opacity=0.82,
            color_discrete_map={"Yes": "#EF4444", "No": "#38BDF8"},
            labels={"Burnout_Index": "Composite Burnout Score (0–3)", "Attrition_Label": "Attrition"}
        )
        fig_bi.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), height=340,
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )
        st.plotly_chart(fig_bi, width='stretch')

    st.markdown("---")
    st.markdown("#### Relationship Satisfaction vs Attrition")
    rs_grp = filtered.groupby("RelationshipSatisfaction").agg(
        Total=("Attrition_Numeric", "count"),
        Exits=("Attrition_Numeric", "sum")
    ).reset_index()
    rs_grp["Rate"] = (rs_grp["Exits"] / rs_grp["Total"]) * 100
    rs_grp["Label"] = rs_grp["RelationshipSatisfaction"].map(
        {1: "1-Low", 2: "2-Fair", 3: "3-Good", 4: "4-High"}
    )
    fig_rs = px.bar(
        rs_grp, x="Label", y="Rate", color="Rate",
        color_continuous_scale="RdYlGn_r",
        text=[f"{r:.1f}%" for r in rs_grp["Rate"]]
    )
    fig_rs.add_hline(y=14.2, line_dash="dash", line_color="#38BDF8", annotation_text="Benchmark")
    fig_rs.update_traces(textposition="outside")
    fig_rs.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"), coloraxis_showscale=False,
        xaxis_title="Relationship Satisfaction", yaxis_title="Attrition Rate (%)"
    )
    st.plotly_chart(fig_rs, width='stretch')


# =========================================================
# TAB 7: DATA PIPELINE & FEATURE ENGINEERING AUDIT
# =========================================================
with tab_pipeline:
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.5rem;">🧪</span>
        <h3 style="margin:0;font-size:1.35rem;font-weight:800;color:#F8FAFC;">
            Data Quality, Deduplication &amp; Feature Engineering Audit
        </h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    pc1, pc2, pc3, pc4 = st.columns(4)
    pipeline_cards = [
        (pc1, "RECORDS INGESTED",   telemetry["initial_rows"],                    "Raw HR Telemetry",      "card-purple", "#C084FC"),
        (pc2, "DUPLICATES REMOVED", telemetry["duplicates_removed"],              "Auto-deduplication",    "card-red",    "#FCA5A5"),
        (pc3, "CLEAN RECORDS",      telemetry["final_rows"],                      "Net validated dataset", "card-amber",  "#FCD34D"),
        (pc4, "FEATURES ENGINEERED",len(telemetry["new_features_engineered"]),    "Derived attributes",    "card-emerald","#6EE7B7"),
    ]
    for col, label, val, sub, card_cls, sub_color in pipeline_cards:
        with col:
            st.markdown(f"""
            <div class="glass-card {card_cls}" style="padding:16px;">
                <div class="kpi-title"><span>{label}</span></div>
                <div class="kpi-num">{val:,}</div>
                <div class="kpi-sub" style="color:{sub_color};">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🔬 Engineered Feature Dictionary")
    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown("""
        | Feature | Description |
        |:--|:--|
        | `Age_Group` | Generational cohorts — Gen-Z, Millennial, Mid-Career, Senior, Veteran |
        | `Tenure_Horizon` | 0-2y Onboarding · 3-5y Mid-Tenure · 10+y Veteran |
        | `Commute_Tier` | Short (<5mi) · Moderate (6-15mi) · High-Friction (>15mi) |
        | `Education_Level_Label` | Below College → Doctorate mapping |
        """)
    with fc2:
        st.markdown("""
        | Feature | Description |
        |:--|:--|
        | `Promotion_Stagnant` | Flags staff ≥3 yrs without promotion |
        | `Manager_Continuity_Ratio` | Manager tenure / total company tenure |
        | `Burnout_Index` | Overtime 1.2 + Travel 0.8 + WLB 0.6 + Commute 0.4 |
        | `Risk_Score` & `Risk_Tier` | Flight risk classifier (Low / Medium / High) |
        """)

    if telemetry.get("dropped_constant_columns"):
        st.info(f"**Dropped Constant Columns:** `{telemetry['dropped_constant_columns']}`")

    st.markdown("---")
    st.markdown("#### 📊 Feature Correlation Matrix (Numeric Fields)")
    numeric_cols = ["Age", "MonthlyIncome", "YearsAtCompany", "YearsSinceLastPromotion",
                    "JobLevel", "Burnout_Index", "Risk_Score", "Attrition_Numeric",
                    "TotalWorkingYears", "YearsWithCurrManager"]
    corr_cols = [c for c in numeric_cols if c in filtered.columns]
    if len(corr_cols) >= 3:
        corr_matrix = filtered[corr_cols].corr()
        fig_corr = px.imshow(
            corr_matrix, text_auto=".2f", aspect="auto",
            color_continuous_scale="RdBu_r", zmin=-1, zmax=1
        )
        fig_corr.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#F8FAFC"),
            height=460, margin=dict(t=20)
        )
        st.plotly_chart(fig_corr, width='stretch')

    st.markdown("---")
    st.markdown("#### Sample Cleaned Telemetry (First 30 Records)")
    preview_cols = [c for c in [
        "JobRole", "Department", "Attrition_Label", "Age_Group", "Tenure_Horizon",
        "OverTime", "BusinessTravel", "MonthlyIncome", "Burnout_Index", "Risk_Score", "Risk_Tier"
    ] if c in filtered.columns]
    st.dataframe(filtered[preview_cols].head(30), width='stretch')

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Cleaned & Engineered Dataset (CSV)",
        data=csv_bytes,
        file_name="palo_alto_attrition_cleaned.csv",
        mime="text/csv"
    )


# =========================================================
# TAB 8: POLICY RISK SIMULATOR
# =========================================================
with tab_sim:
    st.markdown("""
    <div class="section-header">
        <span style="font-size:1.5rem;">🎯</span>
        <h3 style="margin:0;font-size:1.35rem;font-weight:800;color:#F8FAFC;">
            What-If Policy Intervention Simulator
        </h3>
    </div>
    <p style="color:#94A3B8;font-size:0.88rem;margin:10px 0 20px 0;">
        Quantify projected attrition reduction and capital cost avoidance through targeted HR policy interventions.
        Adjust the levers below to model retention investment scenarios in real time.
    </p>
    """, unsafe_allow_html=True)

    s_col1, s_col2 = st.columns([1, 1])

    with s_col1:
        st.markdown("#### ⚙️ Policy Levers")
        st.markdown("**Workload Governance**")
        sim_ot     = st.slider("Overtime Reduction (%)",                0, 100, 50, step=10)
        sim_travel = st.slider("Frequent Travel Reduction (%)",         0, 100, 40, step=10)
        st.markdown("**Compensation & Equity**")
        sim_sal    = st.slider("Base Salary Realignment for L1-L2 (%)", 0,  30, 10, step=5)
        sim_stock  = st.checkbox("Expand RSU / Stock Option Grants (Level 1–2)", value=True)
        st.markdown("**Career Development**")
        sim_promo  = st.checkbox("Automated 30-Month Promotion Review Engine", value=True)
        sim_flex   = st.checkbox("Hybrid Work & Commute Relief Policy",         value=True)
        sim_mentor = st.checkbox("Structured 2-Year Onboarding Guardrail",      value=False)

    with s_col2:
        st.markdown("#### 📈 Projected Retention & Capital ROI")

        _base   = filtered["Attrition_Numeric"].mean()
        _salary = filtered["MonthlyIncome"].mean()

        _mit = min(0.68,
            (sim_ot     / 100.0) * 0.28 +
            (sim_travel / 100.0) * 0.10 +
            (sim_sal    / 100.0) * 0.30 +
            (0.08 if sim_stock  else 0.0) +
            (0.12 if sim_promo  else 0.0) +
            (0.08 if sim_flex   else 0.0) +
            (0.10 if sim_mentor else 0.0)
        )
        _proj  = _base * (1 - _mit)
        _saved = int(round((_base - _proj) * len(filtered)))
        _cost  = _saved * _salary * 6

        rm1, rm2 = st.columns(2)
        with rm1:
            st.metric("Simulated Turnover Rate",
                      f"{_proj * 100:.1f}%",
                      f"-{(_base - _proj) * 100:.1f}% reduction",
                      delta_color="inverse")
        with rm2:
            st.metric("Preserved Security Talent", f"+{_saved} staff", "Retained")
        st.metric("Capital Cost Avoidance", f"${_cost / 1_000_000:.2f}M", "Preserved Capital")

        _comp = pd.DataFrame({
            "Scenario": ["Status Quo", "With Interventions"],
            "Turnover (%)": [_base * 100, _proj * 100],
        })
        fig_comp = px.bar(
            _comp, x="Scenario", y="Turnover (%)", color="Scenario",
            color_discrete_map={"Status Quo": "#EF4444", "With Interventions": "#10B981"},
            text=[f"{v:.1f}%" for v in _comp["Turnover (%)"]]
        )
        fig_comp.update_traces(textposition="outside", textfont_size=14)
        fig_comp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), showlegend=False,
            yaxis_range=[0, max(_comp["Turnover (%)"].max() + 12, 20)]
        )
        st.plotly_chart(fig_comp, width='stretch')

    # Policy Impact Waterfall decomposition
    _levers, _deltas = [], []
    for _lbl, _active, _w in [
        ("Overtime Cap",         sim_ot > 0,   -(sim_ot / 100)     * 0.28 * _base * 100),
        ("Travel Reduction",     sim_travel > 0, -(sim_travel / 100) * 0.10 * _base * 100),
        ("Salary Alignment",     sim_sal > 0,  -(sim_sal / 100)     * 0.30 * _base * 100),
        ("RSU Grants",           sim_stock,    -0.08 * _base * 100),
        ("Promotion Reviews",    sim_promo,    -0.12 * _base * 100),
        ("Hybrid Flex",          sim_flex,     -0.08 * _base * 100),
        ("Onboarding Guardrail", sim_mentor,   -0.10 * _base * 100),
    ]:
        if _active:
            _levers.append(_lbl)
            _deltas.append(_w)

    if _levers:
        st.markdown("#### Policy Impact Waterfall Decomposition")
        fig_wf = go.Figure(go.Waterfall(
            orientation="v", x=_levers, y=_deltas,
            connector=dict(line=dict(color="#334155", width=1.5)),
            decreasing=dict(marker=dict(color="#10B981", line=dict(color="#059669", width=1))),
            increasing=dict(marker=dict(color="#EF4444", line=dict(color="#DC2626", width=1))),
            totals=dict(marker=dict(color="#38BDF8", line=dict(color="#0284C7", width=1)))
        ))
        fig_wf.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), height=340,
            yaxis_title="Attrition Rate Change (%)",
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_wf, width='stretch')

    st.markdown("---")
    st.markdown("#### 📋 Intervention Priority Matrix")
    priority_data = [
        {"Intervention": "Overtime Cap (≤5 hrs/wk)", "Impact": "High", "Cost": "Low", "Time to Effect": "1–3 months", "Risk Reduction": "28%"},
        {"Intervention": "Salary Band Realignment (L1–L2)", "Impact": "High", "Cost": "High", "Time to Effect": "1 month", "Risk Reduction": "30%"},
        {"Intervention": "Automated Promotion Reviews", "Impact": "High", "Cost": "Medium", "Time to Effect": "3–6 months", "Risk Reduction": "12%"},
        {"Intervention": "Hybrid Work Policy", "Impact": "Medium", "Cost": "Low", "Time to Effect": "1–2 months", "Risk Reduction": "8%"},
        {"Intervention": "RSU / Stock Option Expansion", "Impact": "Medium", "Cost": "High", "Time to Effect": "Quarterly cycle", "Risk Reduction": "8%"},
        {"Intervention": "2-Year Onboarding Guardrail", "Impact": "Medium", "Cost": "Medium", "Time to Effect": "6–12 months", "Risk Reduction": "10%"},
        {"Intervention": "Travel Frequency Reduction", "Impact": "Low", "Cost": "Low", "Time to Effect": "Immediate", "Risk Reduction": "10%"},
    ]
    st.dataframe(pd.DataFrame(priority_data), width='stretch')


# ---------------------------------------------------------
# Upgraded Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;">
    <span style="font-size:0.78rem;color:#475569;">
        🛡️ <b style="color:#94A3B8;">Palo Alto Networks</b> Cybersecurity People Analytics &amp;
        3D ONA Engine &nbsp;|&nbsp; Master Enterprise C-Suite Specification &nbsp;|&nbsp;
        Unified Mentor Capstone Project
    </span>
    <span style="font-size:0.75rem;color:#334155;">
        Powered by Streamlit 1.66 · Plotly 7.1 · Pandas 3.0 · Python 3.13
    </span>
</div>
""", unsafe_allow_html=True)
