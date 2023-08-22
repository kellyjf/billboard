#!/usr/bin/python3
from argparse import ArgumentParser as ap
from schema import session, Song, Artist, Entry
import csv
from datetime import datetime

if __name__ == "__main__":
	parser=ap()
	parser.add_argument("csvfile", nargs="?", action="store", help="CSV file to load")
	args=parser.parse_args()


	if args.csvfile:
		with open(args.csvfile, "r") as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				#print(row['date'],row['song'],row['artist'],row['last-week'],row['peak-rank'],row['weeks-on-board'])
				date=datetime.strptime(row['date'],"%Y-%m-%d")
				artist=session.query(Artist).filter(Artist.text==row['artist']).first()
				if not artist:
					artist=Artist(text=row['artist'])
					session.add(artist)
					print(artist)
				song=session.query(Song).filter(Song.artist_id==artist.id).filter(Song.text==row['song']).first()
				if not song:
					song=Song(artist=artist,text=row['song'])
					session.add(song)
					print(date,song)
				
				entry=Entry(song=song, date=date, rank=int(row['rank']), peak=int(row['peak-rank']), weeks=int(row['weeks-on-board']))
				session.add(entry)
				session.commit()


	songs=session.query(Song).all()
	for song in songs:
		entries=sorted(song.entries, key=lambda x: (x.rank, x.date))
		song.weeks=len(entries)
		peak=entries[0]
		song.peak=peak.rank
		song.date=peak.date
		song.weeks=len(entries)
		session.add(song)
		print(song.date, song.artist.text, song.text, song.peak, song.weeks)
	session.commit()
