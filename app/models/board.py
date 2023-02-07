from app import db


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        board_dict = {
            "board_id" : self.board_id,
            "owner": self.owner,
            "title": self.title,
        }
        if self.cards:
            board_dict["cards"] = [card.to_dict() for card in self.cards]

        return board_dict