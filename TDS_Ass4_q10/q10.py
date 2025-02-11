import pdfplumber

def extract_clean_text(pdf_path):
    text_output = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    cleaned_line = " ".join(line.split())  # Ensure proper spacing
                    text_output.append(cleaned_line)
    
    return "\n".join(text_output)

# Example usage
pdf_path = "q-pdf-to-markdown.pdf"
text_content = extract_clean_text(pdf_path)

# Save output to a file
with open("output1.md", "w", encoding="utf-8") as f:
    f.write(text_content)

print("Extracted text saved to output.txt")
