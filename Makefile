
DROPHOME := /home/jfkelly/Dropbox/Apps/Flashcards\ Deluxe

ui_%.py : %.ui
	pyuic5 -i 0 -o $@ $<

ui :  ui_wordsearch.py 

get-office:
	scp office:src/billboard/billboard.sqlite . ;\
	rsync -r office:src/billboard/data/* data/ ;\ 
	rsync -r office:src/billboard/*.csv . 

put-office:
	scp billboard.sqlite office:src/billboard/ ;\
	rsync -r *.csv office:src/billboard
	rsync -r data/* office:src/billboard/data ;\ 

