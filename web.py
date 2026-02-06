import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Professional Data Dashboard",
    layout="wide"
)

st.title("📊 Professional Data Analytics Dashboard")

# -----------------------
# Sidebar
# -----------------------
st.sidebar.header("Dashboard Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("sample_data.csv")

# -----------------------
# Data Cleaning
# -----------------------
df = df.fillna(df.mean(numeric_only=True))
df.drop_duplicates(inplace=True)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.subheader("Filters")

for column in df.select_dtypes(include="object").columns:
    selected = st.sidebar.multiselect(
        f"Filter {column}",
        df[column].unique(),
        default=df[column].unique()
    )
    df = df[df[column].isin(selected)]

# -----------------------
# KPI Section
# -----------------------
st.subheader("Key Metrics")

numeric_cols = df.select_dtypes(include=np.number).columns

col1, col2, col3 = st.columns(3)

if len(numeric_cols) > 0:
    metric_col = numeric_cols[0]

    col1.metric(
        "Total Records",
        len(df)
    )

    col2.metric(
        f"Average {metric_col}",
        round(df[metric_col].mean(), 2)
    )

    col3.metric(
        f"Max {metric_col}",
        df[metric_col].max()
    )

# -----------------------
# Charts Section
# -----------------------
st.subheader("Interactive Visualizations")

chart_type = st.selectbox(
    "Select Chart Type",
    ["Bar Chart", "Scatter Plot", "Histogram", "Box Plot"]
)

num_cols = df.select_dtypes(include=np.number).columns
cat_cols = df.select_dtypes(include="object").columns

if chart_type == "Bar Chart" and len(cat_cols) > 0:
    x = st.selectbox("Category", cat_cols)
    y = st.selectbox("Value", num_cols)
    fig = px.bar(df, x=x, y=y, color=x, title="Bar Chart")

elif chart_type == "Scatter Plot":
    x = st.selectbox("X Axis", num_cols)
    y = st.selectbox("Y Axis", num_cols, index=1 if len(num_cols) > 1 else 0)
    fig = px.scatter(df, x=x, y=y, title="Scatter Plot")

elif chart_type == "Histogram":
    x = st.selectbox("Column", num_cols)
    fig = px.histogram(df, x=x, title="Histogram")

elif chart_type == "Box Plot":
    x = st.selectbox("Column", num_cols)
    fig = px.box(df, y=x, title="Box Plot")

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# Data Table Section
# -----------------------
st.subheader("Filtered Data")

st.dataframe(df, use_container_width=True)

# -----------------------
# Export Option
# -----------------------
st.subheader("Export Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Cleaned Data",
    data=csv,
    file_name="cleaned_data.csv",
    mime="text/csv"
)
