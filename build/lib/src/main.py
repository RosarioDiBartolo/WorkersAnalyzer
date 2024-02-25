import os

from Core import maputil, mesi, PDFBlock
from Extractors.PisaExtractor import PisaExtractor
import pandas as pd

def main(filename, extractor, test=False):
    block = PDFBlock.from_file(filename)
    analyzer = extractor(block.pages)

    Pages_Data = analyzer.features(test)
    Pages_Data , name = block.verify(Pages_Data)

    values = pd.concat(Pages_Data)["turno"].value_counts()
    return Pages_Data, values, name


if __name__ == '__main__':
    from tkinter import filedialog

    files = filedialog.askopenfilenames(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("pdf files",
                                                        "*.pdf*"),
                                                       ))


    print(files)
    base_names = maputil(lambda f: os.path.basename(f).split(".")[0], files)
    # Call the main function with the specified input and output filenames
    for file, base in zip(files, base_names):
        try:
            print("\nAnalizzando dati per il file:", base, "...")
            Pages_Data, values, name = main(file, PisaExtractor )
            print(values)

            output = f"./out/{base}.txt"

            print(f"Salvataggio in corso.... * {output} *")
            if not os.path.exists("./out"):
                os.makedirs("./out")

            with open( output, "w") as out:
                print( name,  values.to_string(),sep='\n' , file=out)
        except Exception as e:
            print(f"Qualcosa è andato storto nella gestione del file '{base}':", e.with_traceback(), sep="\n")

    input("Analisi completata con successo. Premi qualsiasi pulsante per chiudere il progamma\n")