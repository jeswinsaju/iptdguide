import streamlit as st
import pandas as pd

# Page setup optimized for mobile
st.set_page_config(
    page_title="Bender-Gestalt Guide",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Bender-Gestalt Guide")
st.caption("Digitized Reference Manual — Part I: Arrangement")
st.markdown("---")

# Load data from Excel
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data.xlsx")
        # Clean up columns
        df.columns = [col.strip().capitalize() for col in df.columns]
        return df
    except Exception as e:
        st.error("Could not load data.xlsx. Please ensure the file exists.")
        return pd.DataFrame(columns=["Sign", "Meaning"])

df = load_data()

if not df.empty:
    # Mobile-friendly search box
    search_query = st.text_input(
        "🔍 Search Sign or Meaning:", 
        placeholder="Type to filter..."
    ).strip().lower()

    # Filter data based on search
    if search_query:
        filtered_df = df[
            df['Sign'].astype(str).str.lower().str.contains(search_query) | 
            df['Meaning'].astype(str).str.lower().str.contains(search_query)
        ]
    else:
        filtered_df = df

    # Dropdown selector for matching terms
    if not filtered_df.empty:
        sign_list = filtered_df['Sign'].tolist()
        selected_sign = st.selectbox(
            f"Select from matches ({len(sign_list)} found):", 
            options=sign_list
        )
        
        # Displaying the result beautifully on mobile
        meaning = df[df['Sign'] == selected_sign]['Meaning'].values[0]
        st.info(f"### **{selected_sign}**")
        st.write(meaning)
    else:
        st.warning("No matches found. Try another term.")
else:
    st.info("Please add data to your data.xlsx file to get started.")