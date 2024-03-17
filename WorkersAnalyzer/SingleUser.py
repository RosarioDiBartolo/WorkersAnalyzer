from WorkersAnalyzer.DataExtracted import DataExtracted

from WorkersAnalyzer.EasyTest.Test import open_raw_test
from WorkersAnalyzer.PisaExtractor import PisaExtractor



Extractors = [ PisaExtractor(p)  for p in open_raw_test("Andreotti Valeria_AOUP_timbrature" )]
Extractors = [e for e in  Extractors if  (e.mese == 4 and e.anno == 2019) ]
#extractor = UserExtractor( Extractors)
extractor = Extractors[0]

data = DataExtracted(extractor.with_datetime())
data.data["Turni"] = data.turni()

print( data.data  )