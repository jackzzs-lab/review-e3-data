from scrapy import Item, Field


class ProteinDataItem(Item):
    uniprot_id = Field()
    gene_name = Field()
    full_name = Field()
    ec_number = Field()
    sequence = Field()
    subcellular_locations = Field()
    subcellular_topology = Field()
    features = Field()
    
class ProteinStructureItem(Item):
    uniprot_id = Field()
    gene_name = Field()
    pdb_id = Field()
    resolution = Field()
    chains = Field()
    range = Field()