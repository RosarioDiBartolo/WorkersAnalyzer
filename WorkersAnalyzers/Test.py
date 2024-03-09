
import PyPDF2
path = "./WorkersAnalyzers/PisaTests/Galli Chiara_AOUP_timbrature.pdf"


pdf = PyPDF2.PdfReader(path)

pages =  [page.extract_text()  for page in pdf.pages]
text = "\nPAGE\n".join(pages)

pages = [page.split("\n")  for page in pages]
nomi = {row[0] for row in pages}

if __name__ == '__main__':
    print(nomi)
