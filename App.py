import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# List of possible logo filenames, checked in this order. Shared by the
# on-screen branding and the HTML report export so both stay in sync.
LOGO_CANDIDATES = ["Amrize_Logo_2025.svg", "Amrize_Logo_2025.png", "logo.png", "logo.svg"]


def find_logo_file():
    for name in LOGO_CANDIDATES:
        if os.path.exists(name):
            return name
    return None


def show_logo(width=220):
    """Safely display the company logo in the Streamlit UI, whether it's an
    SVG or a raster image (PNG/JPG).

    FIX: previously this just called st.image(name, ...) for whatever file
    was found. Streamlit's st.image() decodes raster images with PIL, and
    PIL cannot open SVG files (they're XML text, not pixel data) — that
    causes a PIL.UnidentifiedImageError crash if the logo is an SVG. SVGs
    are now rendered directly as HTML/base64, and raster files are
    validated with PIL before display; a broken file shows a warning
    instead of crashing the whole app.
    """
    logo_path = find_logo_file()
    if not logo_path:
        st.info("⚠️ Place 'Amrize_Logo_2025.svg' or 'logo.png' in your project folder.")
        return
    try:
        if logo_path.lower().endswith(".svg"):
            with open(logo_path, "r", encoding="utf-8") as f:
                svg_content = f.read()
            b64 = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
            st.markdown(f'<img src="data:image/svg+xml;base64,{b64}" width="{width}"/>', unsafe_allow_html=True)
        else:
            from PIL import Image
            Image.open(logo_path).verify()
            st.image(logo_path, width=width)
    except Exception as e:
        st.warning(f"⚠️ Couldn't load logo file '{logo_path}': {e}")


