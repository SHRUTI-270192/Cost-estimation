import streamlit as st
import pandas as pd
import os

# Title of the app
st.title("Budgetary Offer Processing App")

# Step 1: File Upload Section
st.header("Upload Budgetary Offers")
uploaded_files = st.file_uploader("Upload your files (Excel, PDF, Word, JPEG)", accept_multiple_files=True)

# To store processed data
offers_data = []

# Process each uploaded file
if uploaded_files:
    st.subheader("Uploaded Files:")
    for file in uploaded_files:
        st.write(f"File: {file.name}")
        
        # File type checking
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
            st.write(f"Data from {file.name}:")
            st.write(df)
            offers_data.append(df)
        elif file.name.endswith('.pdf'):
            # Add PDF processing logic (e.g., using PyMuPDF or PyPDF2)
            st.write(f"PDF file: {file.name} - Extracting data...")
        elif file.name.endswith('.docx'):
            # Add Word processing logic (e.g., using python-docx)
            st.write(f"Word file: {file.name} - Extracting data...")
        elif file.name.endswith('.jpeg') or file.name.endswith('.jpg'):
            # Add image processing logic (e.g., using pytesseract)
            st.write(f"Image file: {file.name} - Extracting text...")

# Step 2: LCNITC Calculation Section
st.header("Calculate LCNITC Rates")
if st.button("Generate Calculations for All Offers"):
    all_data = []
    for offer in offers_data:
        # Assuming the structure of each dataframe has 'Base Rate (INR)', 'Freight (%)', etc.
        offer["Freight (INR)"] = (offer["Base Rate (INR)"] * offer["Freight (%)"]) / 100
        offer["P&F (INR)"] = (offer["Base Rate (INR)"] * offer["Packing & Forwarding (%)"]) / 100
        offer["Taxes (INR)"] = (offer["Base Rate (INR)"] + offer["Freight (INR)"] + offer["P&F (INR)"]) * (offer["CGST & SGST (%)"] / 100)
        offer["Landed Cost (INR)"] = offer["Base Rate (INR)"] + offer["Freight (INR)"] + offer["P&F (INR)"] + offer["Taxes (INR)"]
        offer["LCNITC (INR)"] = offer["Landed Cost (INR)"] - offer["Taxes (INR)"]
        all_data.append(offer)

    # Combine all dataframes into one
    final_df = pd.concat(all_data, ignore_index=True)

    # Display final calculated data
    st.write("Calculated Data for All Offers:")
    st.write(final_df)

    # Export as Excel in the required format
    file_path = "calculated_data.xlsx"
    final_df.to_excel(file_path, index=False)
    with open(file_path, "rb") as file:
        st.download_button(
            label="Download Processed Excel",
            data=file,
            file_name="LCNITC_Calculations.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        os.remove(file_path)

# Notes Section
st.header("Notes Section")
st.text_area("Add Special Notes", "Enter any specific notes here for the processed case.")


