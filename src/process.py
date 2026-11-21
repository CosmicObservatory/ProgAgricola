from config.datasources import URL_REF_DGSIAP, URL_API_DGSIAP
from download.File import INEGITree
from download.dgsiap import DGScraper
from yarl import URL


# WebScraping de la página del DGSIAP
webscraper = DGScraper(URL_REF_DGSIAP)
print(webscraper.link)
print(webscraper.status)

webscraper.parser()
print(webscraper.dgsiap)

webscraper.preprocess()
print(webscraper.sections)

webscraper.blocks_intro()

master_dict = webscraper.dict_master()
print(master_dict)


# Descarga de los datos

def parse_link(url, base):
    y_url= URL(url)
    link = base.with_query(y_url.query)
    return link


dgsiap_trees = {v: master_dict[v] for v in master_dict.keys()}
municipal_tree = dgsiap_trees['Municipal']

mun_metadata = municipal_tree['Metadata']['info']['download']
mun_datasets = municipal_tree['Datasets']


mun = INEGITree("DGSIAP", parse_link(mun_metadata, URL_API_DGSIAP), [
    parse_link(data, URL_API_DGSIAP) for data in mun_datasets])
mun.metadata(municipal_tree['Metadata'])
mun.download()