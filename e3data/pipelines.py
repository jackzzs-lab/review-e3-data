import os

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from thefuzz.fuzz import partial_ratio


class ProteinDataFilter:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        subcellulars = []
        for field in ["subcellular_locations", "subcellular_topology", "go_locations"]:
            if adapter.get(field):
                subcellulars.extend(adapter.get(field))
        if not subcellulars:
            raise DropItem("Missing subcellular location informations.")
        for loc in subcellulars:
            if isinstance(loc, str):
                if partial_ratio(loc.lower(), "membrane") > 80:
                    break
                if partial_ratio(loc.lower(), "vesicle") > 80:
                    break
                if partial_ratio(loc.lower(), "envelope") > 80:
                    break
                if partial_ratio(loc.lower(), "caveola") > 80:
                    break
        else:
            raise DropItem("Not a membrane-associated protein.")
        return item


class PDBFilePipeline(FilesPipeline):
    def get_media_requests(self, items, info):
        if items and "pdb_id" in items:
            url = "https://files.rcsb.org/download/{}.pdb".format(items["pdb_id"])
            yield Request(url, meta={"pdb_id": items["pdb_id"], "proxy": info.spider.settings.get("PROXY")})

    def file_path(self, request, response=None, info=None, *, item=None):
        return request.meta["pdb_id"] + ".pdb"

