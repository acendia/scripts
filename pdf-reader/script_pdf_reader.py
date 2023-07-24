import PyPDF2

# Open the PDF file
pdf_file = open('example.pdf', 'rb')

# Create a PdfReader object
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# Get the number of pages
num_pages = pdf_reader.getNumPages()

# Loop through the pages and extract text
for page_num in range(num_pages):
    page = pdf_reader.getPage(page_num)
    text = page.extractText()
    print(text)

# Close the PDF file
pdf_file.close()

