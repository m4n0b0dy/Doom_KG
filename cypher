LOAD CSV WITH HEADERS FROM "file:///massive/art_sng.csv" AS line  with line where line.artist_node is not null and line.song_node is not null
MERGE (artist:Artist {name: line.artist_node})
MERGE (song:Song {name: line.song_node})
MERGE (artist)-[:RAPS_ON]->(song);

LOAD CSV WITH HEADERS FROM "file:///massive/alb_sng.csv" AS line  with line where line.album_node is not null and line.song_node is not null
MERGE (album:Album {name: line.album_node})
MERGE (song:Song {name: line.song_node})
MERGE (album)-[:CONTAINS]->(song);

LOAD CSV WITH HEADERS FROM "file:///massive/art_alb.csv" AS line with line where line.album_node is not null and line.artist_node is not null
MERGE (artist:Artist {name: line.artist_node})
MERGE (album:Album {name: line.album_node})
MERGE (artist)-[:PRIMARY]->(album);