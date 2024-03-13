from WorkersAnalyzer.Core import turno


class DataExtracted:
    def __init__(self, data):
        self.data = data

    def turni(self):
        return self.data["Data"].apply(lambda e: turno(  e.time() )   )