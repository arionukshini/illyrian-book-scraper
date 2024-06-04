import requests
from bs4 import BeautifulSoup
import os
import sys

def test_book(book):
    url = "https://illyrianpride.com/book/detail/"
    book_url = url + book
    
    response = requests.get(book_url)
    if response.status_code == 200:
        pass
    else:
        print(f"Failed to retrieve book page {book_url}, status code: {response.status_code}")
        sys.exit()

def get_sections():
    sections = {}
    print("Enter sections (type 'end' or 'stop' to finish):")
    i = 1
    while True:
        section_name = input(f"Section {i}: ").strip()
        if section_name.lower() in ['end', 'stop']:
            break
        sections[i] = section_name
        i += 1
    return sections

def main():
    # base url
    book = input("Please input which book you want to download: ").lower()
    base_url = f"https://illyrianpride.com/book/{book}/page/"
    sections = get_sections()
    page_num = 1

    test_book(book)
    
    # folder for where to save the files
    pdf_dir = "pdfs"
    os.makedirs(pdf_dir, exist_ok=True)

    # go through the sections
    for section_num, section_name in sections.items():
        while True:
            # construct the full url
            url = f"{base_url}{section_name}{page_num}/"
            print(url)

            # get the page content
            response = requests.get(url)

            # check if the request was successful
            if response.status_code == 200:
                # parse the html content
                soup = BeautifulSoup(response.content, "html.parser")

                # find the pdf link
                pdf_link = soup.find('a', id='pdfHref')
                if (pdf_link and 'href' in pdf_link.attrs):
                    pdf_url = pdf_link['href']
                    print(f"Found PDF URL: {pdf_url}")

                    # download the pdf
                    pdf_response = requests.get(pdf_url)
                    if pdf_response.status_code == 200:
                        # create a file based on the url
                        pdf_filename = os.path.join(pdf_dir, f"document_{section_num}_{page_num}.pdf")
                        with open(pdf_filename, 'wb') as pdf_file:
                            pdf_file.write(pdf_response.content)
                        print(f"Downloaded PDF: {pdf_filename}")
                    else:
                        print(f"Failed to download PDF, status code: {pdf_response.status_code}")
                else:
                    print("PDF link not found on the page")
                    break  # no pdf link found, so we assume this is the last page

                page_num += 1
            else:
                print(f"Failed to retrieve page {page_num}, status code: {response.status_code}")
                break  # if the page couldn't be retrieved, stop processing this section

if __name__ == "__main__":
    main()
