import os
import webbrowser
from fpdf import FPDF
from filestack import Client

class PdfReport:
    """
    Creates a pdf that contains data about the flatmates
    such as their name, their due amount and period of bill.
    """

    def __init__(self, filename):
        self.filename = filename

    def generate(self, flatmate1, flatmate2, bill):
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Add icon
        pdf.image("flatmate_bills/files/house.png", w=50, h=50)

        # Insert title
        pdf.set_font(family="Times", size=22, style='B')
        pdf.cell(w=0, h=80, txt=f"Flatmates Bill", align='C', ln=1)

        # Insert Period label
        pdf.set_font(family='Helvetica', size=18, style='B')
        pdf.cell(w=100, h=40, txt=f"Bill period: ")
        pdf.cell(w=100, h=40, txt=f"{bill.period}", ln=1, align='L')

        # Insert bill details of flatmates
        pdf.set_font(family='Helvetica', size=14)
        pdf.cell(w=100, h=40, txt=f"{flatmate1.name}:")
        pdf.cell(w=100, h=40, txt=f"${flatmate1.pays(bill, flatmate2):.2f}", align='L', ln=1)
        pdf.cell(w=100, h=40, txt=f"{flatmate2.name}:")
        pdf.cell(w=100, h=40, txt=f"${flatmate2.pays(bill, flatmate1):.2f}", align='L')

        pdf_path = f"flatmate_bills/files/{self.filename}.pdf"
        pdf.output(name=pdf_path)

        # webbrowser.open(f"file://files/{os.path.realpath(pdf_path)}", new=1)

class FileShare:

    def __init__(self, filepath, api_key):
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)
        pdf_link = client.upload(filepath=self.filepath)
        return pdf_link.url
