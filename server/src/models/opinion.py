from src.extensions import db
from better_profanity import profanity


class Opinion(db.Model):
    __tablename__ = "opinion"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)
    posted_date = db.Column(db.DateTime, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Opinion {self.title}"

    def censor_profanity_content(self) -> str:
        plain_content = self.content
        if profanity.contains_profanity(plain_content):
            self.content = profanity.censor(plain_content)
            print(f"Profanity detected in {plain_content}! Censoresd to {self.content}")
            return self.content
        else:
            return self.content

    def censor_profanity_title(self) -> str:
        plain_title = self.title
        if profanity.contains_profanity(plain_title):
            self.title = profanity.censor(plain_title)
            print(f"Profanity detected in {plain_title}! Censoresd to {self.title}")
            return self.title
        else:
            return self.title

    def censor_profanity(self):
        self.censor_profanity_content()
        self.censor_profanity_title()
