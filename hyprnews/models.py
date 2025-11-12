from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class Article(db.Model):
    __tablename__ = 'news'
    id      = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    title   = db.Column(db.String(200), nullable=False)
    body    = db.Column(db.Text, nullable=False)
    url     = db.Column(db.String(500))
    # author  = db.Column(db.String(100))

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Article {self.id} {self.title!r}>'

