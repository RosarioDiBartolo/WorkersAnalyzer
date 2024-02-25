import os

from Core import main
from Extractors.PisaExtractor import PisaExtractor


def year_extraction(dir):
    files =[os.path.join( dir, file) for file in  os.listdir(dir) if file.endswith('.pdf')]
    print(files)
    values = [  main(f, PisaExtractor , True)[1].to_string()    for f in files]
    with open(os.path.join(dir, 'out.txt' ), 'w') as f:
        f.write('\n'.join(values  ))


if __name__ == '__main__':
    from tkinter import filedialog

    files = filedialog.askdirectory(initialdir = "/",
                                          title = "Seleziona la cartella del lavoratore",
                                    )
    year_extraction(files)

