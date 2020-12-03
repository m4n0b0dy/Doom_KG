# Hip-Hop Song/Artist/Album Knowledge Graph

## Scraped http://www.ohhla.com/, Performed ETL to transform Raw Text to Node/Edge CSVs, Ingested to Neo4j GraphDB, Wrote Semantic Triple Extraction for Templated Cypher Queries

## Project ToDos
- [x] Scrape all rappers and songs from ohhla
- [x] Extract, Transform, Load, New Line Delimited JSON into CSV Node/Edge format
- [x] Run Neo4j Docker container after mounting data drive
- [x] Ingest all CSV data into Neo4j
- [x] Enhance with Musical Group (extracted from Wikidata)
- [x] Write templated Question Answering Cypher Queries
- [x] Write Triple Extraction helpers file (inspred from [this](https://programmerbackpack.com/python-nlp-tutorial-information-extraction-and-knowledge-graphs/))
- [x] [Demonstrate Question Answering capability from Semantic Triples](https://github.com/m4n0b0dy/Doom_KG/blob/main/notebooks/Question%20Answering.ipynb)

## Project Tools
- Python
  - Spacy
  - Networkx
  - Matplotlib
  - Pandas
  - MultiThreading
- AI Models
  - Spacy "en_core_web_lg"
- Neo4j
- Docker base images
  - Neo4j
- Scraping Tools
  - BeautifulSoup
  - urllib
  - JSON
  - RegEx

## The Paper
- [Paper Published Here](https://github.com/m4n0b0dy/Doom_KG/blob/main/Doom%20KG%20Paper.pdf)

## The Notebook
- [Notebook Published Here](https://github.com/m4n0b0dy/Doom_KG/blob/main/notebooks/Question%20Answering.ipynb)

## Server Specs
- GPU: Nvidia 1660 Super
- CPU: Intel E5-1620 3.6GHz 4-Core
- RAM: 32GB DDR3