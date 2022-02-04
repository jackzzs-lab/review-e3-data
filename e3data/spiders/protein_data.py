from scrapy import Spider, Request

from ..items import ProteinDataItem


class ProteinDataSpider(Spider):
    name = "protein_data"
    allowed_domains = ["uniprot.org"]

    def __init__(self, uniprot_ids=None, **kwargs):
        super().__init__(**kwargs)
        self.uniprot_ids = uniprot_ids

    def start_requests(self):
        if self.uniprot_ids:
            for i in self.uniprot_ids:
                yield Request("https://www.uniprot.org/uniprot/{}.xml".format(i), callback=self.parse_xml)

    def parse_xml(self, response):
        response.selector.remove_namespaces()
        
        item = ProteinDataItem()
        item["uniprot_id"] = response.xpath("//accession/text()").extract_first()
        item["gene_name"] = response.xpath('//gene/name[@type="primary"]/text()').extract_first()
        item["full_name"] = response.xpath("//fullName/text()").extract_first()
        item["ec_number"] = response.xpath("//ecNumber/text()").extract_first()
        item["sequence"] = response.xpath("//sequence/text()").extract_first()
        item["subcellular_locations"] = response.xpath("//subcellularLocation/location[@evidence]/text()").extract()
        item["subcellular_topology"] = response.xpath("//subcellularLocation/topology[@evidence]/text()").extract()
        
        features = []
        for t in response.xpath('//feature[@type="topological domain" or @type="transmembrane region"]'):
            features.append(
                {
                    "type": t.xpath("./@type").extract_first(),
                    "description": t.xpath("./@description").extract_first(),
                    "location": (
                        t.xpath("./location/begin/@position").extract_first(),
                        t.xpath("./location/end/@position").extract_first(),
                    ),
                }
            )
        item["features"] = features
        
        return item
