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
    representatives = db.relationship("Representative", backref="company", lazy=True)
    
    def __repr__(self) -> str:
        return f"Company {self.name}"
    
    
class Logo(db.Model):
    __tablename__ = "logo"
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.LargeBinary, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    mimetype = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return f"Logo {self.logo}"
    

