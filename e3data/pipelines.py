import os

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from thefuzz.fuzz import partial_ratio


class ProteinDataFilter:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get("subcellular_locations") and not adapter.get("subcellular_topology"):
            raise DropItem("Missing subcellular location informations.")
        subcellulars = []
        subcellulars.extend(adapter.get("subcellular_locations"))
        subcellulars.extend(adapter.get("subcellular_topology"))
        for loc in subcellulars:
            if isinstance(loc, str) and partial_ratio(loc.lower(), "membrane") > 80:
                break
        else:
            raise DropItem("Not a membrane-associated protein.")
        return item
    
class PDBFilePipeline(FilesPipeline):
    def get_media_requests(self, items, info):
        if items and 'pdb_id' in items:
            url = "https://files.rcsb.org/download/{}.pdb".format(items['pdb_id'])
            yield Request(url, meta={'pdb_id': items['pdb_id'], 'proxy': info.spider.settings.get('PROXY')})

    def file_path(self, request, response=None, info=None, *, item=None):
        return request.meta['pdb_id'] + '.pdb'