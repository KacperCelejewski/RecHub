from flask import jsonify, make_response, request
from flask_login import login_required, current_user
from src.models.opinion import Opinion
from src.models.company import Company
from src.extensions import db
from sqlalchemy.exc import IntegrityError
from src.opinions import bp_opinion as bp
import datetime
from flask_jwt_extended import jwt_required,get_jwt_identity



@bp.route("/api/opinion/add", methods=["POST"])
@jwt_required()
def add_opinion():
    data = request.get_json()
    for key in data:
        if key == "" or data[key] == "":
            return make_response(jsonify({"message": f"Missing {key} parameter!"}), 400)

    try:
        company_id = int(data["company_id"])
        company = Company.query.filter_by(id=company_id).first()
    except ValueError:
        return make_response(
            jsonify({"message": "Company not found! Bad company id"}), 400
        )
    if company is None:
        return make_response(
            jsonify({"message": "Company not found! Bad company id"}), 400
        )
    current_user_id = get_jwt_identity()
    opinion = Opinion(
        title=data["title"],
        company_id=company_id,
        author_id=current_user_id,
        rating=data["rating"],
        content=data["content"],
        posted_date=datetime.datetime.now(),
    )
    opinion.censor_profanity()
    
    try:
        db.session.add(opinion)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return make_response(jsonify({"message": "Opinion already exists!"}), 409)

    return make_response(jsonify({"message": "Opinion added!"}), 201)

@bp.route("/api/opinions/<company_id>", methods=["GET"])
def get_opinions(company_id):
    opinions = Opinion.query.filter_by(company_id=company_id).all()
    if opinions is None:
        return make_response(jsonify({"message": "Opinions not found!"}), 404)
    opinions = [
        {
            "id": opinion.id,
            "title": opinion.title,
            "posted_date": opinion.posted_date,
            "content": opinion.content,
            "rating": opinion.rating,
            "author_id": opinion.author_id,
            "company_id": opinion.company_id,
        }
        for opinion in opinions
    ]
    return make_response(jsonify({"opinions": opinions}), 200)


@bp.route("/api/opinion/<id>", methods=["GET"])
@jwt_required()
def get_opinion(id):
    opinion = Opinion.query.filter_by(id=id).first()
    if opinion is None:
        return make_response(jsonify({"message": "Opinion not found!"}), 404)
    return make_response(jsonify({"opinion_id":opinion.id,"opinion_title":opinion.title,"posted_date":opinion.posted_date,"content":opinion.content,"rating":opinion.rating,"author_id":opinion.author_id,"company_id":opinion.company_id}), 200)

@bp.route("/api/opinion/<id>/edit", methods=["PUT"])
@jwt_required()
def edit_opinion(id):

        opinion = Opinion.query.filter_by(id=id).first()
        
        if opinion is None:
            return make_response(jsonify({"message": "Opinion not found!"}), 404)
        if current_user.id != opinion.author_id:
            return make_response(jsonify({"message": "You are not the author of this opinion!"}), 401)
        data = request.get_json()
        for key in data:
            if key == "" or data[key] == "":
                return make_response(jsonify({"message": f"Missing {key} parameter!"}), 400)
        opinion.title = data["title"]
        opinion.content = data["content"]
        opinion.rating = data["rating"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return make_response(jsonify({"message": "Opinion already exists!"}), 409)
        return make_response(jsonify({"message": "Opinion edited!"}), 201)


@bp.route("/api/opinion/<id>/delete", methods=["DELETE"])
@jwt_required()
def delete_opinion(id):
    opinion = Opinion.query.filter_by(id=id).first()
    if opinion is None:
        return make_response(jsonify({"message": "Opinion not found!"}), 404)
    if current_user.id != opinion.author_id:
        return make_response(jsonify({"message": "You are not the author of this opinion!"}), 401)
    db.session.delete(opinion)
    db.session.commit()
    return make_response(jsonify({"message": "Opinion deleted!"}), 200)
