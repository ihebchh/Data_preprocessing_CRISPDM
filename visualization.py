import streamlit as st
import pandas as pd
import plotly.express as px
import time
import numpy as np
from io import StringIO
from sklearn.model_selection import train_test_split
from streamlit_elements import elements, mui, html
import seaborn as sns
import matplotlib.pyplot as plt

# Add custom CSS to style the image as a cover
st.set_page_config(layout="wide")
st.image("capture1.PNG", use_container_width=True)

# Add custom CSS for background styling
st.markdown(
    """
    <style>
    /* Set the background image with a clean and subtle effect */
    .stApp {
        background-image: url('cover1.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-color: rgb(255, 255, 255); /* Add a semi-transparent overlay */
        background-blend-mode: overlay;
        font-family: 'Arial', sans-serif; /* Use a professional font */
    }

    /* Title styling for the dashboard */
    .title {
        text-align: center;
        color: #ffffff;
        margin-top: 20vh;
        font-size: 3.5rem;
        font-weight: bold;
        text-shadow: 3px 3px 12px rgba(0, 0, 0, 0.7); /* Enhanced shadow */
        letter-spacing: 1.5px;
    }

    /* Style for the main content area */
    .main-content {
        background: rgba(255, 255, 255, 0.9); /* White with slight transparency */
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2); /* Add a soft shadow */
        padding: 20px;
        margin: 20px auto;
        width: 85%; /* Center content area */
    }

    /* Add custom styling for metrics or cards */
    .metric {
        text-align: center;
        font-size: 1.2rem;
        color: #0366fc;
        font-weight: 600;
        margin: 10px 0;
    }

    .metric-title {
        color: #333;
        font-weight: bold;
    }

    /* Buttons style */
    .btn-primary {
        background-color: #0366fc;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .btn-primary:hover {
        background-color:rgb(2, 73, 179);
    }
</style>
    """,
    unsafe_allow_html=True,
)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "⚙️ Data Processing"])

if page == "🏠 Home":
    st.title("Welcome to CRISP-DM App! 🚀")
    #st.image("cover1.jpg", use_container_width=True)
    st.markdown("""
        **CRISP-DM App** is designed to help you preprocess, clean, and analyze your datasets efficiently.
        - 📊 **Upload your dataset** and explore its structure.
        - 🔍 **Detect and fix issues** in your data.
        - 📈 **Visualize and analyze** data trends interactively.
        
        Navigate to the **Processing Page** from the sidebar to start working on your dataset.
    """)
elif page == "⚙️ Data Processing":
    
# Add a title over the background image
    st.markdown('<h1 class="title">💡Data Preprocessing💡</h1>', unsafe_allow_html=True)

    @st.cache_data
    def load_data(file):
        return pd.read_csv(file)

    file = st.file_uploader("Upload your Database File", type=['csv'])

    if file is not None:
        df = load_data(file)

        n_rows = st.slider("Choose number of rows", min_value=5, max_value=len(df), step=1)
        columns_to_show = st.multiselect("Select columns to show", df.columns.to_list(), default=df.columns.to_list())
        
        # Initial column list
        numerical_columns = df.select_dtypes(include=np.number).columns.to_list()

        st.write(df[:n_rows][columns_to_show])

        # Création des onglets
        tab1, tab2, tab3, tab4 = st.tabs(["Check for Missing Values", "Statistics of Numeric Columns", "Dataset Summary", "INFO"])

        with tab1:
            st.write("Missing Values", df.notnull().sum())
        with tab2:
            st.write("Statistics", df.describe())
        with tab3:
            st.write("Summary", df.head())
        with tab4:
            st.write("Info", df.info())

        # Gestion des colonnes avec des valeurs manquantes
        with st.container():
            st.write("### 🔍 Columns with Missing Values")

    # You can call any Streamlit command, including custom components:
            #columns_with_na = [col for col in df.columns if df[col].isnull().sum() > 0]
            #non_numeric_cols = df.select_dtypes(exclude=['number']).columns.tolist()
            #st.write("NaN cols",columns_with_na)
            if st.button("🔍 Show Columns with Missing Values"):
                missing_cols = [col for col in df.columns if df[col].isnull().sum() > 0]
        
                if missing_cols:
                    #st.write("### Columns with Missing Values:")
                    st.write(missing_cols)
                    for col in missing_cols:
                        st.write(f"**Column: `{col}`** (Missing: {df[col].isnull().sum()} values)")
                        
                        # User selects how to handle missing values
                        choice = st.radio(
                            f"How do you want to handle `{col}`?",
                            ["Mean", "Median", "Drop Rows", "Replace with Custom Value"],
                            key=col
                        )
                        if choice == "Replace with Custom Value":
                            custom_value = st.text_input(f"Enter a value for `{col}`:", key=f"custom_{col}")
                        
                        # Apply transformation when the button is clicked
                        if st.button(f"Apply to `{col}`", key=f"apply_{col}"):
                            if choice == "Mean":
                                df[col].fillna(df[col].mean(), inplace=True)
                            elif choice == "Median":
                                df[col].fillna(df[col].median(), inplace=True)
                            elif choice == "Drop Rows":
                                df.dropna(subset=[col], inplace=True)
                            elif choice == "Replace with Custom Value":
                                if custom_value != "":
                                    df[col].fillna(custom_value, inplace=True)
                                else:
                                    st.warning(f"⚠️ Please enter a custom value for `{col}`")

                    st.success(f"✅ `{col}` processed successfully!")










                else:
                    st.success("No missing values found!")
            
            
        
       ###################################################""
        
       #################################################

        

        # Visualisation des graphiques avec les nouvelles données
        tab3, tab4 = st.tabs(["Scatter Plots", "Histogram"])
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                x_column = st.selectbox('Select Column on X axe', numerical_columns)
            with col2:
                y_column = st.selectbox('Select Column on Y axe', numerical_columns)

            fig_scatter = px.scatter(df, x=x_column, y=y_column)
            with st.spinner("In Progress"):
                st.plotly_chart(fig_scatter)

        with tab4:
            histogram_feature = st.selectbox('Select a feature to histogram', numerical_columns)
            fig_hist = px.histogram(df, x=histogram_feature)
            st.plotly_chart(fig_hist)
        tab5, tab6 = st.tabs(["Correlation Heatmap", "Pairplot"])

        with tab5:
            st.write("### 🔗 Correlation Matrix Heatmap")

            # Select only numeric columns for correlation calculation
            numeric_df = df.select_dtypes(include=[np.number])

            if not numeric_df.empty:
                corr_matrix = numeric_df.corr()

                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax)
                st.pyplot(fig)
            else:
                st.warning("⚠️ No numeric columns available for correlation analysis.")

        with tab6:
            st.write("### 🔗 Pairplot Analysis")
            st.write("This helps visualize scatter plots for multiple numerical columns.")

            selected_columns = st.multiselect("Select Columns for Pairplot", numerical_columns, default=numerical_columns[:3])

            if selected_columns:
                pairplot_fig = sns.pairplot(df[selected_columns])
                st.pyplot(pairplot_fig.fig)
            else:
                st.warning("⚠️ Please select at least one column to generate the pairplot.")

