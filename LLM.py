

from bs4 import BeautifulSoup
import requests
import re
from fpdf import FPDF


class MyFPDF(FPDF):
    def __init__(self):
        super().__init__()

    
    def _escape(self, txt):
      
        txt = txt.replace('\u2013', '-')  
        txt = txt.replace('\u2014', '-')  
        txt = txt.replace('\u2018', "'")  
        txt = txt.replace('\u2019', "'")  
        txt = txt.replace('\u201c', '"') 
        txt = txt.replace('\u201d', '"')  
        return txt.encode('latin-1', 'replace').decode('latin-1')


pdf = MyFPDF()


pdf_file = "Extracted.pdf"


for index in range(1, 11):
    pdf.add_page()
    url = f"https://bhagavadgita.io/chapter/{index}"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Chapter title
    chapter_title = f"Chapter {index}"
    pdf.set_font("Arial", size=16)
    pdf.multi_cell(0, 10, txt=chapter_title, align="C")
    pdf.ln()

    
    verses = soup.find_all("div", class_="flex w-full flex-col justify-between rounded-lg px-6 py-2 hover:cursor-pointer hover:bg-box-bg dark:hover:bg-dark-100 lg:flex-row lg:py-5")

    for verse in verses:
        
        cleaned_text = pdf._escape(verse.text.strip())

      
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=cleaned_text, align="L")
        pdf.ln()


pdf.output(pdf_file)
