# 📊 Customer Churn & Retention Analytics

**An end-to-end data analytics project using Python, SQL, SQLite, and Streamlit to explore customer churn patterns and identify opportunities for customer retention.**

## 📌 Project Overview

Customer churn occurs when customers stop using a company's products or services. For subscription-based businesses, understanding churn is essential for identifying at-risk customer segments, improving customer experience, and developing effective retention strategies.

This project analyzes customer data from a telecommunications dataset to investigate how churn is associated with contract types, customer tenure, payment methods, monthly charges, and customer characteristics.

The project combines data cleaning, SQL-based analysis, data visualization, and an interactive dashboard to turn raw customer records into actionable business insights.

## 🎯 Project Objectives

- Clean and validate customer data using Python and pandas.
- Store and analyze structured customer data using SQLite and SQL.
- Identify customer segments with comparatively high churn.
- Investigate relationships between churn, contract types, tenure, and billing.
- Build an interactive dashboard using Streamlit and Plotly.
- Translate analytical findings into potential customer-retention recommendations.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| pandas | Data cleaning and manipulation |
| SQL | Customer segmentation and churn analysis |
| SQLite | Relational database storage |
| Streamlit | Interactive dashboard development |
| Plotly | Interactive data visualization |
| Git & GitHub | Version control and project hosting |

## 📂 Project Structure

```text
customer-churn-analytics/
│
├── data/
│   ├── raw/                         # Original dataset
│   └── processed/
│       ├── telco_churn_cleaned.csv  # Cleaned customer data
│       └── churn.db                 # SQLite database
│
├── notebooks/                       # Exploratory analysis notebooks
│
├── sql/
│   └── analysis.sql        # SQL analysis and validation
│
├── src/
│   ├── import_to_sqlite.py          # Loads CSV data into SQLite
│   └── run_sql.py                   # Executes SQL queries
│
├── dashboard/
│   └── app.py                       # Streamlit dashboard
│
├── reports/
│   └── initial_findings.md          # Findings and data-quality notes
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 📊 Dataset

The project uses the IBM Telco Customer Churn dataset, which contains customer information, service subscriptions, billing details, contract information, tenure, and churn status.

- **Total customer records:** 7,043
- **Number of columns:** 21
- **Target variable:** `Churn`
- **Churn categories:** `Yes` and `No`

### Key Features

| Feature | Description |
|---|---|
| `customerID` | Unique customer identifier |
| `gender` | Customer gender |
| `SeniorCitizen` | Indicates whether the customer is a senior citizen |
| `Partner` | Indicates whether the customer has a partner |
| `Dependents` | Indicates whether the customer has dependents |
| `tenure` | Number of months the customer has stayed |
| `Contract` | Customer contract type |
| `PaymentMethod` | Customer payment method |
| `MonthlyCharges` | Monthly amount charged |
| `TotalCharges` | Total amount charged over the customer relationship |
| `Churn` | Whether the customer left the service |

The dataset also includes information about internet services, phone services, and optional service subscriptions.

## 🧹 Data Cleaning and Validation

The data preparation process included:

- Converting `TotalCharges` to a numeric data type.
- Identifying missing values and examining their relationship with customer tenure.
- Checking for duplicate customer records and duplicate identifiers.
- Validating churn labels and numeric ranges.
- Checking for negative tenure and charges, as well as tenure values exceeding 72 months.
- Exporting the cleaned dataset for SQL analysis and dashboard development.

### Data Quality Findings

- All 7,043 customer IDs are unique.
- No customer IDs or churn labels are missing.
- No negative tenure values or charges were identified.
- No tenure values exceed 72 months.
- Eleven records have missing `TotalCharges` values. All eleven correspond to customers with zero months of tenure.

The missing total-charge values were retained rather than automatically replaced with zero, avoiding an unsupported assumption about the underlying billing data.

## 🔍 SQL Analysis

The cleaned dataset was imported into a SQLite database to support structured querying and customer segmentation.

The SQL analysis covers:

1. **Overall churn:** Customer counts, retained customers, churned customers, and overall churn share.
2. **Contract analysis:** Comparing churn across month-to-month, one-year, and two-year contracts.
3. **Payment analysis:** Examining churn across different payment methods.
4. **Customer segmentation:** Comparing churn across senior-citizen, partner, and dependent groups.
5. **Tenure analysis:** Grouping customers by tenure to investigate how churn varies over time.
6. **Billing analysis:** Comparing churn between customers with above-average and at-or-below-average monthly charges.
7. **Combined segmentation:** Investigating churn across contract and tenure groups.
8. **Advanced SQL:** Applying common table expressions (CTEs), aggregate functions, conditional logic, and window functions.
9. **Data-quality checks:** Validating identifiers, missing values, churn labels, and numeric constraints.

## 📈 Key Findings

The analysis identified several notable patterns in the dataset.

### 1. Month-to-month customers have higher churn

| Contract type | Churn percentage |
|---|---:|
| Month-to-month | 42.7% |
| One year | 11.3% |
| Two year | 2.8% |

Customers on month-to-month contracts have substantially higher observed churn than customers on longer-term contracts.

**Business implication:** Consider testing retention incentives, clearer renewal communication, or suitable longer-term plans for month-to-month customers. These patterns alone do not establish that changing contract type will cause churn to decrease.

### 2. Churn is concentrated among newer customers

| Customer tenure | Churn percentage |
|---|---:|
| 0–12 months | 47.44% |
| 13–24 months | 28.71% |
| 25–48 months | 20.39% |
| 49–72 months | 9.51% |

The highest observed churn occurs among customers in their first 12 months.

**Business implication:** An improved onboarding experience, early customer support, and proactive engagement may be worthwhile areas to investigate.

### 3. Payment method is associated with churn

Electronic check users have an observed churn percentage of approximately 45%, compared with lower percentages among customers using other payment methods.

**Business implication:** Investigate whether payment experience, customer preferences, billing friction, or differences in customer composition help explain this pattern before recommending changes.

### 4. Senior citizens have higher observed churn

| Customer group | Churn percentage |
|---|---:|
| Senior citizens | 41.68% |
| Non-senior citizens | 23.61% |

This difference identifies a segment worth examining further. It does not explain why the difference exists.

### 5. Higher monthly charges are associated with higher churn

| Monthly charge segment | Churn percentage |
|---|---:|
| Above average | 34.54% |
| At or below average | 16.47% |

Customers whose monthly charges exceed the dataset-wide average of approximately $64.76 have higher observed churn.

**Business implication:** Further analysis could examine service bundles, perceived value, pricing, and contract types to understand whether these factors contribute to the association.

### 6. Contract type and tenure together reveal important segments

Among month-to-month customers with 0–12 months of tenure, the observed churn percentage is **51.35%**, compared with an overall churn share of approximately **26.54%**.

This segment may be a useful starting point for investigating early customer-retention opportunities.

*Percentages are based on the supplied dataset and may vary slightly with rounding.*

## 📊 Interactive Dashboard

The Streamlit dashboard allows users to explore churn patterns interactively.

### Dashboard Features

- KPI cards showing customer count, churned customers, and churn share.
- Contract-type filtering.
- Payment-method filtering.
- Customer-tenure range filtering.
- Monthly-charge range filtering.
- Interactive visualizations for contract, payment, tenure, and monthly-charge patterns.
- Dynamic chart updates based on selected filters.
- Empty-state handling when filters return no matching records.

The dashboard uses a dark purple visual theme with lavender and orchid accents.

### Run the Dashboard

From the project root, activate the virtual environment and run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run dashboard/app.py
```

