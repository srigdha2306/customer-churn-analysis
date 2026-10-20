from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st 

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "telco_churn_cleaned.csv"
)

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.sidebar.title("Explore Customers")
st.sidebar.caption("Filter the data to explore customer segments.")

contract_options = sorted(df["Contract"].dropna().unique())
payment_options = sorted(df["PaymentMethod"].dropna().unique())

selected_contracts = st.sidebar.multiselect(
    "Contract Type",
    options=contract_options,
    default=contract_options
)

selected_payments = st.sidebar.multiselect(
    "Payment Method",
    options=payment_options,
    default=payment_options
)

min_tenure = int(df["tenure"].min())
max_tenure = int(df["tenure"].max())

selected_tenure = st.sidebar.slider(
    "Customer Tenure (months)",
    min_value=min_tenure,
    max_value=max_tenure,
    value=(min_tenure, max_tenure)
)

min_charges = float(df["MonthlyCharges"].min())
max_charges = float(df["MonthlyCharges"].max())

selected_charges = st.sidebar.slider(
    "Monthly Charges ($)",
    min_value=min_charges,
    max_value=max_charges,
    value=(min_charges, max_charges),
    step=1.0
)

filtered_df = df[
    df["Contract"].isin(selected_contracts)
    & df["PaymentMethod"].isin(selected_payments)
    & df["tenure"].between(
        selected_tenure[0], selected_tenure[1]
    )
    & df["MonthlyCharges"].between(
        selected_charges[0], selected_charges[1]
    )
]



st.title("📊Customer Churn & Retention Analytics")
st.write("Welcome to the Customer Churn Analysis Dashboard! This tool provides interactive visualizations and deep insights into customer behavior, helping you identify at-risk customers and understand key drivers of churn.")
st.divider()


st.markdown("""
<style>
/* Midnight plum background */
.stApp {
    background: #120D1F;
    color: #F5F0FF;
}

/* Spacious dashboard layout */
.block-container {
    max-width: 1450px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #F5F0FF !important;
    letter-spacing: -0.5px;
}

h1 {
    font-size: 2.5rem !important;
    font-weight: 750 !important;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: #211832;
    border: 1px solid #493663;
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.18);
}

div[data-testid="stMetricLabel"] {
    color: #C4B5FD !important;
    font-size: 0.95rem;
}

div[data-testid="stMetricValue"] {
    color: #C4B5FD !important;
    font-weight: 700;
}

/* General text */
p, label, .stMarkdown {
    color: #E9DFFB;
}

/* Dividers */
hr {
    border-color: #493663;
}

/* Buttons */
.stButton > button {
    background: #A78BFA;
    color: #180F2A;
    border: none;
    border-radius: 10px;
    font-weight: 650;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #C4B5FD;
    color: #180F2A;
    border: 1px solid #E879F9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #191226;
    border-right: 1px solid #493663;
}
</style>
""", unsafe_allow_html=True)


total_customers = len(filtered_df)
churned_customers = (filtered_df["Churn"] == "Yes").sum()
churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0
    else 0.0
)

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Churn Share", f"{churn_rate:.2f}%")

st.divider()
st.header("Churn Analysis")

st.subheader("📄 Churn by Contract Type")

if filtered_df.empty:
    st.info(
        " No customers match your selections. "
        "Please select at least one option in the sidebar "
        "to view the contract analysis."
    )

else:
    contract_rates = (
        filtered_df.groupby("Contract")["Churn"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="Churn Rate")
        .sort_values("Churn Rate")
    )

    contract_fig = px.bar(
        contract_rates,
        x="Contract",
        y="Churn Rate",
        text="Churn Rate",
        title="Churn Rate by Contract Type",
        color_discrete_sequence=["#A78BFA"]
    )

    contract_fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Churn rate: %{y:.2f}%"
            "<extra></extra>"
        )
    )

    contract_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#120D1F",
        plot_bgcolor="#211832",
        font=dict(
            color="#E9DFFB",
            family="Arial"
        ),
        title_font=dict(
            color="#F5F0FF",
            size=20
        ),
        margin=dict(l=30, r=35, t=70, b=50),
        xaxis_title="Contract Type",
        yaxis_title="Customers Churned (%)",
        yaxis=dict(
            range=[0, 100],
            ticksuffix="%",
            gridcolor="#493663"
        ),
        xaxis=dict(
            gridcolor="#493663",
            automargin=True
        ),
        showlegend=False
    )

    st.plotly_chart(
        contract_fig,
        use_container_width=True,
        key="contract_churn_chart"
    )

st.subheader("💳 Churn by Payment Method")

if filtered_df.empty:
    st.info("Select some filters to view payment method analysis.")

