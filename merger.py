import os
from PyPDF2 import PdfMerger
import re


def is_valid_filename(filename):
    invalid_chars = r'[<>:"/\\|?*]'

    # checking if the file name has any invalid characters
    if re.search(invalid_chars, filename):
        return False
    return True


def delete_pdf_files(directory):
    # Delete PDF files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Deleted: {file_path}")


# folder with the pdfs
folder_path = "pdfs/"
# ask the user for the name of the merged pdf file
file_name = input("What do you want the file to be named: ")

# check if the name is valid
if is_valid_filename(file_name):
    merged_name = file_name + ".pdf"
    print(f"Valid file name. The complete file name will be: {merged_name}")
else:
    print(
        'Invalid file name. Please avoid using the following characters: \\ / : * ? " < > |'
    )

# get all of the pdf files from the folder
pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

# sort them based on their names
pdf_files.sort(key=lambda x: int(x.split("_")[1]))
pdf_merger = PdfMerger()

# merge the pdfs
for pdf_name in pdf_files:
    with open(os.path.join(folder_path, pdf_name), "rb") as file:
        pdf_merger.append(file)

# checking if the output folder exists
output_folder = "merged"
os.makedirs(output_folder, exist_ok=True)

# save the merged file
output_file = os.path.join(output_folder, merged_name)
with open(output_file, "wb") as output:
    pdf_merger.write(output)

print(f"Merged PDF saved as {output_file}")
delete_files = input("Do you want to delete the PDF files in pdfs/? ").lower()
if delete_files == "no":
    pass
elif delete_files == "yes":
    delete_pdf_files("pdfs")
else:
    print("Invalid input. Please enter 'yes' or 'no'.")
