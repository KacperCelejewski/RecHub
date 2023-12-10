from src.extensions import db


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    location = (db.Column(db.String(120), nullable=False))
    ceo = (db.Column(db.String(120), nullable=False))
    description = (db.Column(db.String(120), unique=True, nullable=False))
    technology = (db.Column(db.String(120), nullable=False))
    industry = (db.Column(db.String(120), nullable=False))
    opinions = db.relationship("Opinion", backref="company", lazy=True)
    # recruiter = (
    #     (db.Column(db.relationship("Recruiter", backref="company", lazy=True))),
    # )
    # opinion = ((db.Column(db.relationship("Opinion", backref="company", lazy=True))),)
    def __repr__(self) -> str:
        return f"Company {self.name}"