else:
    payment_rates = (
        filtered_df.groupby("PaymentMethod")["Churn"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="Churn Rate")
        .sort_values("Churn Rate")
    )

    payment_fig = px.bar(
        payment_rates,
        x="Churn Rate",
        y="PaymentMethod",
        orientation="h",
        text="Churn Rate",
        color_discrete_sequence=["#E879F9"],
        title="Churn Rate by Payment Method"
    )

    payment_fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Churn rate: %{x:.2f}%"
            "<extra></extra>"
        )
    )

    payment_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#120D1F",
        plot_bgcolor="#211832",
        font=dict(color="#E9DFFB", family="Arial"),
        title_font=dict(color="#F5F0FF", size=20),
        margin=dict(l=20, r=50, t=70, b=35),
        xaxis_title="Customers Churned (%)",
        yaxis_title="Payment Method",
        xaxis=dict(
            range=[0, 100],
            ticksuffix="%",
            gridcolor="#493663"
        ),
        yaxis=dict(gridcolor="#493663"),
        showlegend=False
    )

    st.plotly_chart(
        payment_fig,
        use_container_width=True,
        key="payment_churn_chart"
    )


st.subheader("📅 Churn by Customer Tenure")

if filtered_df.empty:
    st.info(
        " No customers match your selections. "
        "Select at least one option in the sidebar "
        "to view tenure analysis."
    )

else:
    tenure_df = filtered_df.copy()

    tenure_df["TenureGroup"] = pd.cut(
        tenure_df["tenure"],
        bins=[-1, 12, 24, 48, 60, float("inf")],
        labels=[
            "0-12 months",
            "13-24 months",
            "25-48 months",
            "49-60 months",
            "61+ months"
        ]
    )

    tenure_rates = (
        tenure_df.groupby("TenureGroup", observed=False)["Churn"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="Churn Rate")
    )

    tenure_rates = tenure_rates.dropna(subset=["Churn Rate"])

    group_counts = tenure_df.groupby(
        "TenureGroup", observed=False
    ).size()

    tenure_rates = tenure_rates[
        tenure_rates["TenureGroup"].isin(
            group_counts[group_counts > 0].index
        )
    ]

    if tenure_rates.empty:
        st.info("No tenure groups are available for this selection.")

    else:
        tenure_fig = px.bar(
            tenure_rates,
            x="TenureGroup",
            y="Churn Rate",
            text="Churn Rate",
            title="Churn Rate by Customer Tenure",
            color_discrete_sequence=["#C4B5FD"],
            category_orders={
                "TenureGroup": [
                    "0-12 months",
                    "13-24 months",
                    "25-48 months",
                    "49-60 months",
                    "61+ months"
                ]
            }
        )

        tenure_fig.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Churn rate: %{y:.2f}%"
                "<extra></extra>"
            )
        )

        tenure_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#120D1F",
            plot_bgcolor="#211832",
            font=dict(color="#E9DFFB", family="Arial"),
            title_font=dict(color="#F5F0FF", size=20),
            margin=dict(l=30, r=35, t=70, b=60),
            xaxis_title="Customer Tenure",
            yaxis_title="Customers Churned (%)",
            yaxis=dict(
                range=[0, 100],
                ticksuffix="%",
                gridcolor="#493663"
            ),
            xaxis=dict(
                gridcolor="#493663",
                automargin=True
            ),
            showlegend=False
        )

        st.plotly_chart(
            tenure_fig,
            use_container_width=True,
            key="tenure_churn_chart"
        )


st.subheader("💸 Churn by Monthly Charges")

if filtered_df.empty:
    st.info(
        " No customers match your selections. "
        "Select at least one option in the sidebar "
        "to compare monthly charges."
    )

elif filtered_df["Churn"].nunique() < 2:
    st.info(
        "This selection contains only one churn status. "
        "Select a broader group to compare customers "
        "who stayed and those who churned."
    )

else:
    charges_fig = px.box(
        filtered_df,
        x="Churn",
        y="MonthlyCharges",
        color="Churn",
        title="Monthly Charges by Churn Status",
        category_orders={"Churn": ["No", "Yes"]},
        color_discrete_map={
            "No": "#A78BFA",
            "Yes": "#FB7185"
        },
        points="outliers",
        labels={
            "Churn": "Customer Churned",
            "MonthlyCharges": "Monthly Charges"
        }
    )

    charges_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#120D1F",
        plot_bgcolor="#211832",
        font=dict(color="#E9DFFB", family="Arial"),
        title_font=dict(color="#F5F0FF", size=20),
        margin=dict(l=30, r=30, t=70, b=40),
        xaxis=dict(
            gridcolor="#493663",
            automargin=True
        ),
        yaxis=dict(
            gridcolor="#493663",
            title="Monthly Charges"
        ),
        showlegend=False
    )

    charges_fig.update_traces(
        hovertemplate=(
            "Churn status: %{x}<br>"
            "Monthly charges: %{y:.2f}"
            "<extra></extra>"
        )
    )

    st.plotly_chart(
        charges_fig,
        use_container_width=True,
        key="monthly_charges_chart"
    )
