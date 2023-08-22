
DROPHOME := /home/jfkelly/Dropbox/Apps/Flashcards\ Deluxe

ui_%.py : %.ui
	pyuic5 -i 0 -o $@ $<

ui :  \
	ui_wordsearch.py ui_dict.py\
	ui_refinfo.py ui_phrase.py \
	ui_quizwindow.py ui_prefs.py \
	ui_flashcard.py  ui_cardquiz.py \
	ui_verb.py ui_verbquiz.py ui_verbinfo.py \
	ui_exprquiz.py ui_exprframe.py  \
	ui_structure.py ui_structwidget.py  ui_structframe.py ui_structsel.py ui_structwin.py \
	ui_stats.py \
	ui_document.py ui_docselect.py  ui_highlight.py \
	ui_recogframe.py \
	ui_expression.py \
	ui_translate.py \
	ui_phrase.py ui_record.py 


get-office:
	scp office:src/billboard/billboard.sqlite . ;\
	rsync -r office:src/billboard/*.csv . 

get-tarball:
	scp office:src/pdict/inet.tar.xz .

put-office:
	scp billboard.sqlite office:src/billboard/ ;\
	rsync -r *.csv office:src/billboard

	rsync -r data/mp3/* office:src/pdict/data/mp3 

put-tarball:
	scp inet.tar.xz office:src/pdict/