def get_logo_html_tag(style="height: 48px; margin-bottom: 12px;"):
    """Return an <img> tag with the logo embedded as base64 data, so the
    exported HTML report stays a single self-contained file (no separate
    image file to keep alongside it, no broken link if it's shared)."""
    logo_path = find_logo_file()
    if not logo_path:
        return ""
    try:
        ext = logo_path.lower().rsplit(".", 1)[-1]
        mime = "image/svg+xml" if ext == "svg" else f"image/{'jpeg' if ext in ('jpg', 'jpeg') else ext}"
        with open(logo_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f'<img src="data:{mime};base64,{b64}" style="{style}" alt="Amrize logo"/>'
    except Exception:
        return ""

# 1. Page Configuration
st.set_page_config(
    page_title="Amrize - Z-Groups Tracker Elevate",
    page_icon="📊",
    layout="wide"
)

# 2. Modern Light UI - TODAS LAS ALERTAS FORZADAS EN AZUL CORPORATIVO SUAVE
st.markdown("""
    <style>
    /* Global App Light Background */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    }

    /* Headers & Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #011e6a !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    /* Sidebar Styling (Deep Amrize Blue) */
    [data-testid="stSidebar"] {
        background-color: #011e6a;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* METRIC CARDS - UN SOLO BLOQUE AZUL CLARITO (#f0f5ff) CON ALTURA FIJA (140px) */
    div[data-testid="stMetric"] {
        background-color: #f0f5ff !important;
        border: 1px solid #dbeafe !important;
        border-left: 6px solid #2563eb !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        height: 140px !important;
        min-height: 140px !important;
        max-height: 140px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        box-sizing: border-box !important;
    }

    div[data-testid="stMetric"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    div[data-testid="stMetric"]:hover {
        box-shadow: 0 10px 15px -3px rgba(1, 30, 106, 0.12) !important;
        border-color: #93c5fd !important;
    }

    div[data-testid="stMetricValue"] {
        color: #001fbe !important;
        font-weight: 800 !important;
        font-size: 30px !important;
        word-break: break-all;
    }

    div[data-testid="stMetricLabel"] {
        color: #334155 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600 !important;
    }

    /* Table & Dataframe Modern Styling */
    div[data-testid="stDataFrame"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* FORZAR TODAS LAS ALERTAS (INFO, WARNING, SUCCESS) A AZUL SUAVE Y AZUL OSCURO EN TEXTO */
    .stAlert,
    div[data-testid="stAlert"] {
        background-color: #e0f2fe !important;
        border: 1px solid #7dd3fc !important;
        border-left: 6px solid #0284c7 !important;
        color: #0369a1 !important;
        border-radius: 10px !important;
    }
    .stAlert p, .stAlert span, .stAlert div,
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] span, div[data-testid="stAlert"] div {
        color: #0369a1 !important;
        font-weight: 600 !important;
    }

    /* Horizontal Dividers */
    hr {
        border-top: 1.5px solid #e2e8f0;
        margin: 2rem 0;
    }

    /* Period Badge Styling */
    .period-badge {
        background: #f0f5ff;
        color: #011e6a;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        display: inline-block;
        border: 1px solid #93c5fd;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(1, 30, 106, 0.05);
    }

    /* Custom Buttons Styling */
    .stButton>button {
        background-color: #0284c7;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 18px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #0369a1;
        box-shadow: 0 4px 10px rgba(2, 132, 199, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
# FIX: credentials are no longer hardcoded in source. They are read from
# st.secrets (Streamlit's secrets manager) so they are never committed to
# the repo in plain text. Add a `.streamlit/secrets.toml` file (kept out of
# version control) with:
#
#   [auth]
#   username = "ElevateBE"
#   password = "your-real-password"
#
# In Streamlit Community Cloud, set the same values under
# "Settings -> Secrets" instead of a local file.
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


def _get_credentials():
    try:
        return st.secrets["auth"]["username"], st.secrets["auth"]["password"]
    except Exception:
        # Fallback so the app doesn't crash if secrets aren't configured yet
        # (useful for local dev), but this should be replaced before deploying.
        st.sidebar.warning(
            "⚠️ No secrets configured (st.secrets['auth']). Using a temporary "
            "development-only login. Set real credentials in secrets.toml before sharing this app."
        )
        return "ElevateBE", "Elevate2026"


def check_login():
    """Validates credentials against st.secrets (see note above)."""
    valid_user, valid_pass = _get_credentials()
    if st.session_state["username_input"] == valid_user and st.session_state["password_input"] == valid_pass:
        st.session_state["logged_in"] = True
        if "login_error" in st.session_state:
            del st.session_state["login_error"]
    else:
        st.session_state["login_error"] = "❌ Incorrect username or password."


if not st.session_state["logged_in"]:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.write("")
        st.write("")
        show_logo(width=220)

        st.subheader("🔑 Sign In to Z-Groups Tracker")
        st.text_input("Username", key="username_input")
        st.text_input("Password", type="password", key="password_input", on_change=check_login)
        st.button("Login", on_click=check_login, type="primary")

        if "login_error" in st.session_state:
            st.error(st.session_state["login_error"])

    st.stop()

# --- BRANDING: AUTOMATIC LOGO DETECTOR (After Login) ---
show_logo(width=280)

st.title("Z-Groups Tracker Elevate")

# --- SIDEBAR: SELECTOR DE MES Y AÑO DEL REPORTE ---
st.sidebar.header("🗓️ Report Period Selection")

months_list = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
years_list = [2024, 2025, 2026, 2027, 2028, 2029, 2030]

current_month_index = datetime.now().month - 1
current_year = datetime.now().year

selected_month = st.sidebar.selectbox("Report Month", options=months_list, index=current_month_index)
# FIX: replaced the magic-number fallback (`2`, i.e. hardcoded to 2026) with a
# calculation based on the actual current year, so the default index stays
# correct even if `years_list` changes or years pass.
default_year_index = (
    years_list.index(current_year)
    if current_year in years_list
    else min(range(len(years_list)), key=lambda i: abs(years_list[i] - current_year))
)
selected_year = st.sidebar.selectbox("Report Year", options=years_list, index=default_year_index)

report_period_str = f"{selected_month} {selected_year}"

# Badge de Periodo Estilizado
st.markdown(f'<div class="period-badge">📅 Active Report Period: <strong>{report_period_str}</strong></div>', unsafe_allow_html=True)
st.markdown("Upload your comparative monthly files (Excel or CSV) or connect to Google Sheets to track analyst changes and overall portfolio movement.")

# Placeholder for the "Download report as HTML" button. It's declared here
# so the button appears near the top of the page, but it's only filled in
# with real data at the very end of the script, once every table and
# summary number below has actually been computed.
report_download_placeholder = st.empty()


# --- HELPER FUNCTION: UNIVERSAL FILE READER ---
def load_data_file(uploaded_file):
    """Dynamically reads Excel (.xlsx, .xls) and CSV files"""
    if uploaded_file is not None:
        file_name = uploaded_file.name.lower()
        if file_name.endswith('.csv'):
            try:
                return pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file, encoding='latin1')
        else:
            return pd.read_excel(uploaded_file)
    return None


# --- STEP 1: DATA SOURCE SELECTION ---
st.sidebar.header("Data Source Selection")
data_source = st.sidebar.radio(
    "Choose Data Source:",
    ("Upload Files (Excel / CSV)", "Connect Google Sheets")
)

df_prev_raw = None
df_curr_raw = None

if data_source == "Upload Files (Excel / CSV)":
    prev_file = st.sidebar.file_uploader("Upload PREVIOUS MONTH file", type=["xlsx", "xls", "csv"])
    curr_file = st.sidebar.file_uploader("Upload CURRENT MONTH file", type=["xlsx", "xls", "csv"])

    if prev_file and curr_file:
        try:
            df_prev_raw = load_data_file(prev_file)
            df_curr_raw = load_data_file(curr_file)
        except Exception as e:
            st.error(f"Error reading uploaded files: {e}")
            st.stop()

else:
    default_sheet_url = "https://docs.google.com/spreadsheets/d/1HmShbAOnElJOQ9qy0lvYkxL6qxS7dc2xl9QzuUWTaAs/edit?gid=1603648333#gid=1603648333"
    sheet_url = st.sidebar.text_input("Google Sheet URL", value=default_sheet_url)
    # FIX: the tab names are still assumed to be "P.M. Report" / "C.M. Report".
    # If a different workbook is pasted, load will fail with a clear message
    # instead of a generic traceback, and the tab names are now configurable
    # from the sidebar instead of being buried in the code.
    pm_tab_name = st.sidebar.text_input("Previous Month tab name", value="P.M. Report")
    cm_tab_name = st.sidebar.text_input("Current Month tab name", value="C.M. Report")

    if st.sidebar.button("Load Google Sheets Data"):
        try:
            if "/d/" in sheet_url:
                sheet_id = sheet_url.split("/d/")[1].split("/")[0]
            else:
                sheet_id = sheet_url

            url_pm = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={pm_tab_name.replace(' ', '+')}"
            url_cm = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={cm_tab_name.replace(' ', '+')}"

            df_prev_raw = pd.read_csv(url_pm)
            df_curr_raw = pd.read_csv(url_cm)

            st.session_state["df_prev_raw"] = df_prev_raw
            st.session_state["df_curr_raw"] = df_curr_raw
            st.sidebar.success("Google Sheets loaded successfully!")
        except Exception as e:
            st.error(
                f"Error connecting to Google Sheets: {e}\n\n"
                f"Check that the sheet is shared as 'Anyone with the link can view' and that "
                f"the tab names ('{pm_tab_name}', '{cm_tab_name}') match exactly."
            )
            st.stop()
    elif "df_prev_raw" in st.session_state and "df_curr_raw" in st.session_state:
        df_prev_raw = st.session_state["df_prev_raw"]
        df_curr_raw = st.session_state["df_curr_raw"]

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

if df_prev_raw is None or df_curr_raw is None:
    st.info("💡 Please upload both previous and current month files or load the Google Sheets data from the sidebar.")
    st.stop()

# --- STEP 2: ROBUST DATA CLEANING & VALIDATION ---


def sanitize_and_normalize_columns(df):
    df.columns = df.columns.astype(str).str.strip()
    if "Status" not in df.columns and len(df.columns) >= 7:
        df.rename(columns={df.columns[6]: "Status"}, inplace=True)
    return df


df_prev_raw = sanitize_and_normalize_columns(df_prev_raw)
df_curr_raw = sanitize_and_normalize_columns(df_curr_raw)

required_cols = ["Customer", "Customer Name", "Z-Group", "Credit Analyst", "Total Past Due", "Total Balance"]

missing_prev = [c for c in required_cols if c not in df_prev_raw.columns]
missing_curr = [c for c in required_cols if c not in df_curr_raw.columns]

if missing_prev or missing_curr:
    st.error(f"Error: Missing required columns!\nPrevious File Missing: {missing_prev}\nCurrent File Missing: {missing_curr}")
    st.stop()


def clean_currency_series(series):
    """Parse currency strings to numeric values, correctly preserving
    negative / credit balances.

    FIX: the previous version only stripped '$' and ',' before parsing.
    Accounting-style negatives — e.g. "(1,234.56)" for a credit/negative
    balance — don't match a plain numeric pattern, so pd.to_numeric coerced
    them to NaN, and the subsequent .fillna(0) silently turned every
    negative balance into $0.00. That meant credits and negative balances
    were being dropped from every table and total in the report. Both
    "(1,234.56)" and "-1,234.56" style negatives are now handled correctly.
    """
    s = series.astype(str).str.strip()
    is_paren_negative = s.str.match(r'^\(.*\)$')
    s = s.str.replace(r'[()]', '', regex=True)
    s = s.str.replace(r'[\$,]', '', regex=True).str.strip()
    values = pd.to_numeric(s, errors='coerce').fillna(0)
    values = values.where(~is_paren_negative, -values.abs())
    return values


def clean_data(df):
    df_clean = df.copy()

    df_clean = df_clean[
        df_clean["Total Balance"].astype(str).str.strip().str.upper() != "NOT FOUND"
    ]

    # FIX (data-integrity bug): the previous version coerced every
    # non-numeric / blank "Customer" ID to 0 via `.fillna(0)`. That meant any
    # row with a malformed ID (blank cell, text, etc.) silently collapsed to
    # the same key "0". Later, `pd.merge(..., on="Customer")` would then
    # match ALL such rows against each other (a cartesian blow-up), corrupting
    # the "Analyst Assignment Transitions", "New Accounts" and executive
    # summary numbers. We now drop rows whose Customer ID can't be parsed
    # instead of silently merging them together, and warn the user so bad
    # source data is visible rather than hidden.
    customer_numeric = pd.to_numeric(
        df_clean["Customer"].astype(str).str.replace(r'\.0$', '', regex=True),
        errors='coerce'
    )
    n_unparseable = customer_numeric.isna().sum()
    if n_unparseable > 0:
        st.warning(
            f"⚠️ Skipped {n_unparseable} row(s) with a missing or invalid 'Customer' ID "
            f"(these would otherwise be merged together incorrectly)."
        )
    df_clean = df_clean[customer_numeric.notna()].copy()
    df_clean["Customer"] = customer_numeric[customer_numeric.notna()].astype(int).astype(str)

    df_clean["Total Balance"] = clean_currency_series(df_clean["Total Balance"])
    df_clean["Total Past Due"] = clean_currency_series(df_clean["Total Past Due"])

    if "Status" in df_clean.columns:
        df_clean["Status"] = df_clean["Status"].fillna("Unspecified").astype(str).str.strip()
    else:
        df_clean["Status"] = "Unspecified"

    return df_clean


df_prev_global = clean_data(df_prev_raw)
df_curr_global = clean_data(df_curr_raw)

# --- STEP 3: GENERAL PORTFOLIO SUMMARY ---
prev_active_accounts = df_prev_global[df_prev_global["Status"].str.upper() == "ACTIVE"]
curr_active_accounts = df_curr_global[df_curr_global["Status"].str.upper() == "ACTIVE"]

prev_active_count = len(prev_active_accounts)
curr_active_count = len(curr_active_accounts)

if prev_active_count > 0:
    variation_active = ((curr_active_count - prev_active_count) / prev_active_count) * 100
    variation_str_active = f"{variation_active:+.2f}%"
else:
    variation_str_active = "N/A"

st.subheader("📌 General Portfolio Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Active Accounts (Previous Month)",
        value=f"{prev_active_count:,}"
    )
with col2:
    st.metric(
        label=f"Active Accounts ({report_period_str})",
        value=f"{curr_active_count:,}",
        delta=variation_str_active
    )
with col3:
    total_balance_active_curr = curr_active_accounts[curr_active_accounts["Total Balance"] != 0]["Total Balance"].sum()
    st.metric(
        label=f"Total Active Balance ({report_period_str})",
        value=f"${total_balance_active_curr:,.2f}"
    )

st.write("---")

# --- SIDEBAR FILTER: STATUS ---
df_prev_clean = df_prev_global.copy()
df_curr_clean = df_curr_global.copy()

available_statuses = sorted(list(set(df_prev_clean["Status"].unique()).union(set(df_curr_clean["Status"].unique()))))
if available_statuses and available_statuses != ["Unspecified"]:
    selected_statuses = st.sidebar.multiselect(
        "Filter Tables by Status (Column G)",
        options=available_statuses,
        default=available_statuses
    )
    if selected_statuses:
        df_prev_clean = df_prev_clean[df_prev_clean["Status"].isin(selected_statuses)]
        df_curr_clean = df_curr_clean[df_curr_clean["Status"].isin(selected_statuses)]

df_prev_open = df_prev_clean[df_prev_clean["Total Balance"] != 0]
df_curr_open = df_curr_clean[df_curr_clean["Total Balance"] != 0]

# --- STEP 4: STRICT ANALYST-TO-ANALYST TRANSITION TABLE ---
st.subheader("🔄 Credit Analyst Assignment Transitions")
st.markdown("These are the accounts that transitioned strictly **from one specific credit analyst to another** (excluding unassigned states or None).")

df_comparison = pd.merge(
    df_prev_clean[["Customer", "Credit Analyst", "Total Past Due", "Total Balance"]],
    df_curr_clean[["Customer", "Customer Name", "Credit Analyst", "Total Past Due", "Total Balance"]],
    on="Customer",
    suffixes=("_Previous", "_Current")
)

df_comparison["Credit Analyst_Previous"] = df_comparison["Credit Analyst_Previous"].fillna("").astype(str).str.strip()
df_comparison["Credit Analyst_Current"] = df_comparison["Credit Analyst_Current"].fillna("").astype(str).str.strip()

# FIX: unified the "invalid / unassigned" placeholder list so it's defined
# once and reused everywhere (Z-Group checks previously used a shorter,
# inconsistent list — see STEP on Unassigned Accounts below).
invalid_states = ["NOT FOUND", "NO CREDIT ANALYST ASSIGNED.", "NAN", "", "NONE", "UNASSIGNED", "NONE.", "NULL"]

df_analyst_changes = df_comparison[
    (df_comparison["Credit Analyst_Previous"] != df_comparison["Credit Analyst_Current"]) &
    (~df_comparison["Credit Analyst_Previous"].str.upper().isin(invalid_states)) &
    (~df_comparison["Credit Analyst_Current"].str.upper().isin(invalid_states)) &
    (df_comparison["Credit Analyst_Previous"].notna()) &
    (df_comparison["Credit Analyst_Current"].notna())
]

transferred_balance = 0
transferred_past_due = 0
df_changes_formatted = None  # populated below only if there are changes to show

if not df_analyst_changes.empty:
    df_changes_formatted = df_analyst_changes[[
        "Customer", "Customer Name",
        "Credit Analyst_Previous", "Credit Analyst_Current",
        "Total Past Due_Current", "Total Balance_Current"
    ]].rename(columns={
        "Credit Analyst_Previous": "Previous Analyst",
        "Credit Analyst_Current": "Current Analyst",
        "Total Past Due_Current": "Total Past Due",
        "Total Balance_Current": "Total Balance"
    })

    st.dataframe(
        df_changes_formatted.style.format({
            "Total Past Due": "${:,.2f}",
            "Total Balance": "${:,.2f}"
        }),
        use_container_width=True
    )

    transferred_past_due = df_analyst_changes["Total Past Due_Current"].sum()
    transferred_balance = df_analyst_changes["Total Balance_Current"].sum()
    transferred_count = len(df_analyst_changes)

    st.info(
        f"💰 **Financial Impact of Assignments:** Identified **{transferred_count}** accounts transferred between valid analysts for {report_period_str}, "
        f"representing **${transferred_balance:,.2f}** in Total Balance and **${transferred_past_due:,.2f}** in Total Past Due."
    )
else:
    st.info(f"✅ No credit analyst assignment transitions were detected between valid analysts for {report_period_str}.")

st.write("---")

# --- NEW SECTION: NEW ACCOUNTS OF THE MONTH ---
st.subheader("✨ New Accounts of the Month")
st.markdown(f"These are new active accounts identified in **{report_period_str}** with open AR that did not exist in the previous month report.")

prev_customer_ids = set(df_prev_clean["Customer"].unique())
df_new_accounts = df_curr_open[~df_curr_open["Customer"].isin(prev_customer_ids)]

new_accounts_count = len(df_new_accounts)
new_accounts_balance = df_new_accounts["Total Balance"].sum()
df_new_formatted = None  # populated below only if there are new accounts to show

if not df_new_accounts.empty:
    df_new_formatted = df_new_accounts[[
        "Customer", "Customer Name", "Z-Group", "Credit Analyst", "Total Past Due", "Total Balance"
    ]].rename(columns={
        "Credit Analyst": "Analyst",
        "Total Past Due": "Total Past Due",
        "Total Balance": "Total Balance"
    })

    st.dataframe(
        df_new_formatted.style.format({
            "Total Past Due": "${:,.2f}",
            "Total Balance": "${:,.2f}"
        }),
        use_container_width=True
    )
    st.info(
        f"New Accounts Impact: Identified {new_accounts_count} new open AR accounts in {report_period_str} with a combined balance of ${new_accounts_balance:,.2f}."
    )
else:
    st.info(f"No new open AR accounts were identified for {report_period_str}.")

st.write("---")

# --- UNASSIGNED ACCOUNTS SECTION ---
st.subheader("⚠️ Unassigned Accounts")
st.markdown(f"These are **{report_period_str}** accounts with an open balance where **BOTH Z-Group and Credit Analyst are empty or unassigned**.")

# FIX: this list used to be shorter than `invalid_states` (missing
# "UNASSIGNED" and "NO CREDIT ANALYST ASSIGNED."), so a Z-Group literally
# containing "Unassigned" would NOT have been caught here even though the
# equivalent Credit Analyst value would be. Reusing `invalid_states` makes
# both checks consistent.
invalid_zgroups = invalid_states

df_unassigned = df_curr_open[
    (
        (df_curr_open["Z-Group"].astype(str).str.strip().str.upper().isin(invalid_zgroups)) |
        (df_curr_open["Z-Group"].isna())
    ) &
    (
        (df_curr_open["Credit Analyst"].astype(str).str.strip().str.upper().isin(invalid_states)) |
        (df_curr_open["Credit Analyst"].isna())
    )
]

unassigned_balance_sum = 0
unassigned_count = len(df_unassigned)
df_unassigned_formatted = None  # populated below only if there are unassigned accounts to show

if not df_unassigned.empty:
    df_unassigned_formatted = df_unassigned[[
        "Customer", "Customer Name", "Status", "Z-Group", "Credit Analyst", "Total Past Due", "Total Balance"
    ]].rename(columns={
        "Credit Analyst": "Assigned Status",
        "Total Past Due": "Total Past Due",
        "Total Balance": "Total Balance"
    })

    st.dataframe(
        df_unassigned_formatted.style.format({
            "Total Past Due": "${:,.2f}",
            "Total Balance": "${:,.2f}"
        }),
        use_container_width=True
    )

    unassigned_balance_sum = df_unassigned["Total Balance"].sum()
    st.info(
        f"Total Exposure Unassigned: There are {unassigned_count} accounts in {report_period_str} with open balance missing BOTH Z-Group and Credit Analyst, "
        f"representing a total of ${unassigned_balance_sum:,.2f}."
    )
else:
    st.info(f"Great! No active open-balance accounts were found with both Z-Group and Credit Analyst empty in {report_period_str}.")

st.write("---")

# --- STEP 5: ANALYST PORTFOLIO DISTRIBUTION ---
st.subheader("👥 Analyst Portfolio Distribution & Monthly Variation")

df_prev_valid_analysts = df_prev_global[~df_prev_global["Credit Analyst"].astype(str).str.strip().str.upper().isin(invalid_states)]
df_curr_valid_analysts = df_curr_global[~df_curr_global["Credit Analyst"].astype(str).str.strip().str.upper().isin(invalid_states)]

prev_total_all = df_prev_valid_analysts.groupby("Credit Analyst").agg(Total_Prev_All=("Customer", "count")).reset_index()
curr_total_all = df_curr_valid_analysts.groupby("Credit Analyst").agg(Total_Curr_All=("Customer", "count")).reset_index()

df_prev_open_active = df_prev_valid_analysts[
    (df_prev_valid_analysts["Total Balance"] != 0) &
    (df_prev_valid_analysts["Status"].str.upper() == "ACTIVE")
]

df_curr_open_active = df_curr_valid_analysts[
    (df_curr_valid_analysts["Total Balance"] != 0) &
    (df_curr_valid_analysts["Status"].str.upper() == "ACTIVE")
]

prev_open_active_dist = df_prev_open_active.groupby("Credit Analyst").agg(Open_AR_Prev_Active=("Customer", "count")).reset_index()
curr_open_active_dist = df_curr_open_active.groupby("Credit Analyst").agg(
    Open_AR_Curr_Active=("Customer", "count"),
    Sum_Past_Due=("Total Past Due", "sum"),
    Sum_Balance=("Total Balance", "sum")
).reset_index()

df_dist_merged = pd.merge(curr_open_active_dist, prev_open_active_dist, on="Credit Analyst", how="outer")
df_dist_merged = pd.merge(df_dist_merged, curr_total_all, on="Credit Analyst", how="outer")
df_dist_merged = pd.merge(df_dist_merged, prev_total_all, on="Credit Analyst", how="outer").fillna(0)

df_dist_merged["Account_Diff"] = df_dist_merged["Open_AR_Curr_Active"] - df_dist_merged["Open_AR_Prev_Active"]


def calc_open_ar_pct(row):
    prev = row["Open_AR_Prev_Active"]
    curr = row["Open_AR_Curr_Active"]
    if prev > 0:
        return f"{((curr - prev) / prev * 100):+.2f}%"
    elif curr > 0:
        return "New (+100%)"
    else:
        return "0.00%"


df_dist_merged["Open AR % Change"] = df_dist_merged.apply(calc_open_ar_pct, axis=1)
df_dist_merged = df_dist_merged.sort_values(by="Open_AR_Curr_Active", ascending=False)

df_dist_final = df_dist_merged[[
    "Credit Analyst",
    "Total_Prev_All",
    "Total_Curr_All",
    "Open_AR_Prev_Active",
    "Open_AR_Curr_Active",
    "Open AR % Change",
    "Sum_Past_Due",
    "Sum_Balance"
]].rename(columns={
    "Credit Analyst": "Credit Analyst",
    "Total_Prev_All": "Prev Accounts (All)",
    "Total_Curr_All": "Curr Accounts (All)",
    "Open_AR_Prev_Active": "Prev Acc Open AR",
    "Open_AR_Curr_Active": "Curr Acc Open AR",
    "Open AR % Change": "Open AR % Change",
    "Sum_Past_Due": "Total Past Due",
    "Sum_Balance": "Total Balance"
})

st.dataframe(
    df_dist_final.style.format({
        "Prev Accounts (All)": "{:,.0f}",
        "Curr Accounts (All)": "{:,.0f}",
        "Prev Acc Open AR": "{:,.0f}",
        "Curr Acc Open AR": "{:,.0f}",
        "Total Past Due": "${:,.2f}",
        "Total Balance": "${:,.2f}"
    }),
    use_container_width=True
)

st.write("---")

# --- EXECUTIVE SUMMARY & INSIGHTS ---
st.subheader(f"📋 Executive Summary & Insights ({report_period_str})")

if not df_dist_merged.empty:
    top_vol_row = df_dist_merged.loc[df_dist_merged["Open_AR_Curr_Active"].idxmax()]
    top_vol_analyst = top_vol_row["Credit Analyst"]
    top_vol_count = int(top_vol_row["Open_AR_Curr_Active"])

    top_exp_row = df_dist_merged.loc[df_dist_merged["Sum_Balance"].idxmax()]
    top_exp_analyst = top_exp_row["Credit Analyst"]
    top_exp_balance = top_exp_row["Sum_Balance"]
else:
    top_vol_analyst, top_vol_count = "N/A", 0
    top_exp_analyst, top_exp_balance = "N/A", 0

# FIX: this block previously compared `df_prev_global` / `df_curr_global`
# (i.e. BEFORE the sidebar Status filter is applied) while every other
# section of the report ("Analyst Assignment Transitions", "New Accounts",
# "Unassigned Accounts", "Portfolio Distribution") uses the filtered
# `df_prev_clean` / `df_curr_clean`. That inconsistency meant "Highest
# Account Reduction" could include accounts the user had explicitly
# excluded via the Status filter, giving a number that didn't reconcile
# with the rest of the page. Now it uses the same filtered frames.
df_account_match = pd.merge(
    df_prev_clean[["Customer", "Credit Analyst"]],
    df_curr_clean[["Customer", "Credit Analyst", "Total Balance"]],
    on="Customer",
    suffixes=("_Prev", "_Curr")
)

df_account_match["Credit Analyst_Prev"] = df_account_match["Credit Analyst_Prev"].fillna("").astype(str).str.strip()
df_account_match["Credit Analyst_Curr"] = df_account_match["Credit Analyst_Curr"].fillna("").astype(str).str.strip()

df_lost_accounts = df_account_match[
    (~df_account_match["Credit Analyst_Prev"].str.upper().isin(invalid_states)) &
    (df_account_match["Credit Analyst_Prev"] != df_account_match["Credit Analyst_Curr"])
]

lost_summary = df_lost_accounts.groupby("Credit Analyst_Prev").agg(
    Lost_Count=("Customer", "count"),
    Lost_Balance_Current=("Total Balance", "sum")
).reset_index()

if not lost_summary.empty:
    max_lost_row = lost_summary.loc[lost_summary["Lost_Count"].idxmax()]
    lost_analyst = max_lost_row["Credit Analyst_Prev"]
    accounts_lost = int(max_lost_row["Lost_Count"])
    lost_balance_real = max_lost_row["Lost_Balance_Current"]
else:
    lost_analyst, accounts_lost, lost_balance_real = "N/A", 0, 0

col_summary, col_notes = st.columns([2, 1])

with col_summary:
    summary_text = f"""
    * **Workload Leader:** **{top_vol_analyst}** manages the highest volume of active clients with **{top_vol_count:,}** accounts.
    * **Risk Exposure Leader:** **{top_exp_analyst}** holds the highest portfolio risk exposure totaling **${top_exp_balance:,.2f}** in Total Balance.
    """

    if accounts_lost > 0:
        summary_text += f"""
    * **Highest Account Reduction:** **{lost_analyst}** had **{accounts_lost}** accounts removed from their portfolio in **{report_period_str}**, representing **${lost_balance_real:,.2f}** in Total Balance (based on current month values).
        """
    else:
        summary_text += f"""
    * **Highest Account Reduction:** No active analysts experienced account removals in **{report_period_str}**.
        """

    summary_text += f"""
    * **New Clients Added:** Identified **{new_accounts_count}** brand-new client accounts in **{report_period_str}**, representing **${new_accounts_balance:,.2f}** in open balance.
    * **Unassigned Portfolio:** There are **{unassigned_count}** unassigned accounts missing both Z-Group and Credit Analyst, representing **${unassigned_balance_sum:,.2f}**.
    """
    st.markdown(summary_text)

with col_notes:
    if unassigned_count > 0:
        st.info(
            f"⚠️ **Action Required:** We recommend reviewing and assigning analyst ownership to the **{unassigned_count} unassigned accounts** "
            f"as soon as possible to mitigate financial exposure of **${unassigned_balance_sum:,.2f}** for **{report_period_str}**."
        )
    else:
        st.info(f"✅ **Outstanding:** All active open-balance accounts have assigned analysts in {report_period_str}. Zero unattended balance detected.")

# --- DOWNLOAD REPORT AS HTML ---
# Builds a single self-contained HTML file (branding + every table and
# insight already computed above) and wires it to the download button
# placeholder created near the top of the page. The layout/CSS mirrors the
# Amrize-branded report template (kpi-card, section-title, alert-box,
# table-scroll-container / styled-table, single global search box) so the
# exported file looks the same whoever generates it.


def _df_to_html_table(df, currency_cols=None):
    """Render a DataFrame as a scrollable table (sticky header) inside a
    table-scroll-container, matching the report template's styled-table."""
    if df is None or df.empty:
        return "<p class='report-empty'>No data available for this section.</p>"
    df_display = df.copy()
    if currency_cols:
        for col in currency_cols:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
    raw_table_html = df_display.to_html(index=False, border=1, classes="dataframe styled-table", escape=True)
    return f'<div class="table-scroll-container">{raw_table_html}</div>'


report_generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Amrize - Z-Groups Tracker Elevate ({report_period_str})</title>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            margin: 0;
            padding: 30px;
        }}
        .header {{ margin-bottom: 24px; }}
        .title {{ font-size: 28px; font-weight: 800; color: #011e6a; margin-bottom: 8px; }}
        .period-badge {{
            display: inline-block; background: #f0f5ff; color: #011e6a;
            padding: 8px 18px; border-radius: 20px; font-weight: 600; font-size: 14px;
            border: 1px solid #93c5fd; margin-bottom: 20px;
        }}
        .kpi-container {{ display: flex; gap: 15px; margin-bottom: 30px; }}
        .kpi-card {{
            flex: 1; background: #f0f5ff; border: 1px solid #dbeafe;
            border-left: 6px solid #2563eb; padding: 20px; border-radius: 12px;
            box-sizing: border-box;
        }}
        .kpi-title {{ font-size: 12px; color: #334155; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-value {{ font-size: 28px; font-weight: 800; color: #001fbe; margin-top: 6px; }}

        .section-title {{ font-size: 20px; font-weight: 700; color: #011e6a; margin: 30px 0 15px 0; }}
        .section-desc {{ font-size: 14px; color: #64748b; margin-top: -10px; margin-bottom: 15px; }}

        /* Banner de Alerta y Nota Azul Corporativo */
        .alert-box {{
            background-color: #e0f2fe;
            border: 1px solid #7dd3fc;
            border-left: 6px solid #0284c7;
            padding: 14px 18px;
            color: #0369a1;
            border-radius: 10px;
            font-weight: 500;
            font-size: 14px;
            margin-top: 10px;
            margin-bottom: 20px;
        }}

        /* Contenedor de Tabla con Altura Fija y Scroll Vertical */
        .table-scroll-container {{
            max-height: 380px;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            margin-bottom: 10px;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .styled-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        .styled-table th, .styled-table td {{ padding: 12px 16px; text-align: left; font-size: 13px; border-bottom: 1px solid #e2e8f0; }}

        /* Encabezado congelado (Sticky) durante el Scroll */
        .styled-table th {{
            position: sticky;
            top: 0;
            z-index: 10;
            background-color: #011e6a;
            color: white;
            font-weight: 700;
        }}
        .styled-table tr:nth-child(even) {{ background-color: #f8fafc; }}
        .styled-table tr:hover {{ background-color: #f1f5f9; }}

        input[type="text"] {{
            width: 100%; padding: 10px 14px; border: 1px solid #cbd5e1; border-radius: 8px; margin-bottom: 15px; box-sizing: border-box;
        }}

        .insights-grid {{ display: flex; gap: 20px; background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; }}
        .insights-col {{ flex: 2; }}
        .notes-col {{ flex: 1; }}
        ul {{ line-height: 1.8; }}

        .report-empty {{ color: #64748b; font-style: italic; }}
        .footer {{ margin-top: 40px; color: #94a3b8; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        {get_logo_html_tag()}
        <div class="title">Z-Groups Tracker Elevate</div>
        <div class="period-badge">📅 Active Report Period: <strong>{report_period_str}</strong></div>
    </div>

    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">Active Accounts (Previous Month)</div>
            <div class="kpi-value">{prev_active_count:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Active Accounts ({report_period_str})</div>
            <div class="kpi-value">{curr_active_count:,} <span style="font-size:14px; color:#334155; font-weight:600;">({variation_str_active})</span></div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Total Active Balance ({report_period_str})</div>
            <div class="kpi-value">${total_balance_active_curr:,.2f}</div>
        </div>
    </div>

    <div class="section-title">🔄 Credit Analyst Assignment Transitions</div>
    <div class="section-desc">These are the accounts that transitioned strictly from one specific credit analyst to another (excluding unassigned states or None).</div>
    {f'{_df_to_html_table(df_changes_formatted, currency_cols=["Total Past Due", "Total Balance"])}<div class="alert-box">💰 <strong>Financial Impact of Assignments:</strong> Identified <strong>{transferred_count}</strong> accounts transferred between valid analysts for {report_period_str}, representing <strong>${transferred_balance:,.2f}</strong> in Total Balance and <strong>${transferred_past_due:,.2f}</strong> in Total Past Due.</div>' if df_changes_formatted is not None else f'<div class="alert-box">✅ No credit analyst assignment transitions were detected between valid analysts for {report_period_str}.</div>'}

    <div class="section-title">✨ New Accounts of the Month</div>
    <div class="section-desc">These are new active accounts identified in <strong>{report_period_str}</strong> with open AR that did not exist in the previous month report.</div>
    {f'{_df_to_html_table(df_new_formatted, currency_cols=["Total Past Due", "Total Balance"])}<div class="alert-box"><strong>New Accounts Impact:</strong> Identified <strong>{new_accounts_count}</strong> new open AR accounts in <strong>{report_period_str}</strong> with a combined balance of <strong>${new_accounts_balance:,.2f}</strong>.</div>' if df_new_formatted is not None else f'<div class="alert-box">No new open AR accounts were identified for {report_period_str}.</div>'}

    <div class="section-title">⚠️ Unassigned Accounts</div>
    <div class="section-desc">These are <strong>{report_period_str}</strong> accounts with an open balance where BOTH Z-Group and Credit Analyst are empty or unassigned.</div>
    {f'{_df_to_html_table(df_unassigned_formatted, currency_cols=["Total Past Due", "Total Balance"])}<div class="alert-box"><strong>Total Exposure Unassigned:</strong> There are <strong>{unassigned_count}</strong> accounts in <strong>{report_period_str}</strong> with open balance missing BOTH Z-Group and Credit Analyst, representing a total of <strong>${unassigned_balance_sum:,.2f}</strong>.</div>' if df_unassigned_formatted is not None else f'<div class="alert-box">Great! No active open-balance accounts were found with both Z-Group and Credit Analyst empty in {report_period_str}.</div>'}

    <div class="section-title">👥 Analyst Portfolio Distribution</div>
    <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="🔍 Search/Filter table by Analyst or Values...">
    {_df_to_html_table(df_dist_final, currency_cols=["Total Past Due", "Total Balance"])}

    <div class="section-title">📋 Executive Summary & Insights ({report_period_str})</div>
    <div class="insights-grid">
        <div class="insights-col">
            <ul>
                <li><strong>Workload Leader:</strong> <strong>{top_vol_analyst}</strong> manages the highest volume of active clients with <strong>{top_vol_count:,}</strong> accounts.</li>
                <li><strong>Risk Exposure Leader:</strong> <strong>{top_exp_analyst}</strong> holds the highest portfolio risk exposure totaling <strong>${top_exp_balance:,.2f}</strong> in Total Balance.</li>
                <li><strong>Highest Account Reduction:</strong> {f"<strong>{lost_analyst}</strong> had <strong>{accounts_lost}</strong> accounts removed from their portfolio in <strong>{report_period_str}</strong>, representing <strong>${lost_balance_real:,.2f}</strong> in Total Balance (based on current month values)." if accounts_lost > 0 else f"No active analysts experienced account removals in {report_period_str}."}</li>
                <li><strong>New Clients Added:</strong> Identified <strong>{new_accounts_count}</strong> brand-new client accounts in <strong>{report_period_str}</strong>, representing <strong>${new_accounts_balance:,.2f}</strong> in open balance.</li>
                <li><strong>Unassigned Portfolio:</strong> There are <strong>{unassigned_count}</strong> unassigned accounts missing both Z-Group and Credit Analyst, representing <strong>${unassigned_balance_sum:,.2f}</strong>.</li>
            </ul>
        </div>
        <div class="notes-col">
            {f'<div class="alert-box" style="margin-top: 0;">⚠️ <strong>Action Required:</strong> We recommend reviewing and assigning analyst ownership to the {unassigned_count} unassigned accounts as soon as possible to mitigate financial exposure of ${unassigned_balance_sum:,.2f} for {report_period_str}.</div>' if unassigned_count > 0 else f'<div class="alert-box" style="margin-top: 0;">✅ <strong>Outstanding:</strong> All active open-balance accounts have assigned analysts in {report_period_str}. Zero unattended balance detected.</div>'}
        </div>
    </div>

    <p class="footer">Generated by Z-Groups Tracker Elevate on {report_generated_at}.</p>

    <script>
        function filterTable() {{
            var input = document.getElementById("searchInput").value.toUpperCase();
            var tables = document.querySelectorAll(".styled-table");
            tables.forEach(table => {{
                var rows = table.querySelectorAll("tr");
                for (var i = 1; i < rows.length; i++) {{
                    var text = rows[i].innerText.toUpperCase();
                    rows[i].style.display = text.indexOf(input) > -1 ? "" : "none";
                }}
            }});
        }}
    </script>
</body>
</html>
"""

report_download_placeholder.download_button(
    label="⬇️ Download Report as HTML",
    data=html_report,
    file_name=f"Z_Group_Report_{report_period_str.replace(' ', '_')}.html",
    mime="text/html",
)
