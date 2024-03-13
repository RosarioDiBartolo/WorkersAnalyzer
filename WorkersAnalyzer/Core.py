import os
from tkinter import filedialog

import PyPDF2
import numpy as np

Orari_Entrate = np.array([7, 14, 21])

Orario_turno = {
7: "Mattina",
14: "Pomeriggio",
21: "Notte",
}
def turno(entrata):
    indice_piu_vicino = np.argmin(np.abs(Orari_Entrate - entrata.hour))
    numero_piu_vicino = Orari_Entrate[indice_piu_vicino]
    return Orario_turno[numero_piu_vicino]
class Directory:

    def __init__(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

        self.directory = dir
    def to(self, file):
        return os.path.join(self.directory, file)

    @staticmethod
    def return_dir(method):
        def wrapper(*args, **kwargs):
            directory = method(*args, **kwargs)
            return Directory(directory)

        return wrapper
    @return_dir
    def path(self, *paths):
        return os.path.join(self.directory, *paths)



    @staticmethod
    def from_explorer():
        dir = filedialog.askdirectory(initialdir="./",
                                            title="Select a Directory",)
        return Directory(dir)



def PDFIterator(file):
    pages = PyPDF2.PdfReader(file).pages

    for page in pages:
        text = page.extract_text()
        if not text:
            continue

        yield text.split("\n")
