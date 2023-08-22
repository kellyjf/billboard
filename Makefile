
DROPHOME := /home/jfkelly/Dropbox/Apps/Flashcards\ Deluxe

ui_%.py : %.ui
	pyuic5 -i 0 -o $@ $<

ui :  ui_wordsearch.py 

get-office:
	scp office:src/billboard/billboard.sqlite . ;\
	rsync -r office:src/billboard/*.csv . 

get-tarball:
	scp office:src/pdict/inet.tar.xz .

put-office:
	scp billboard.sqlite office:src/billboard/ ;\
	rsync -r *.csv office:src/billboard

put-tarball:
	scp inet.tar.xz office:src/pdict/
