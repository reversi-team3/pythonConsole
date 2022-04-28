from mysql.connector import connect, Error

from database import DBManager


class ActiveGameManager:
    def __init__(self, db: DBManager):
        self.db = db
        query = """CREATE TABLE IF NOT EXISTS ActiveGames(
                    username1 char(255),
                    username2 char(255),
                    game JSON,
                    primary key (username1)
                    );"""

        with db.con.cursor() as cursor:
            cursor.execute(query)
            db.con.commit()

    def addGame(self, username1, username2, game):
        query = f"INSERT INTO ActiveGames (username1, username2, game) VALUES {username1, username2, game} ON DUPLICATE KEY UPDATE game=VALUES(game);"
        with self.db.con.cursor() as cursor:
            cursor.execute(query)
            self.db.con.commit()

    def updateGame(self, username1, username2, game):
        query1 = f"UPDATE ActiveGames SET game = null WHERE username1 = \"{username1}\";"
        with self.db.con.cursor() as cursor:
            cursor.execute(query1)
            self.db.con.commit()
        query2 = f"UPDATE ActiveGames SET game = \'{game}\' WHERE username1 = \"{username1}\";"
        with self.db.con.cursor() as cursor:
            cursor.execute(query2)
            self.db.con.commit()
