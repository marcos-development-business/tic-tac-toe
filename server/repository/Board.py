import sqlite3
import uuid


class Board:
    def __init__(self):
        try:
            self.connection = sqlite3.connect("database.db")
        except Exception:
            raise Exception("Cannot connect to database")

    def create(self) -> str | None:
        board_id = str(uuid.uuid4())

        try:
            cursor = self.connection.cursor()
            for row in range(3):
                for column in range(3):
                    column_id = str(uuid.uuid4())
                    cursor.execute(f"""
                        INSERT INTO boards (board_id, id, value, posX, posY) VALUES (
                            ?, ?, null, ?, ?
                        )
                    """, (board_id, column_id, column, row))
                    self.connection.commit()
        except Exception as e:
            print("Exception ", e)
            return None

        return board_id

    def mark_board_position(self, row: int, column: int, board_id: str, player: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM boards WHERE board_id = ? AND posX = ? AND posY = ?", (board_id, column, row))

            rows = cursor.fetchall()

        except Exception:
            raise Exception("Cannot mark, try again later")

        if len(rows) != 1:
            raise Exception("This position not exists")

        if rows[0][2] is not None:
            raise Exception("This position already is marked")

        try:
            cursor.execute("""
                UPDATE boards SET value = ? WHERE board_id = ? AND posX = ? AND posY = ?
            """, (str(player), board_id, column, row))
            self.connection.commit()
        except Exception:
            raise Exception("Cannot mark, try again later")

    def get_board(self, board_id: str) -> list:
        try:
            print(board_id)
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM boards WHERE board_id = ?", (str(board_id),))

            boards = cursor.fetchall()
        except Exception as e:
            print(e)
            raise Exception("Cannot get board, try again later")

        if len(boards) == 0:
            raise Exception("This board not exist")

        board_matrix = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

        for board in boards:
            row = board[4]
            column = board[3]
            value = board[2]
            board_matrix[row][column] = value

        return board_matrix
