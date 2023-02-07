from app import db
from app.models.board import Board
from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.card import Card


boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_Board():
    request_body = request.get_json()
    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board {new_board.title} successfully created", 201)

@boards_bp.route("", methods=["GET"])
def read_all_boards():
    board_query = Board.query
    title_query = request.args.get("title")
    if title_query:
        board_query = board_query.filter(Board.title.ilike(f"%{title_query}%"))
        
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "desc":
            board_query = board_query.order_by(Board.title.desc())
        else:
            board_query = board_query.order_by(Board.title.asc())

    boards = board_query.all()
    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())
    return jsonify(boards_response)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

@boards_bp.route("/<id>", methods=["GET"])
def read_one_board(id):
    board = validate_model(Board, id)
    return board.to_dict()

@boards_bp.route("/<id>", methods=["PUT"])
def update_board(id):
    board = validate_model(Board, id)

    request_body = request.get_json()
    board.title = request_body["title"]
    board.title = request_body["creator"]
    

    db.session.commit()
    
    return make_response(f"Board #{id} successfully updated")

@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_model(Board, id)

    db.session.delete(board)
    db.session.commit()

    return make_response(f"Board #{id} successfully deleted")

# Create a new Card for the board with id 

@boards_bp.route("/<id>/cards", methods=["POST"])
def add_new_card_to_board(id):
    board = validate_model(Board, id)

    request_body = request.get_json()
    new_card = Card.from_dict(request_body)
    new_card.board = board

    db.session.add(new_card)
    db.session.commit()

    message = f"Card {new_card.message} created with Board{board.title}"
    return make_response(jsonify(message), 201)
# Get all Cards for the board with id
@boards_bp.route("/<id>/cards", methods=["GET"])
def get_all_cards_for_board(id):
    board = validate_model(Board, id)

    cards_response = []
    for card in board.cards:
        cards_response.append(card.to_dict())

    return jsonify(cards_response)