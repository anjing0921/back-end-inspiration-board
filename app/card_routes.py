from app import db
from app.models.board import Board
from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.card import Card


cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@cards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_model(Board, id)

    db.session.delete(board)
    db.session.commit()

    return make_response(f"Board #{id} successfully deleted")