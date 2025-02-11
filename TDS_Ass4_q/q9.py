import pdfplumber
import pandas as pd

# Function to extract table data from all pages in the PDF
def extract_tables_from_pdf(pdf_path):
    all_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(len(pdf.pages)):  # Loop through all pages
            page = pdf.pages[page_num]
            table = page.extract_table()
            if table:
                headers = table[0]
                data = table[1:]
                df = pd.DataFrame(data, columns=headers)
                all_data.append(df)
    
    # Concatenate all extracted tables into a single DataFrame
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return None

pdf_path = "q-extract-tables-from-pdf-1-25.pdf"

# Extract table data from all pages
df = extract_tables_from_pdf(pdf_path)

if df is not None:
    # Convert 'Maths' column to numeric (handling errors)
    df['Maths'] = pd.to_numeric(df['Maths'], errors='coerce')

    # Filter rows where 'Maths' is greater than or equal to 56
    filtered_df = df[df['Maths'] >= 56]

    # Calculate the total Maths marks
    total_math_marks = filtered_df['Maths'].sum()

    print("Total Maths marks of students who scored 56 or more:", total_math_marks)
else:
    print("No table data found in the PDF.")
