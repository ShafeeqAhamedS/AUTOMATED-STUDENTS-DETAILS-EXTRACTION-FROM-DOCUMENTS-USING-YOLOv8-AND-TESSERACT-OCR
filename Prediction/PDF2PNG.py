import os
import fitz  
# PyMuPDF

# Input and output directories
pdf_file = "Marksheet.pdf"
out_folder = "Marksheet_Convt.png"

# Create the output directory if it doesn't exist
if not os.path.exists(out_folder):
    os.makedirs(out_folder)


# Convert  PDF to an image with higher quality (600 DPI)
pdf_document = fitz.open(pdf_file)

# Get the first page of the PDF
page = pdf_document[0]
    
# Create an image from the page with 300 DPI
pix = page.get_pixmap(matrix=fitz.Matrix(600 / 72, 600 / 72))
    
# Define the image file path
image_path = os.path.join(out_folder, os.path.splitext(pdf_file)[0] + '.png')
    
# Save the image with high quality
pix.save(image_path, "png")
    
# Close the PDF document
pdf_document.close()

print("PDF to image conversion with high quality completed.")