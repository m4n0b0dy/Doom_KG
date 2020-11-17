import sys
sys.path.insert(0, '../tools/')
from rap_scrpr import *
import pandas as pd

link_df = pd.read_csv('clean_links.csv')

scrape_multi_artists(list(zip(link_df['link'], link_df['name']))[0:4])