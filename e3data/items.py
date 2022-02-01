from scrapy import Item, Field


class ProteinDataItem(Item):
    uniprot_id = Field()
    gene_name = Field()
    full_name = Field()
    sequence = Field()
    subcellular_locations = Field()
    subcellular_topology = Field()
    features = Field()