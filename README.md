# review-e3-data
A crawler for analyzing membrane-associated E3 ubiquitin ligase-related data.

## How to use
1. get a list of human e3 ligases from [NIH](https://esbl.nhlbi.nih.gov/Databases/KSBP2/Targets/Lists/E3-ligases/), as "data/e3.csv".
2. create a conda environment with:
```console
conda create -n e3-data -c conda-forge ipykernel scrapy seaborn matplotlib pandas numpy
```
3. run "run_crawler.py" to crawl data into "data/e3.json" and "data/e3_pdb.json". "data/e3.json" is a list of membrane-associated E3 ligases and their uniprot data. "data/e3_pdb.json" is a list of uniprot id and best pdb id found in RCSB PDB of the E3 ligases. All available PDBs of crawled proteins will also be downloaded to "data/pdb".
4. add the conda environment into ipykernel.
```console
python -m ipykernel install --user --name=e3-data
```
5. open "analyze.ipynb" with jupyter notebook, from any environment, and switch the python kernel to "e3-data".
6. run all the cells to get "data/e3_summary.csv", which is a summary of all crawled data, and "tm_domains.fasta", which contains all transmembrane domains of crawled e3 ligases.
