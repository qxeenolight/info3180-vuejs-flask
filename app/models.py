# Add any model classes for Flask-SQLAlchemy here
import base64
import os
from app import app
from . import db
from datetime import datetime
class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.String(1024))
    poster = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, title, description, poster, created_at):
        self.title = title
        self.description = description
        self.poster = poster
        self.created_at = created_at

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicodedata(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def get_image_url(self):
        with open(os.path.join(app.config['UPLOAD_FOLDER'], self.filename), 'rb') as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
        return f'data:image/jpeg;base64,{encoded_image}'
    
    def __repr__(self):
        return '<Movies %r>' % (self.title)