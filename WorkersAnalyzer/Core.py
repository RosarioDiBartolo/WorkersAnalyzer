import PyPDF2


class PDFBlock:

    def __init__(self, pages):
        self.pages = pages

    def exytract_text(self):
        return maputil(lambda page:page.extract_text() , self.pages)
    @staticmethod
    def from_file(filename):
        return PDFBlock( PyPDF2.PdfReader(filename).pages  )
    def verify(self, pages):
        data = [d[0] for d in pages  ]
        names = set(d[1] for d in pages )

        if len(names) > 1:
            print(names)
            raise Exception("Qualcosa è andato storto... il nome riscontrato nei pdf non sembra essere coerente")
        return data, names.pop()
def analyze(row: str):
    values = row.replace("*", ' ').split()
    giorno_settimana = values[0]
    giorno = values[1]
    entry = None
    for word in values[2:]:
        Firstletter = word[0]
        if Firstletter.upper() == "E":
            entry = word[1:]
            break
    return {"w-day": giorno_settimana, "day": giorno, "entrata": entry}

orari_turni = {
    700: "Mattina",
    2000: "Notte",
    1400: "Pomeriggio"
}
orari = orari_turni.keys()
def turno(orario_entrata_uscita):
    orario_entrata_uscita = int(orario_entrata_uscita)
    nearest = min(orari, key=lambda x: abs(x - orario_entrata_uscita))
    return orari_turni[nearest]


#simple map utility
maputil = lambda f, x: list(map(f, x))

unpack = lambda x: [z for y in x for z in y ]




#class for handling non-ocr files.
#Probably by using pytesseract
class ScannedExtractor:
    pass

#analizza i dati di un file pdf,dato un algoritmo di estrazione "corpus"


mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobbre", "Novembre", "Dicembre"]


