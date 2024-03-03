from setuptools import setup, find_packages

Nome = "WorkersAnalyzer"
Descrizione = f"""
"{Nome}" è un software designato per l'automatizzazzione di diversi processi relativi all'ambito gestionale di lavoratori/dipendenti do un azienda, o semplici componenti di istituzioni o associazioni indipendentemente dallo scopo =)
"""


requirements = """
anyio==4.3.0
beautifulsoup4==4.12.3
bs4==0.0.2
certifi==2024.2.2
charset-normalizer==3.3.2
dateutils==0.6.12
docx==0.2.4
h11==0.14.0
httpcore==1.0.4
httpx==0.27.0
idna==3.6
lxml==5.1.0
numpy==1.26.4
pandas==2.2.0
pillow==10.2.0
pyarrow==15.0.0
PyPDF2==3.0.1
python-dateutil==2.8.2
python-docx==1.1.0
pytz==2024.1
requests==2.31.0
setuptools==69.1.1
six==1.16.0
sniffio==1.3.0
soupsieve==2.5
typing_extensions==4.9.0
tzdata==2024.1
urllib3==2.2.1
""".split('\n')

setup(
    name=Nome,
    version='0.1.0',
    description=Descrizione,
    author='Rosario Di Bartolo',
    packages=find_packages(),  # Automatically discover and include all packages,
    setup_requires=['wheel'],

install_requires=requirements

)


