import os

from WorkersAnalyzer.Core import PDFIterator


def open_raw_test(name):
    with open(os.path.join("../RawText", f"{name}.txt"), 'r') as f:
        pages = f.read().split("\nPAGE\n")

    return [page.splitlines() for page in pages]


def basename(filename):
    return filename.split(".")[0]


def test_on_files():
    tests_path = "../PisaTests"
    files = os.listdir(tests_path)

    for file in files:
        name = basename(file)
        print("Executing:", name)

        yield PDFIterator( os.path.join(tests_path, file) ), name