Streamlit will provide a local URL to open the dashboard in your browser.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11 or compatible version
- Git
- A code editor such as VS Code or Google Antigravity

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd customer-churn-analytics
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Prepare the data

Place the original dataset in `data/raw/` and run the cleaning workflow used to generate:

```text
data/processed/telco_churn_cleaned.csv
```

The cleaned CSV is required by the dashboard and SQLite import script.

### 5. Create or refresh the SQLite database

```bash
python src/import_to_sqlite.py
```

### 6. Execute the SQL analysis

```bash
python src/run_sql.py
```

### 7. Launch the dashboard

```bash
python -m streamlit run dashboard/app.py
```

**Note:** These instructions assume the dataset and cleaned CSV are available locally. Check the repository's data availability and licensing requirements before publishing or sharing the dataset.

## 💡 Business Recommendations

Based on the observed patterns, the following are potential areas for further investigation:

- **Improve early customer engagement:** Examine onboarding and support experiences for customers in their first year.
- **Investigate contract-related churn:** Explore why month-to-month customers leave more frequently and test appropriate retention approaches.
- **Review billing experience:** Investigate payment-method differences and possible payment friction.
- **Understand perceived value:** Study whether service combinations, monthly charges, and contract type help explain customer departures.
- **Evaluate retention interventions:** Track future churn outcomes to determine whether proposed actions actually improve retention.

These recommendations are hypotheses to investigate, not proven causal conclusions.

## ⚠️ Limitations

- The analysis is based on a snapshot of customer data rather than a longitudinal experiment.
- Associations between customer characteristics and churn do not establish causation.
- The analysis does not establish the profitability or cost-effectiveness of potential retention campaigns.
- Missing `TotalCharges` values for zero-tenure customers are retained as missing.
- The dashboard is descriptive and does not currently predict which individual customers will churn.
- Results may not generalize to other telecom companies, markets, or time periods.

## 🚀 Future Improvements

Potential extensions include:

- Developing a reproducible data-cleaning pipeline.
- Adding more exploratory visualizations and customer segments.
- Automating database refreshes.
- Building a churn-prediction model and evaluating it using appropriate metrics.
- Comparing classification models and explaining their predictions.
- Adding tests for data validation and SQL logic.
- Deploying the dashboard and documenting a reproducible online demo.

## 📚 Skills Demonstrated

- Data cleaning and preprocessing
- Exploratory data analysis
- SQL querying and customer segmentation
- Aggregations, CTEs, and window functions
- SQLite database management
- Interactive data visualization
- Dashboard development
- Data-quality validation
- Business insight communication
- Project documentation

## 👩‍💻 Author

Developed as a portfolio project to strengthen practical skills in data analytics, SQL, Python, and interactive application development.

---

*This project is intended for educational and portfolio purposes. Findings are descriptive and should be validated with additional data before making business decisions.*
