from xhtml2pdf import pisa
from cStringIO import StringIO

def create_pdf(pdf_data,file_name):
    resultFile = open('reports/%s.pdf'%file_name, "w+b")
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), dest=resultFile) 
    resultFile.close() 
    return