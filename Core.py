import os
import PyPDF2
import pandas as pd
import argparse
from Info import Descrizione, Nome


class Extractor:
    def __init__(self, file_path: str):
        self.file_path = file_path




    @property
    def corpus(self):
        print(f'File PDF rinvenuto "{self.file_path}"    Estrazione testo... ')
        corpus = [row for page in PyPDF2.PdfReader(self.file_path).pages for row in Extractor.from_pdf(page)]
        return corpus

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

class CorpusExtractor():

    #to replace with regex
    def page_corpus(self, page):
        pass

    def corpus(self, pages):
        return maputil( self.page_corpus, pages )

class DefaultExtractor(CorpusExtractor):
    def page_corpus(self, page):
        text = page.extract_text()
        rows = text.split("\n")
        corpus = []
        for row in rows[7:]:
            try:
                float(row) #La tabbella è delineata da una riga contenente un singolo numro in virgola mobile
                return corpus
            except ValueError:
                corpus.append(
                    row.replace('*', ' ')  #Davanti al giorno "do", viene avvolte aggiunto un asterisco al posto dello spazio
                )



#analizza i dati di un file pdf,dato un algoritmo di estrazione "corpus"
class Analyzer:
    def __init__(self, filename,   corpusExtractor: CorpusExtractor = DefaultExtractor()):
        self.corpusExtractor = corpusExtractor
        self.pages = [page for page in PyPDF2.PdfReader(filename).pages]

    #list of pandas Dataframes for different Pages of the same PDF
    def features(self):
        corpus = self.corpusExtractor.corpus(self.pages)
        return maputil(lambda page_corpus:  pd.DataFrame( self.analyze_corpus(page_corpus) ).dropna().set_index("day") , corpus)


    @staticmethod
    def analyze(row):
        values = row.split()
        giorno_settimana = values[0]
        giorno = values[1]
        entry = None
        for word in values[2:]:
            Firstletter = word[0]
            if Firstletter.upper() == "E":
                entry = word[1:]
                break
        return {"w-day": giorno_settimana, "day": giorno, "entrata": entry}
    def analyze_corpus(self, page_corpus):
        return maputil(  Analyzer.analyze , page_corpus )
mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobbre", "Novembre", "Dicembre"]

def elaborate(Data):

    Data["turno"] = Data["entrata"].apply(turno)
    Data["orario"] = Data["entrata"].apply(lambda orario: f"{orario[:2]}:{orario[2:]}")
    return Data
def main(filename ):
    analyzer = Analyzer(filename, DefaultExtractor())
    Pages_Data: list[pd.DataFrame] = maputil(elaborate, analyzer.features())
    values = pd.concat(Pages_Data)["turno"].value_counts()

    return Pages_Data, values



"""if __name__ == '__main__':
    Pages_Data, values = main()
    formats = '\n'.join(f"{mesi[idx]}\n{page.to_string()}" for idx, page in enumerate( Pages_Data ))

    print(formats)
    print(values)"""


if __name__ == '__main__':
    from tkinter import filedialog

    files: str = filedialog.askopenfilenames(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("pdf files",
                                                        "*.pdf*"),
                                                       ))

    print(files)

    base_names = maputil(os.path.basename, files)
    # Call the main function with the specified input and output filenames
    for file, base in zip(files, base_names):
        try:
            print("\nAnalizzando dati per il file:", base, "...")
            Pages_Data, values = main(file)
            print(values)

            output = f"./out/{base}.txt"

            print(f"Salvataggio in corso.... * {output} *")
            formats = '\n'.join(f"{mesi[idx]}\n{page.to_string()}" for idx, page in enumerate(Pages_Data))
            if not os.path.exists("./out"):
                os.makedirs("./out")

            with open( output, "w") as out:
                print(formats, values , sep="\n\n" , file=out)
        except Exception as e:
            print(f"Qualcosa è andato storto nella gestione del file '{base}':", e, sep="\n")
