"""
    DGSIAP + Web Scraping = DGScraper
"""

import warnings
warnings.filterwarnings("ignore", message=".*global interpreter lock.*", category=RuntimeWarning)

from bs4 import BeautifulSoup
import yarl
import re
import requests as r


"""
    Fase Uno: El Diccionario Maestro
"""

class DGScraper:
    def __init__(self, ref, info="Agricola"):
        assert info in ["Agricola", "Pecuaria"], "Revisa la información a consultar"
        link = ref + info + ".php"
        self.link = link
        print(link)
        response = r.get(link, stream=True) 
        response.raise_for_status()
        self.status = response.status_code
        self.response = response

    def parser(self):
        self.dgsiap = BeautifulSoup(self.response.content, "lxml")
    
    def preprocess(self):
        self.dg_main = self.dgsiap.find("main")
        self.sections = self.dg_main.find_all("section", recursive=False)

    def blocks_intro(self):
        history = self.sections[3]
        data_title = history.find("div", {"class":"mb-0 h5 font-weight-bold section-title"}).text
        data_content = history.find("div", {"id":"dataAccordion"})
        blocks = data_content.find_all("div", recursive=False)
        data_blocks = {b.find("div", {"class":"d-flex align-items-center"}).text.strip(): b for b in blocks}
        # print(f"Los datos historicos se presentan en el espacio denominado: {data_title}")
        data_blocks_f = [f"{k + 1}. {b}" for k, b in enumerate(data_blocks.keys())]
        # print(f"Los datos se encuentran divididos en 3 bloques:\n\n{"\n".join(data_blocks_f)}")
        self.blocks = data_blocks


    def format_codebook(self, category):
        data_blocks = self.blocks
        assert category in list(data_blocks.keys()), "Revisa la categoria"
        if category == "Municipal":
            raw = self.sections[2]
            sec = raw.find("div", {"class":"dict-section"})
        else:
            sec = data_blocks[category]
        mini_blocks = sec.find_all("div", {"class":re.compile(r"col-12 col-md-6*?")})
        codebook, metadata = mini_blocks[0], mini_blocks[1]
        codebook_info = {"title": codebook.find("h2").text, 
                        "description": codebook.find("p").text,
                        "download": codebook.find("a")['href']}
        meta = metadata.find("div")
        datetype = meta.find_all("div", recursive=False)
        metadata_info = {"title": meta.find("h4").text,
                        "state": datetype[0].find("span", {"class":"label"}).text,
                        "lastdate": datetype[0].find("span", {"class":"value"}).text,
                        "range": datetype[1].find("span", {"class":"label"}).text,
                        "size": datetype[1].find("span", {"class":"value"}).text
                        }
        return metadata_info, codebook_info


    def dict_master(self):
        data_blocks= self.blocks

        # Diccionario de Datos
        data_dicts = {db:{} for db in data_blocks.keys()}

        for db in data_dicts.keys():
            data_dicts[db]["metadata"], data_dicts[db]["info"] = self.format_codebook(db)

        data_history = {db:[] for db in data_blocks.keys()}

        for db in data_history.keys():
            block = data_blocks[db]
            con_data = block.find_all("a", {"class":"dl-btn"})
            href_data = [yarl.URL(a['href']) for a in con_data]
            data_history[db] += href_data


        # Conglomerado en un solo dicctionario. 
        assert set(data_history.keys()) == set(data_dicts.keys()), "Revise los bloques utilizados"
        connector = {b: {"Metadata": data_dicts[b],
                    "Datasets": data_history[b]}
                    for b in data_dicts.keys()}
        return connector
