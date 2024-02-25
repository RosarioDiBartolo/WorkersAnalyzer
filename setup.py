from setuptools import setup, find_packages

Nome = "WorkerAnalyzer"
Descrizione = f"""
"{Nome}" è un software designato per l'automatizzazzione di diversi processi relativi all'ambito gestionale di lavoratori/dipendenti do un azienda, o semplici componenti di istituzioni o associazioni indipendentemente dallo scopo =)
"""



setup(
    name=Nome,
    version='0.1.0',
    description=Descrizione,
    author='Rosario Di Bartolo',
    packages=find_packages(),  # Automatically discover and include all packages,
    setup_requires=['wheel'],

install_requires= """numpy==1.26.4
pandas==2.2.0
pyarrow==15.0.0
PyPDF2==3.0.1
pytz==2024.1
six==1.16.0
tzdata==2024.1
""".split('\n')

)


