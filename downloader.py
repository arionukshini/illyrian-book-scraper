import requests
from bs4 import BeautifulSoup
import os

# Define the base URL
base_url = "https://illyrianpride.com/book/ueb-sherbimet/page/"
section = {
    1: "hyrje-ne-ueb-sherbime-",
    2: "xml-",
    3: "teknologjite-e-shperndara-ne-ueb-",
    4: "arkitektura-e-ueb-sherbimeve-",
    5: "modelet-arkitekturale-te-ueb-sherbimeve-",
    6: "komunikimi-ndermjet-aplikacioneve-softuerike-",
    7: "teknologjite-dhe-komponetet-e-ueb-sherbimeve-"
}

# Directory to save the PDFs
pdf_dir = "pdfs"
os.makedirs(pdf_dir, exist_ok=True)

page_num = 1

# Iterate through the sections
for section_num, section_name in section.items():
    while True:
        # Construct the full URL
        url = f"{base_url}{section_name}{page_num}/"
        print(url)

        # Fetch the content of the page
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the PDF link
            pdf_link = soup.find('a', id='pdfHref')
            if pdf_link and 'href' in pdf_link.attrs:
                pdf_url = pdf_link['href']
                print(f"Found PDF URL: {pdf_url}")

                # Download the PDF
                pdf_response = requests.get(pdf_url)
                if pdf_response.status_code == 200:
                    # Create a filename based on the URL
                    pdf_filename = os.path.join(pdf_dir, f"document_{section_num}_{page_num}.pdf")
                    with open(pdf_filename, 'wb') as pdf_file:
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded PDF: {pdf_filename}")
                else:
                    print(f"Failed to download PDF, status code: {pdf_response.status_code}")
            else:
                print("PDF link not found on the page")
                break  # No PDF link found, so we assume this is the last page

            page_num += 1
        else:
            print(f"Failed to retrieve page {page_num}, status code: {response.status_code}")
            break  # If the page couldn't be retrieved, stop processing this section
