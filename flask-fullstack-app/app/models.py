from datetime import datetime
from hashlib import md5
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(64))
    background_image = db.Column(db.String(64))
    digest_email = db.Column(db.String(128))
    registered_date = db.Column(db.DateTime, default=datetime.utcnow)
    account_type = db.Column(db.String(64), default='free')
    collection_count = db.Column(db.Integer, default=0)
    item_count = db.Column(db.Integer, default=0)
    collections = db.relationship('Collection', backref='author', lazy='dynamic')
    items = db.relationship('Item', backref='author', lazy='dynamic')
    images = db.relationship('Image', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_digest(self, digest):
        self.digest_email = digest

    def avatar(self, size):
        digest = md5(self.digest_email.lower().encode('utf-8')).hexdigest()
        if self.profile_image:
            return self.profile_image
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_collections(self):
        return Collection.query.filter_by(user_id=self.id)

    def get_items(self):
        return Item.query.filter_by(user_id=self.id)

# Collections Model
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    description = db.Column(db.String(140))
    visibility = db.Column(db.String(140), index=True, default='Private')
    item_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item', backref='collection', lazy='dynamic')
    images = db.relationship('Image', backref='collection', lazy='dynamic')

    def __repr__(self):
        return '<Collection {}>'.format(self.name)

# Items Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(140), index=True)
    description = db.Column(db.String(140))
    category = db.Column(db.String(140))
    custom = db.Column(db.Text(4294000000))
    collection_name = db.Column(db.String(140))
    category = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    images = db.relationship('Image', backref='item', lazy='dynamic')

    def __repr__(self):
        return '<Item {}>'.format(self.name)

    def get_images(self, id):
        images = Image.query.filter_by(item_id=id).all()
        if not images:
            return [{"name":"../static/images/no-img.jpg"}]
        else:
            return Image.query.filter_by(item_id=id).all()

# Images Model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

    def __repr__(self):
        return '<Image {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))