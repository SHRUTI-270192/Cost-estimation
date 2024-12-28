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
        # Placeholder logic for file processing
        offers_data.append({
            "File Name": file.name,
            "Status": "Processed"  # Update with actual processing logic
        })

# Step 2: LCNITC Calculation Section
st.header("Calculate LCNITC Rates")
if st.button("Generate Sample Data"):
    # Create dummy data for testing
    data = {
        "Supplier": ["M/s MPFS Raipur", "M/s Macro Tech Engineers"],
        "Base Rate (INR)": [18000, 18500],
        "Freight (%)": [0, 2],
        "Packing & Forwarding (%)": [3, 0],
        "CGST & SGST (%)": [18, 18]
    }
    df = pd.DataFrame(data)
    st.write("Uploaded Data:")
    st.write(df)

    # Perform LCNITC calculation
    df["Freight (INR)"] = (df["Base Rate (INR)"] * df["Freight (%)"]) / 100
    df["P&F (INR)"] = (df["Base Rate (INR)"] * df["Packing & Forwarding (%)"]) / 100
    df["Taxes (INR)"] = (df["Base Rate (INR)"] + df["Freight (INR)"] + df["P&F (INR)"]) * (df["CGST & SGST (%)"] / 100)
    df["Landed Cost (INR)"] = df["Base Rate (INR)"] + df["Freight (INR)"] + df["P&F (INR)"] + df["Taxes (INR)"]
    df["LCNITC (INR)"] = df["Landed Cost (INR)"] - df["Taxes (INR)"]

    st.write("Calculated Data:")
    st.write(df)

    # Export as Excel
    file_path = "calculated_data.xlsx"
    df.to_excel(file_path, index=False)
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

