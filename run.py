from pathlib import Path

import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from e3data.spiders.protein_data import ProteinDataSpider

# Settings
e3_csv = "./data/e3.csv"
e3_uniprot_column = "Uniprot"
pdb_output = "./data/pdb"
json_output = "./data/e3.json"

# Parse E3 csv
e3_df = pd.read_csv(e3_csv)
e3_uniprot_list = e3_df[e3_uniprot_column].tolist()

# Run
settings = get_project_settings()
settings["FEEDS"] = {Path(json_output): {"format": "json", "encoding": "utf8"}}
process = CrawlerProcess(settings=settings)
process.crawl(ProteinDataSpider, uniprot_ids=e3_uniprot_list)
process.start()
