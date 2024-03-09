import os
from tkinter import filedialog

import PyPDF2

class Directory:

    @staticmethod
    def return_dir(method):
        def wrapper(*args, **kwargs):
            directory = method(*args, **kwargs)
            return Directory(directory)
        return wrapper



    def __init__(self, dir):
        self.directory = dir

    @return_dir
    def path(self, *paths):
        return os.path.join(self.directory, *paths)
    @staticmethod
    def from_explorer():
        dir = filedialog.askdirectory(initialdir="./",
                                            title="Select a Directory",)
        return Directory(dir)



def PDFIterator(files):
    for file in files:
        pages = PyPDF2.PdfReader(file).pages

        for page in pages:
            yield page.extract_text().split("\n")