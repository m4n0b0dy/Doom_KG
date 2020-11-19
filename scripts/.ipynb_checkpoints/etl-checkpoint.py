import pandas as pd
import json
import re

from os import listdir
from os.path import isfile, join

from multiprocessing.pool import ThreadPool as Pool
thread_count = 500

ALL_ARTISTS = set()
ALL_ALBUMS = set()
ALL_SONGS = set()

def info_extract(art, album, songs):
	sep_name = re.sub('f./|f/|w/|&amp;|and|((^|\W)\()|(\)($|\W))', ',', art)
	list_of_names = sep_name.split(',')
	art_sng_rels = []
	alb_sng_rels = []
	global ALL_ALBUMS, ALL_ARTISTS, ALL_SONGS
	ALL_ALBUMS = ALL_ALBUMS|{album}
	alb_abrv = album[:2]+'-'+album[2:]
	for song in songs:
		song_name = song+'_'+alb_abrv
		ALL_SONGS = ALL_SONGS|{song_name}
		alb_sng_rels.append({'album_node':album, 'song_node':song_name, 'typ':'contains_song'})
		for name in list_of_names:
			if 'raw_song_' in name:
				continue
			name = name.strip().lower()
			ALL_ARTISTS = ALL_ARTISTS|{name}
			art_sng_rels.append({'artist_node':name, 'song_node':song_name, 'typ':'raps_on'})
	return art_sng_rels, alb_sng_rels

def etl_file(file):
	print('Starting Loading',file)
	master_name = file.split('.json')[0].lower()
	with open(mypath+file,'r') as f:
		data = json.load(f)
	art_sng_rels = []
	alb_sng_rels = []
	art_alb_rels = []
	for name, albums in data.items():
		if type(albums) == str:
			albums = {albums:''}
		for album, songs in albums.items():
			if not (len(album) > 500 or 'www.' in album) and songs != '':
				art_alb_rels.append({'album_node':album, 'artist_node':master_name, 'typ':'primary_artist'})
			art_sngs, alb_sngs = info_extract(name, album, list(songs))
			art_sng_rels.extend(art_sngs)
			alb_sng_rels.extend(alb_sngs)

	art_sng_df = pd.DataFrame(art_sng_rels)
	art_sng_df.to_csv('../data/csvs/'+'art_sng_df_'+master_name.replace(' ','')+'.csv',index=False)
	alb_sng_df = pd.DataFrame(alb_sng_rels)
	alb_sng_df.to_csv('../data/csvs/'+'alb_sng_df_'+master_name.replace(' ','')+'.csv',index=False)
	art_alb_df = pd.DataFrame(art_alb_rels)
	art_alb_df.to_csv('../data/csvs/'+'art_alb_df_'+master_name.replace(' ','')+'.csv',index=False)
	print('Finished Loading',file)

if __name__=='__main__':
	mypath = '../data/json_lyrics/'
	allfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	pool = Pool(thread_count)
	pool.map(etl_file, allfiles)
	pool.close()
	pool.join()
	_ = pd.DataFrame(columns=['nm'])
	_['nm'] = list(ALL_ARTISTS)
	_.to_csv('../data/csvs/all_artist_nodes.csv',index=False)
	_ = pd.DataFrame(columns=['nm'])
	_['nm'] = list(ALL_ALBUMS)
	_.to_csv('../data/csvs/all_album_nodes.csv',index=False)
	_ = pd.DataFrame(columns=['nm'])
	_['nm'] = list(ALL_SONGS)
	_.to_csv('../data/csvs/all_song_nodes.csv',index=False)