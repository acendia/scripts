# Import the PyPDF2 library
import PyPDF2

# Open the PDF file
pdf_file = open('example.pdf', 'rb')

# Create a PdfReader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Get the number of pages
num_pages = len(pdf_reader.pages)

# Loop through the pages and extract text
for page_num in range(num_pages):
    page = pdf_reader.pages[page_num]
    text = page.extract_text()
    print(text)

# Close the PDF file
pdf_file.close()