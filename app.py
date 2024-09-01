from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# new instance of the SentimentIntensityAnalyzer class
sia = SentimentIntensityAnalyzer()

# new instance of the Flask class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    review_text = db.Column(db.String(300), unique = True)
    score = db.Column(db.Integer, default = None)

def check_score(review):
    return sia.polarity_scores(review).get('compound')


@app.route("/")
def home():
    review_list = Review.query.all()
    print(review_list)
    return render_template("index.html", review_list = review_list)

@app.route("/add", methods=["POST"])
def add():
    review = request.form.get("review")
    new_review=Review(review_text = review, score = check_score(review))
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('home'))


if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)