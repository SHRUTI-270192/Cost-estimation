import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import os

# Title of the app
st.title("Budgetary Offer Processing App")

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(pdf_file)  # Open the PDF file
        text = ""
        for page_num in range(doc.page_count):  # Loop through each page
            page = doc.load_page(page_num)  # Load the page
            text += page.get_text("text")  # Extract text from the page
        return text
    except Exception as e:
        st.error(f"Error while processing the PDF: {e}")
        return None

# Step 1: File Upload Section
st.header("Upload Budgetary Offers")
uploaded_files = st.file_uploader("Upload your files (PDF)", accept_multiple_files=True)

# Store the extracted data
extracted_data = []

# Process each uploaded file
if uploaded_files:
    for file in uploaded_files:
        st.write(f"Processing file: {file.name}")
        extracted_text = extract_text_from_pdf(file)  # Extract text
        
        if extracted_text:
            st.text_area("Extracted Text", extracted_text, height=300)  # Display extracted text
            extracted_data.append(extracted_text)  # Store extracted text for further processing
        else:
            st.error(f"Failed to extract text from {file.name}.")
else:
    st.warning("Please upload a valid PDF file.")

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

# Step 3: Generate Cost Estimate Sheet
st.header("Generate Cost Estimate Sheet")
if st.button("Generate Cost Estimate"):
    # Sample data for cost estimate sheet
    cost_data = {
        "Sl. No.": [1],
        "UCS Code": ["20512001002541"],
        "Drawing No.": ["SMS3-22-277"],
        "Item description": ["Gear coupling Assy. For long roller"],
        "Unit": ["EA"],
        "Installed qty": [36],
        "Order Qty": [40],
        "Estimated rate (Rs.) (L1 price)(LCNITC)": [18000],
        "Amount (Rs.)": [18000 * 40]
    }

    cost_df = pd.DataFrame(cost_data)

    # Display the cost estimate data
    st.write("Cost Estimate Data:")
    st.write(cost_df)

    # Export the cost estimate sheet to Excel
    cost_file_path = "cost_estimate_sheet.xlsx"
    cost_df.to_excel(cost_file_path, index=False)

    with open(cost_file_path, "rb") as file:
        st.download_button(
            label="Download Cost Estimate Sheet",
            data=file,
            file_name="Cost_Estimate_Sheet.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        os.remove(cost_file_path)

# Notes Section
st.header("Notes Section")
st.text_area("Add Special Notes", "Enter any specific notes here for the processed case.")




