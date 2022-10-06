from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import json
import os
import babel
import dateutil.parser
import collections
import collections.abc
collections.Callable = collections.abc.Callable
import os

from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask import Flask



# db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


'''
Genre
'''
class Genre(db.Model):  
  __tablename__ = 'Genre'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  Books = db.relationship('Book', backref='Genre', lazy=True, cascade="all, delete")

  def __init__(self, name):
    self.name = name

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()


  def format(self):
    return {
      'id': self.id,
      'name': self.name
    }

'''
Books
'''
class Book(db.Model):  
  __tablename__ = 'Book'

  id = db.Column(db.Integer, primary_key=True)
  Genre_id = db.Column(db.Integer, db.ForeignKey('Genre.id'), nullable=False)
  book_name = db.Column(db.String)
  book_description = db.Column(db.String)

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()


  def format(self):
    return {
      'id': self.id,
      'Genre_id': self.Genre_id,
      'book_name': self.book_name,
      'book_description': self.book_description
      }