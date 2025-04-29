import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Page Configuration
st.set_page_config(
    page_title="Advanced Data Analysis Suite",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #1a1a1a}
    h1 {color: #4a8fe7}
    h2 {color: #c94c4c}
    .st-bw {background-color: #2d2d2d}
    .st-cb {color: white !important}
    .css-18e3th9 {padding: 2rem 5rem}
</style>
""", unsafe_allow_html=True)

# App Header
st.title("📊 Advanced Data Analysis Suite")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration Panel")
    uploaded_file = st.file_uploader("Upload Dataset", type=["csv", "xlsx"])
    analysis_mode = st.selectbox("Select Analysis Mode", 
                               ["Quick Scan", "Deep Dive Analysis"])
    st.markdown("---")
    st.markdown("**Advanced Options**")
    sample_size = st.slider("Sample Size (%)", 1, 100, 100)
    corr_threshold = st.slider("Correlation Threshold", 0.0, 1.0, 0.7)
    st.markdown("---")
    st.info("Made with ❤️ by Data Science Pro")

# Data Loading
@st.cache_data(ttl=3600)
def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    return None

# Main App Logic
if uploaded_file is not None:
    with st.spinner('Crunching your data...'):
        time.sleep(1)
        df = load_data(uploaded_file)
        
        if sample_size < 100:
            df = df.sample(frac=sample_size/100)
        
        # Data Preview Section
        st.header("🔍 Data Preview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Total Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        
        st.dataframe(df.head(10), use_container_width=True)
        
        # Advanced Analysis Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Profiling Report", 
            "📊 Interactive Visualizations",
            "🤖 AutoML",
            "🔧 Data Wrangling"
        ])

        with tab1:
            st.header("Automated EDA Report")
            profile = ProfileReport(df, explorative=True)
            st_profile_report(profile)

        with tab2:
            st.header("Interactive Data Visualizations")
            col1, col2 = st.columns(2)
            
            with col1:
                x_axis = st.selectbox("X-Axis", df.columns)
                y_axis = st.selectbox("Y-Axis", df.columns)
                color_by = st.selectbox("Color By", [None] + list(df.columns))
                
                plot_type = st.selectbox("Select Visualization Type", [
                    "Scatter Plot", 
                    "Histogram", 
                    "Box Plot",
                    "Violin Plot",
                    "3D Scatter"
                ])
            
            with col2:
                if plot_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by)
                    st.plotly_chart(fig, use_container_width=True)
                elif plot_type == "Histogram":
                    fig = px.histogram(df, x=x_axis, color=color_by)
                    st.plotly_chart(fig)
                elif plot_type == "Box Plot":
                    fig = px.box(df, x=x_axis, y=y_axis, color=color_by)
                    st.plotly_chart(fig)
                elif plot_type == "Violin Plot":
                    fig = px.violin(df, x=x_axis, y=y_axis, color=color_by)
                    st.plotly_chart(fig)
                elif plot_type == "3D Scatter":
                    z_axis = st.selectbox("Z-Axis", df.columns)
                    fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, color=color_by)
                    st.plotly_chart(fig)

        with tab3:
            st.header("Automated Machine Learning")
            target = st.selectbox("Select Target Variable", df.columns)
            
            if st.button("Train Predictive Model"):
                X = df.drop(columns=[target])
                y = df[target]
                
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42)
                
                model = RandomForestRegressor(n_estimators=100)
                model.fit(X_train, y_train)
                predictions = model.predict(X_test)
                
                st.subheader("Model Performance")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("R² Score", round(r2_score(y_test, predictions), 2))
                with col2:
                    st.metric("RMSE", round(np.sqrt(mean_squared_error(y_test, predictions)), 2))
                
                fig = px.scatter(x=y_test, y=predictions, 
                               labels={'x': 'Actual', 'y': 'Predicted'})
                st.plotly_chart(fig)

        with tab4:
            st.header("Data Wrangling Tools")
            wrangle_option = st.selectbox("Select Operation", [
                "Handle Missing Values",
                "Filter Data",
                "Feature Engineering",
                "Encode Categorical Variables"
            ])
            
            if wrangle_option == "Handle Missing Values":
                st.subheader("Missing Value Treatment")
                strategy = st.radio("Select Strategy", [
                    "Drop Missing Values",
                    "Fill with Mean/Median",
                    "Interpolation"
                ])
                
                if st.button("Apply Treatment"):
                    if strategy == "Drop Missing Values":
                        df = df.dropna()
                    elif strategy == "Fill with Mean/Median":
                        for col in df.columns:
                            if df[col].dtype in ['int64', 'float64']:
                                fill_value = df[col].mean() if df[col].skew() < 0.5 else df[col].median()
                                df[col].fillna(fill_value, inplace=True)
                    elif strategy == "Interpolation":
                        df = df.interpolate()
                    st.success("Missing values treatment applied!")

            elif wrangle_option == "Filter Data":
                st.subheader("Data Filtering")
                filter_column = st.selectbox("Select Column to Filter", df.columns)
                min_val, max_val = st.slider("Select Value Range", 
                    float(df[filter_column].min()), 
                    float(df[filter_column].max()), 
                    (float(df[filter_column].min()), float(df[filter_column].max())))
                df = df[(df[filter_column] >= min_val) & (df[filter_column] <= max_val)]
                st.success(f"Data filtered to {len(df)} records!")

else:
    st.info("👋 Upload a dataset to get started!")
    if st.button("Load Sample Dataset"):
        df = pd.DataFrame(np.random.randn(500, 5), columns=list('ABCDE'))
        df['Category'] = np.random.choice(['X', 'Y', 'Z'], 500)
        st.session_state.df = df
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
    ### 🛠️ Features Overview
    - **Automated EDA Report**: Comprehensive data profiling
    - **Interactive Visualizations**: Dynamic, publication-quality charts
    - **Predictive Modeling**: AutoML with performance metrics
    - **Data Wrangling**: Clean and preprocess data directly in-app
    - **Custom Analysis**: Save and export your workflows
""")