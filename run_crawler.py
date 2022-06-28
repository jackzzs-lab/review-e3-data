from pathlib import Path
import json
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from e3data.spiders.protein_data import ProteinDataSpider
from e3data.spiders.protein_structure import ProteinStructureSpider

# Settings
e3_csv = "./data/e3.csv"
e3_uniprot_column = "Uniprot"
data_json_output = "./data/e3.json"
pdb_json_output = "./data/e3_pdb.json"
pdb_output = "./data/pdb"
os.makedirs(pdb_output, exist_ok=True)

# Parse E3 csv
e3_df = pd.read_csv(e3_csv)
e3_uniprot_list = e3_df[e3_uniprot_column].tolist()

# Run crawler: protein_data
settings = get_project_settings()
settings["FEEDS"] = {Path(data_json_output): {"format": "json", "encoding": "utf8"}}
settings["ITEM_PIPELINES"] = {'e3data.pipelines.ProteinDataFilter': 300}
process = CrawlerProcess(settings=settings)
process.crawl(ProteinDataSpider, uniprot_ids=e3_uniprot_list)
process.start()

# Get filtered list
with open(data_json_output, 'r') as f:
    data = json.load(f)
if not data or not isinstance(data, list):
    raise ValueError(f'Invalid data "{data_json_output}"')

# Run crawler: protein_structure
settings = get_project_settings()
settings["FEEDS"] = {Path(pdb_json_output): {"format": "json", "encoding": "utf8"}}
settings["PROXY"] = 'http://localhost:1080'
settings["FILES_STORE"] = pdb_output
settings["ITEM_PIPELINES"] = {"e3data.pipelines.PDBFilePipeline": 300}
process = CrawlerProcess(settings=settings)
process.crawl(ProteinStructureSpider, uniprot_ids=[e.get("uniprot_id") for e in data], pdb_dir=pdb_output)
process.start()
