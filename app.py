import streamlit as st
import pandas as pd
import io
import numpy as np

st.title("CSV Converter & Transformer App")
st.write("Upload a CSV file, transform data, and convert it to different formats")

st.write("### Try with Sample Data")
if st.button("Load Sample Employee Data"):
    sample_df = pd.read_csv("sample_data.csv")
    st.session_state.df = sample_df

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")

if 'df' in st.session_state:
    df = st.session_state.df
    
    st.write("### File Preview")
    st.dataframe(df.head())
    
    st.write(f"**Rows:** {len(df)}")
    st.write(f"**Columns:** {len(df.columns)}")
    
    st.write("### Data Transformations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Column Operations**")
        if st.checkbox("Convert text to uppercase"):
            text_cols = df.select_dtypes(include=['object']).columns
            if len(text_cols) > 0:
                selected_col = st.selectbox("Select column:", text_cols)
                if selected_col:
                    df[selected_col] = df[selected_col].astype(str).str.upper()
        
        if st.checkbox("Add salary bonus (10%)"):
            if 'salary' in df.columns:
                df['salary_with_bonus'] = df['salary'] * 1.1
        
        if st.checkbox("Calculate years of service"):
            if 'join_date' in df.columns:
                df['join_date'] = pd.to_datetime(df['join_date'])
                df['years_of_service'] = (pd.Timestamp.now() - df['join_date']).dt.days / 365.25
                df['years_of_service'] = df['years_of_service'].round(1)
    
    with col2:
        st.write("**Filtering Options**")
        
        if st.checkbox("Filter by department"):
            if 'department' in df.columns:
                departments = df['department'].unique()
                selected_dept = st.selectbox("Select department:", departments)
                df = df[df['department'] == selected_dept]
        
        if st.checkbox("Filter by age range"):
            if 'age' in df.columns:
                min_age, max_age = st.slider("Age range:", 
                                           int(df['age'].min()), 
                                           int(df['age'].max()), 
                                           (int(df['age'].min()), int(df['age'].max())))
                df = df[(df['age'] >= min_age) & (df['age'] <= max_age)]
        
        if st.checkbox("Sort by column"):
            sort_col = st.selectbox("Sort by:", df.columns)
            sort_order = st.radio("Order:", ["Ascending", "Descending"])
            ascending = sort_order == "Ascending"
            df = df.sort_values(by=sort_col, ascending=ascending)
    
    st.write("### Transformed Data Preview")
    st.dataframe(df)
    
    st.write("### Download Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="transformed_file.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="Download as Excel",
            data=excel_data,
            file_name="transformed_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        json_str = df.to_json(orient='records', indent=2)
        st.download_button(
            label="Download as JSON",
            data=json_str,
            file_name="transformed_file.json",
            mime="application/json"
        )
    
    st.write("### Data Summary")
    st.write(df.describe())

else:
    st.info("Please upload a CSV file or click 'Load Sample Employee Data' to get started.")