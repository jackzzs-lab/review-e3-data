import logging
import pandas as pd
from scrapy import Spider, Request

from ..items import ProteinStructureItem


def apply(func, obj):
    try:
        if obj is not None:
            return func(obj)
        else:
            return None
    except (TypeError, ValueError):
        return None


class ProteinStructureSpider(Spider):
    name = "protein_structure"
    allowed_domains = ["uniprot.org", "rcsb.org"]

    def __init__(self, uniprot_ids=None, **kwargs):
        super().__init__(**kwargs)
        self.uniprot_ids = uniprot_ids

    def start_requests(self):
        if self.uniprot_ids:
            for i in self.uniprot_ids:
                yield Request("https://www.uniprot.org/uniprot/{}.xml".format(i), callback=self.parse_xml)

    def parse_xml(self, response):
        # namespace must be ignored for selection
        response.selector.remove_namespaces()

        uniprot_id = response.xpath("//accession/text()").extract_first()
        gene_name = response.xpath('//gene/name[@type="primary"]/text()').extract_first()

        # crawl available pdb structure entries
        entries = []
        for tree in response.xpath('//dbReference[@type="PDB" and ./property[@type="method"]/@value="X-ray"]'):
            resolution = tree.xpath('./property[@type="resolution"]/@value').extract_first().replace("A", "").strip()
            entry = {
                "uniprot_id": uniprot_id,
                "gene_name": gene_name,
                "pdb_id": tree.xpath("./@id").extract_first(),
                "resolution": apply(float, resolution),
            }
            chains_str = tree.xpath('./property[@type="chains"]/@value').extract_first()
            if chains_str:
                for r in chains_str.split(", "):
                    entry["chains"] = r.split("=")[0].split("/")
                    entry["range"] = [apply(int, i) for i in r.split("=")[1].split("-")]
                entries.append(entry)

        # select entry based on resolution
        if entries:
            entries = pd.DataFrame(entries)
            # get the structure of the highest resolution
            entry = entries.loc[entries["resolution"] == min(entries["resolution"]), :].to_dict("records")[0]
            yield ProteinStructureItem(entry)
        else:
            logging.warning(f"can't find any pdb structure information for {uniprot_id} ({gene_name}), skipping")

