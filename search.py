#!/usr/bin/python3
from argparse import ArgumentParser as ap
from schema import session, Song, Artist, Entry
from datetime import datetime
import requests
from lxml import html
import os
import re

# >>> y=re.findall("\"/watch\?v=([^\"]*)\\\\u0026", txt)

if __name__ == "__main__":
	parser=ap()
	parser.add_argument("--start","-s", action="store", type=int, default=1970,  help="From year")
	parser.add_argument("--end","-e", action="store", type=int, help="To year")
	parser.add_argument("--min-peak","-n", action="store", type=int, default=7,  help="Min Peak")
	parser.add_argument("--max-peak","-x", action="store", type=int, default=10,  help="Max Peak")
	args=parser.parse_args()



	fromdate=datetime.strptime(f"{args.start}-01-01", "%Y-%m-%d")
	if args.end:
		todate=datetime.strptime(f"{args.end}-01-01", "%Y-%m-%d")
	else:
		todate=datetime.strptime(f"{args.start+1}-01-01", "%Y-%m-%d")

	entries=session.query(Entry).filter(Entry.date<todate).filter(Entry.date>=fromdate).all()
	
	songs=set([x.song for x in entries])
	res=list()
	for song in songs:
		ents=sorted(song.entries, key=lambda x:x.rank)
		peak=ents[0]
		
		if peak.rank<=args.max_peak and peak.rank>=args.min_peak:
			res.append(peak)

	for result in sorted(res, key=lambda x: (x.date,x.rank))[:3]:
		
		print(f"{result.date.strftime('%Y-%m-%d')} {result.rank: 3d} {result.song.artist.text:<35.35} {result.song.text}")

		song=result.song
		artist=song.artist

		url="https://www.youtube.com/results?search_query="+requests.utils.quote(f"{result.song.text} {result.song.artist.text}")
		
		
		if not os.path.exists("data/{song.id}.html"):
			res=requests.get(url)
			text=None
			if res.status_code == 200:
				with open(f"data/{song.id}.html", "w") as f:
					text=res.text
					f.write(text)
		else:
			with open(f"data/{song.id}.html", "r") as f:
				text=f.read()


		if text:
			codes=re.findall("\"/watch\?v=([^\"]*)\\\\u0026", text)
			dcodes=[]
			for code in codes:
				if code not in dcodes:
					dcodes.append(code)
			for code in dcodes[:3]:
				print(f"https://youtube.com/watch?v={code}")

		print(url)
		
