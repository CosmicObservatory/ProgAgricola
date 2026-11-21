from download.dgsiap import DGScraper
# DGSIAP
URL_REF_DGSIAP = "https://nube.agricultura.gob.mx/datosAbiertos/"

webscraper = DGScraper(URL_REF_DGSIAP)
print(webscraper.link)
print(webscraper.status)

webscraper.parser()
print(webscraper.dgsiap)

webscraper.preprocess()
print(webscraper.sections)

webscraper.blocks_intro()


print(webscraper.dict_master())
