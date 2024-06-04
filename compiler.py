import os
from PyPDF2 import PdfMerger

# Path to the folder containing PDF files
folder_path = 'pdfs/'

# Get a list of all PDF files in the folder
pdf_files = [file for file in os.listdir(folder_path) if file.endswith('.pdf')]

# Sort the files based on their names
pdf_files.sort(key=lambda x: int(x.split('_')[1]))

# Create a PdfMerger object
pdf_merger = PdfMerger()

# Merge PDF files
for file_name in pdf_files:
    with open(os.path.join(folder_path, file_name), 'rb') as file:
        pdf_merger.append(file)

# Output folder for merged PDF
output_folder = 'compiled'
os.makedirs(output_folder, exist_ok=True)

# Output merged PDF
output_file = os.path.join(output_folder, 'merged.pdf')
with open(output_file, 'wb') as output:
    pdf_merger.write(output)

print(f'Merged PDF saved as {output_file}')
