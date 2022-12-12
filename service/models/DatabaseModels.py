from flask_security import RoleMixin, UserMixin
from controllers.SetupController import db

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Article(db.Model):
    __tablename__ = "article"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(255), unique=False, nullable=True)
    content = db.Column(db.Text(10000), nullable=False)
    time = db.Column(db.Time, nullable=False)
    id_source = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)


class MediaSequence(db.Model):
    __tablename__ = "media_sequence"

    id = db.Column(db.Integer, primary_key=True)
    id_media = db.Column(db.Integer, db.ForeignKey('media.id'), nullable=True)
    id_article = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=True)


class MediaType(db.Model):
    __tablename__ = "media_type"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text(255), unique=True, nullable=False)


class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    media_link = db.Column(db.String(190), unique=False, nullable=False)
    id_media_type = db.Column(db.Integer, db.ForeignKey('media_type.id'), nullable=False)


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)


class SourceTag(db.Model):
    __tablename__ = "source_tag"

    id_source_tag = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text(255), unique=True, nullable=False)


class SourceTags(db.Model):
    __tablename__ = "source_tags"

    id = db.Column(db.Integer, primary_key=True)
    id_source = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
    id_source_tag = db.Column(db.Integer, db.ForeignKey('source_tag.id'), nullable=False)


class Source(db.Model):
    __tablename__ = "source"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(190), unique=True, nullable=False)
    name = db.Column(db.Text(255), nullable=False)
    id_url_type = db.Column(db.Integer, db.ForeignKey('url_type.id'), nullable=True)


class UrlType(db.Model):
    __tablename__ = "url_type"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text(255), unique=False, nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
