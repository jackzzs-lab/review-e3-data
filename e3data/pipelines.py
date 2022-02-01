import logging

from scrapy.exceptions import DropItem
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