import streamlit as st
import pandas as pd
from sklearn.impute import SimpleImputer

st.set_page_config(page_title="Data Cleaning App", layout="wide")

st.title('🧹 Data Cleaning App')

uploaded_file = st.file_uploader('Upload your CSV file', type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader('📊 Raw Data Preview')
    st.dataframe(df.head())

    st.subheader('📌 Data Summary before Cleaning')

    st.write("Total Records:", len(df))
    st.write("Total Columns:", len(df.columns))
    st.write("Missing Values:", df.isnull().sum().sum())
    st.write("Missing Values per Column:")
    st.dataframe(df.isnull().sum())

    if st.button('🚀 Clean Data'):
        df_clean = df.copy()

        # Separate columns
        num_cols = df_clean.select_dtypes(include=['float64', 'int64']).columns
        cat_cols = df_clean.select_dtypes(include=['object']).columns

        # Impute numeric
        if len(num_cols) > 0:
            num_imputer = SimpleImputer(strategy='mean')
            df_clean[num_cols] = num_imputer.fit_transform(df_clean[num_cols])

        # Impute categorical
        if len(cat_cols) > 0:
            cat_imputer = SimpleImputer(strategy='most_frequent')
            df_clean[cat_cols] = cat_imputer.fit_transform(df_clean[cat_cols])

        st.subheader('✅ Cleaned Data Preview')
        st.dataframe(df_clean.head())

        st.subheader('📌 Data Summary after Cleaning')

        st.write("Missing Values:", df_clean.isnull().sum().sum())
        st.dataframe(df_clean.isnull().sum())

        # Download button
        csv = df_clean.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Cleaned Data",
            data=csv,
            file_name='cleaned_data.csv',
            mime='text/csv'
        )
