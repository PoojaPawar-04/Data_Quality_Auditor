import streamlit as st
import pandas as pd
import re

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Data Quality Auditor",
    page_icon="🔍",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 10px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🔍 Data Quality Auditor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Automated data validation, quality scoring, issue detection, and audit reporting using Python and Pandas.</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

st.subheader("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"],
    key="data_upload"
)

if uploaded_file is not None:

    # -----------------------------------------------------
    # READ FILE
    # -----------------------------------------------------

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    st.success(
        f"✅ Successfully uploaded: **{uploaded_file.name}**"
    )

    # -----------------------------------------------------
    # DATASET OVERVIEW
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📊 Dataset Overview</div>',
        unsafe_allow_html=True
    )

    total_rows = len(df)
    total_columns = len(df.columns)
    missing_values = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Rows",
            total_rows
        )

    with col2:
        st.metric(
            "Total Columns",
            total_columns
        )

    with col3:
        st.metric(
            "Missing Values",
            missing_values
        )

    with col4:
        st.metric(
            "Duplicate Rows",
            duplicate_rows
        )

    # -----------------------------------------------------
    # DATA QUALITY AUDIT
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🔎 Data Quality Audit</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "The auditor checks the dataset for common data-quality issues "
        "and classifies them by severity."
    )

    issues = []

    # -----------------------------------------------------
    # MISSING VALUES
    # -----------------------------------------------------

    for column in df.columns:

        missing = int(
            df[column].isnull().sum()
        )

        if missing > 0:

            issues.append({
                "Issue Type": "Missing Values",
                "Column": column,
                "Count": missing,
                "Severity": "High"
            })

    # -----------------------------------------------------
    # DUPLICATE ROWS
    # -----------------------------------------------------

    if duplicate_rows > 0:

        issues.append({
            "Issue Type": "Duplicate Rows",
            "Column": "All Columns",
            "Count": duplicate_rows,
            "Severity": "Medium"
        })

    # -----------------------------------------------------
    # INVALID EMAIL
    # -----------------------------------------------------

    if "Email" in df.columns:

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        invalid_emails = 0

        for email in df["Email"].dropna():

            if not re.match(
                email_pattern,
                str(email)
            ):
                invalid_emails += 1

        if invalid_emails > 0:

            issues.append({
                "Issue Type": "Invalid Email",
                "Column": "Email",
                "Count": invalid_emails,
                "Severity": "High"
            })

    # -----------------------------------------------------
    # NEGATIVE SALES
    # -----------------------------------------------------

    if "Sales" in df.columns:

        negative_sales = int(
            (df["Sales"] < 0).sum()
        )

        if negative_sales > 0:

            issues.append({
                "Issue Type": "Negative Sales",
                "Column": "Sales",
                "Count": negative_sales,
                "Severity": "High"
            })

    # -----------------------------------------------------
    # INVALID STATUS
    # -----------------------------------------------------

    if "Status" in df.columns:

        valid_status = [
            "Completed",
            "Pending",
            "Cancelled"
        ]

        invalid_status = int(
            (~df["Status"].isin(valid_status)).sum()
        )

        if invalid_status > 0:

            issues.append({
                "Issue Type": "Invalid Status",
                "Column": "Status",
                "Count": invalid_status,
                "Severity": "Medium"
            })

    # -----------------------------------------------------
    # INCONSISTENT TEXT VALUES
    # -----------------------------------------------------

    for column in df.select_dtypes(
        include="object"
    ).columns:

        cleaned_values = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
        )

        original_values = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        if len(cleaned_values) > 0:

            value_groups = {}

            for original, cleaned in zip(
                original_values,
                cleaned_values
            ):

                if cleaned not in value_groups:

                    value_groups[cleaned] = set()

                value_groups[cleaned].add(
                    original
                )

            inconsistent_count = 0

            for values in value_groups.values():

                if len(values) > 1:

                    inconsistent_count += len(
                        values
                    )

            if inconsistent_count > 0:

                issues.append({
                    "Issue Type": "Inconsistent Text",
                    "Column": column,
                    "Count": inconsistent_count,
                    "Severity": "Medium"
                })

    # -----------------------------------------------------
    # DATE VALIDATION
    # -----------------------------------------------------

    for column in df.columns:

        if "date" in str(column).lower():

            non_empty_dates = df[column].dropna()

            if len(non_empty_dates) > 0:

                converted_dates = pd.to_datetime(
                    non_empty_dates,
                    errors="coerce"
                )

                invalid_dates = int(
                    converted_dates.isnull().sum()
                )

                if invalid_dates > 0:

                    issues.append({
                        "Issue Type": "Invalid Dates",
                        "Column": column,
                        "Count": invalid_dates,
                        "Severity": "High"
                    })

    # -----------------------------------------------------
    # OUTLIER DETECTION
    # -----------------------------------------------------

    for column in df.select_dtypes(
        include="number"
    ).columns:

        numeric_data = df[column].dropna()

        if len(numeric_data) >= 4:

            Q1 = numeric_data.quantile(0.25)
            Q3 = numeric_data.quantile(0.75)

            IQR = Q3 - Q1

            lower_limit = Q1 - (
                1.5 * IQR
            )

            upper_limit = Q3 + (
                1.5 * IQR
            )

            outliers = numeric_data[
                (numeric_data < lower_limit)
                |
                (numeric_data > upper_limit)
            ]

            outlier_count = int(
                len(outliers)
            )

            if outlier_count > 0:

                issues.append({
                    "Issue Type": "Outliers",
                    "Column": column,
                    "Count": outlier_count,
                    "Severity": "Medium"
                })

    # -----------------------------------------------------
    # AUDIT RESULTS
    # -----------------------------------------------------

    if issues:

        audit_df = pd.DataFrame(
            issues
        )

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # SEVERITY SUMMARY
        # -------------------------------------------------

        st.subheader("🚦 Issue Severity")

        severity_summary = (
            audit_df
            .groupby("Severity")["Count"]
            .sum()
            .reindex(
                ["High", "Medium", "Low"],
                fill_value=0
            )
        )

        severity_col1, severity_col2, severity_col3 = st.columns(3)

        with severity_col1:

            st.metric(
                "🔴 High",
                int(
                    severity_summary["High"]
                )
            )

        with severity_col2:

            st.metric(
                "🟠 Medium",
                int(
                    severity_summary["Medium"]
                )
            )

        with severity_col3:

            st.metric(
                "🟢 Low",
                int(
                    severity_summary["Low"]
                )
            )

        st.bar_chart(
            severity_summary
        )

        # -------------------------------------------------
        # ISSUE SUMMARY
        # -------------------------------------------------

        st.subheader("📊 Issue Summary")

        issue_summary = (
            audit_df
            .groupby("Issue Type")["Count"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            issue_summary
        )

        # -------------------------------------------------
        # CLEANING RECOMMENDATIONS
        # -------------------------------------------------

        st.subheader(
            "🧹 Cleaning Recommendations"
        )

        recommendations = {

            "Missing Values":
                "Review missing values and fill them with appropriate information where possible.",

            "Duplicate Rows":
                "Review duplicate records and remove them if they represent repeated entries.",

            "Invalid Email":
                "Correct email addresses that do not follow a valid email format.",

            "Negative Sales":
                "Verify negative sales values and correct them if they are data-entry errors.",

            "Invalid Status":
                "Replace invalid status values with Completed, Pending, or Cancelled.",

            "Inconsistent Text":
                "Standardize capitalization, spacing, and text values.",

            "Invalid Dates":
                "Review invalid date values and convert them to a consistent date format.",

            "Outliers":
                "Review unusually high or low numeric values and verify whether they are genuine observations."
        }

        for issue_type in audit_df[
            "Issue Type"
        ].unique():

            if issue_type in recommendations:

                st.warning(
                    f"⚠️ {issue_type}: "
                    f"{recommendations[issue_type]}"
                )

        # -------------------------------------------------
        # DOWNLOAD REPORT
        # -------------------------------------------------

        st.subheader(
            "📥 Download Audit Report"
        )

        report_csv = audit_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Audit Report",
            data=report_csv,
            file_name="data_quality_audit_report.csv",
            mime="text/csv"
        )

    else:

        st.success(
            "🎉 No major data-quality issues detected!"
        )

    # -----------------------------------------------------
    # DATA QUALITY SCORE
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📈 Data Quality Score</div>',
        unsafe_allow_html=True
    )

    total_issues = sum(
        issue["Count"]
        for issue in issues
    )

    if total_rows > 0:

        issue_rate = (
            total_issues /
            total_rows
        )

        score = max(
            0,
            100 -
            (issue_rate * 100)
        )

    else:

        score = 100

    if score >= 90:

        score_status = "Excellent"

    elif score >= 75:

        score_status = "Good"

    elif score >= 50:

        score_status = "Needs Improvement"

    else:

        score_status = "Poor"

    score_col1, score_col2 = st.columns(2)

    with score_col1:

        st.metric(
            "Overall Data Quality Score",
            f"{score:.2f}%"
        )

    with score_col2:

        st.metric(
            "Quality Status",
            score_status
        )

    st.progress(
        int(score)
    )

    # -----------------------------------------------------
    # COLUMN QUALITY REPORT
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Column Quality Report</div>',
        unsafe_allow_html=True
    )

    column_report = []

    for column in df.columns:

        total = len(df)

        missing = int(
            df[column].isnull().sum()
        )

        unique = int(
            df[column].nunique()
        )

        if total > 0:

            completeness = (
                (total - missing) /
                total
            ) * 100

        else:

            completeness = 100

        column_report.append({

            "Column": column,

            "Data Type": str(
                df[column].dtype
            ),

            "Missing Values": missing,

            "Unique Values": unique,

            "Completeness (%)": round(
                completeness,
                2
            )
        })

    column_report_df = pd.DataFrame(
        column_report
    )

    st.dataframe(
        column_report_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # MISSING VALUE CHART
    # -----------------------------------------------------

    st.subheader(
        "📊 Missing Values by Column"
    )

    missing_by_column = df.isnull().sum()

    missing_by_column = (
        missing_by_column[
            missing_by_column > 0
        ]
    )

    if len(missing_by_column) > 0:

        st.bar_chart(
            missing_by_column
        )

    else:

        st.success(
            "🎉 No missing values found!"
        )

    # -----------------------------------------------------
    # DATASET PREVIEW
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📋 Dataset Preview</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Preview of the uploaded dataset."
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Data Quality Auditor | Built with Python, Pandas and Streamlit"
)