#!/usr/bin/python3

#
# SQLAlchemy creates an object heirarchy that adapts python code classes
# to DB tables.  By subclassing all these adapter objects from a declariative
# base table, code can traverse the object tree to detect the structure of 
# the object heirarchy, and create schema DDL so that the database can be created
# from the derived SQL
#
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

#
# The classes represent tables, and they contain members for the columns
# and constraints of the table.  These are instances of classes that are available 
# in the main sqlalchemy module
from sqlalchemy import Table, Index, Column, Boolean, Integer, String, Float, Unicode, DateTime, ForeignKey, func
import string

from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import ForeignKeyConstraint

class Artist(Base):
	__tablename__ = "artists"

	id = Column(Integer, primary_key=True)
	text = Column(String)
	def __repr__(self):
		return f"Artist({self.id!r},{self.text!r})" 
class Song(Base):
	__tablename__ = "songs"
	id = Column(Integer, primary_key=True)
	artist_id= Column(String, ForeignKey("artists.id"))
	text = Column(String)
	peak= Column(Integer)
	date = Column(DateTime)
	weeks= Column(Integer)
	url = Column(String)
	def __repr__(self):
		return f"Song({self.id!r},artist={self.artist.text},{self.text!r})" 

Song.artist = relationship("Artist", uselist=False, back_populates="songs")
Artist.songs = relationship("Song", back_populates="artist")

class Entry(Base):
	__tablename__ = "entries"
	id = Column(Integer, primary_key=True)
	song_id= Column(Integer, ForeignKey("songs.id"))
	date = Column(DateTime, index=True)
	rank= Column(Integer)
	peak= Column(Integer, index=True)
	weeks= Column(Integer)

Song.entries = relationship("Entry",  back_populates="song")
Entry.song = relationship("Song", uselist=False,  back_populates="entries")
Index('ix_entries_song_rank', Entry.song_id, Entry.rank)

class Url(Base):
	__tablename__ = "urls"
	id = Column(Integer, primary_key=True)
	song_id= Column(Integer, ForeignKey("songs.id"))
	url = Column(String)

Song.urls = relationship("Url", back_populates="song")
Url.song = relationship("Song", uselist=False, back_populates="urls")
#Artist.entries = relationship("Entry",  back_populates="artist")
#Entry.artist = relationship("Artist", uselist=False,  back_populates="entries")

from sqlalchemy import create_engine, not_
engine=create_engine("sqlite:///billboard.sqlite")
Base.metadata.create_all(engine)

#from sqlalchemy.orm import Session
#Session=sessionmaker(engine)
Session=sessionmaker(engine, autoflush=False)

session=Session()
_quiet=False

if __name__ == "__main__":
	from argparse import ArgumentParser as ap
	parser=ap()
	parser.add_argument("--list","-l", action="store_true", help="List Database")
	args=parser.parse_args()



