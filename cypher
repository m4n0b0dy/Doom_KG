#create nodes

:auto USING PERIODIC COMMIT 9999
LOAD CSV WITH HEADERS FROM "file:///massive/all_artist_nodes.csv" AS line
MERGE (artist:Artist {name: line.nm})

:auto USING PERIODIC COMMIT 9999
LOAD CSV WITH HEADERS FROM "file:///massive/all_album_nodes.csv" AS line
MERGE (album:Album {name: line.nm, trunc_name: LEFT(line.nm,100)})

:auto USING PERIODIC COMMIT 9999
LOAD CSV WITH HEADERS FROM "file:///massive/all_song_nodes.csv" AS line
MERGE (song:Song {name: line.nm})

#index nodes
CREATE INDEX artist_index IF NOT EXISTS
FOR (n:Artist)
ON (n.name);

CREATE INDEX album_index IF NOT EXISTS
FOR (n:Album)
ON (n.name);

CREATE INDEX song_index IF NOT EXISTS
FOR (n:Song)
ON (n.name);

#create relationships
:auto USING PERIODIC COMMIT 9999
LOAD CSV WITH HEADERS FROM "file:///massive/art_sng.csv" AS line  with line where line.artist_node is not null and line.song_node is not null
MATCH (artist:Artist {name: line.artist_node})
MATCH (song:Song {name: line.song_node})
MERGE (artist)-[:RAPS_ON]->(song);

:auto USING PERIODIC COMMIT 9999
LOAD CSV WITH HEADERS FROM "file:///massive/alb_sng.csv" AS line  with line where line.album_node is not null and line.song_node is not null
MATCH (album:Album {trunc_name: LEFT(line.album_node,100)})
MATCH (song:Song {name: line.song_node})
MERGE (album)-[:CONTAINS]->(song);

:auto USING PERIODIC COMMIT 9999
LOAD CSV WITH HEADERS FROM "file:///massive/art_alb.csv" AS line with line where line.album_node is not null and line.artist_node is not null
MATCH (artist:Artist {name: line.artist_node})
MATCH (album:Album {trunc_name: LEFT(line.album_node,100)})
MERGE (artist)-[:PRIMARY]->(album);

#bring in the wiki data
CREATE INDEX group_index IF NOT EXISTS
FOR (n:Group)
ON (n.name);


LOAD CSV WITH HEADERS FROM 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSHe5hgovoVh-LwpJpYGBGdgrhP-4nBinqR_qHKKPaCQjJikez0V9xZu9kYg8zeI32KJqcWkBosTaVu/pub?gid=773183182&single=true&output=csv'
as line
WITH line WHERE line.artist_node is not null and line.group_node is not null
MERGE (artist:Artist {name: toLower(line.artist_node)})
MERGE (album:Group {name: line.group_node})
MERGE (artist)-[:PRIMARY]->(album);
