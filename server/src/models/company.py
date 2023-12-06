from src.extensions import db


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = (db.Column(db.String(120), nullable=False),)
    ceo = (db.Column(db.String(120), nullable=False),)
    description = (db.Column(db.String(120), unique=True, nullable=False),)
    # recruiter = (
    #     (db.Column(db.relationship("Recruiter", backref="company", lazy=True))),
    # )
    # opinion = ((db.Column(db.relationship("Opinion", backref="company", lazy=True))),)

    def __repr__(self):
        return f"Company('{self.name}', '{self.location}', '{self.ceo}', '{self.description}', '{self.recruiter}', '{self.opinion}', '{self.likes}')"
