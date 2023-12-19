from src.extensions import db
import os


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    location = db.Column(db.String(120), nullable=False)
    ceo = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    technology = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120), nullable=False)
    opinions = db.relationship("Opinion", backref="company", lazy=True)
    representatives = db.relationship("Representative", backref="company", lazy=True)
    website = db.Column(db.String(120))

    def average_rating(self):
        sum = 0
        for opinion in self.opinions:
            sum += opinion.rating
        if len(self.opinions) > 0:
            return sum / len(self.opinions)
        else:
            return "No ratings yet"

    def __repr__(self) -> str:
        return f"Company {self.name}"


class Logo(db.Model):
    __tablename__ = "logo"
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    mimetype = db.Column(db.String(120), nullable=False)

    def check_mimetype(self):
        if self.mimetype == "image/jpeg" or self.mimetype == "image/png":
            return True
        else:
            return False

    def check_size(self):
        file_size = os.path.getsize(self.logo)
        if file_size > 1000000:
            return False
        else:
            return True

    def __repr__(self) -> str:
        return f"Logo {self.logo}"
