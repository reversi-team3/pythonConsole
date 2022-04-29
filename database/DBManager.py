from mysql.connector import connect, Error
from getpass import getpass


class DBManager:
    __instance = None

    @staticmethod
    def get_instance():
        if DBManager.__instance is None:
            DBManager.__instance = DBManager()
        return DBManager.__instance

    def __init__(self):
        #     self.conn = None
        if DBManager.__instance is not None:
            raise Exception("This class is a singleton")

        try:
            conn = connect(
                host='localhost',
                user='Team3',
                password="Team3"
            )
            print("DB Connected")
            query = """
                    CREATE DATABASE IF NOT EXISTS REVERSIDB1;
                    USE REVERSIDB1;
                    CREATE TABLE IF NOT EXISTS player(
                    username char(255),
                    pw char(255),
                    elo int DEFAULT 1500,
                    win int DEFAULT 0,
                    loss int DEFAULT 0,
                    tie int DEFAULT 0,
                    primary key (username)
                    );
                    CREATE TABLE IF NOT EXISTS game(
                    g_id int not null auto_increment,
                    turn int,
                    size int,
                    username char(255),
                    primary key (g_id),
                    foreign key (username) references player(username)  
                    );
                    CREATE TABLE IF NOT EXISTS leaderboard(
                    username char(255),
                    ranking int,
                    foreign key(username) references player(username)
                    );
                    CREATE TABLE IF NOT EXISTS disk(
                    xcoord int,
                    ycoord int,
                    value int,
                    g_id int,
                    color char(255),
                    foreign key (g_id) references game(g_id)
                    );
                    CREATE TABLE IF NOT EXISTS ActiveGames(
                    username1 char(255),
                    username2 char(255),
                    game JSON,
                    turn char(255),
                    primary key (username1)
                    );"""

            with conn.cursor() as cursor:
                lines = query.split(';')
                for line in lines:
                    cursor.execute(line)
                conn.commit()
            conn.close()
            # return 0  # 0 = Connection success
        except Error as e:
            print(e)
            # return 1  # 1 = Connection failed
        self.con = connect(
            host='localhost',
            user='Team3',
            password="Team3",
            database="REVERSIDB1"
        )

    # def dummyPlayer(self):
    #     query = "INSERT INTO player (username, pw) VALUES (%s,%s)"
    #     with self.con.cursor() as cursor:

    #         cursor.execute(query,('kihang','kim'))
    #         self.con.commit()

    # def get_player(self):
    #     query1 = "SELECT * FROM Players"
    # with self.conn.cursor() as cursor:
    #     cursor.execute(query1)

    def addPlayer(self, username, pw):
        query = "INSERT INTO player (username, pw) VALUES (%s, %s)"
        with self.con.cursor() as cursor:
            cursor.execute(query, (username, pw))
            self.con.commit()

    def checkPlayer(self, username):
        query = "select * from player where username = %s"

        with self.con.cursor() as cursor:
            cursor.execute(query, (username,))
            row = cursor.fetchall()
            return row

    def checkRank(self):
        query = "SELECT username FROM player ORDER BY win DESC LIMIT 10"

        with self.con.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
            return row

    def updateLeaderboard(self, username, rank):
        query = "INSERT INTO leaderboard (username, ranking) VALUES (%s, %s)"

        with self.con.cursor() as cursor:
            cursor.execute(query, (username, rank))
            self.con.commit()

    def getLeaderboard(self):
        query = "SELECT * FROM leaderboard"

        with self.con.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchall()
            return row

    # kihang add
    def addGame(self, username1, username2, game):
        query = f"INSERT INTO ActiveGames (username1, username2, game, turn) VALUES {username1, username2, game, username1} ON DUPLICATE KEY UPDATE game=VALUES(game);"
        with self.con.cursor() as cursor:
            cursor.execute(query)
            self.con.commit()

    def updateGame(self, username1, game, turn):
        query1 = f"UPDATE ActiveGames SET game = \'{game}\', turn = \'{turn}\'  WHERE username1 = \"{username1}\";"
        with self.con.cursor() as cursor:
            cursor.execute(query1)
            self.con.commit()
        # query2 = f"UPDATE ActiveGames SET game = null WHERE username2 = \"{username2}\";"
        # with self.con.cursor() as cursor:
        #     cursor.execute(query2)
        #     self.con.commit()

    def deleteGame(self, username1):
        query1 = f"DELETE FROM ActiveGames WHERE username1 = \'{username1}\';"
        with self.con.cursor() as cursor:
            cursor.execute(query1)
            self.con.commit()

    def checkGame(self, username):
        query = "select * from ActiveGames where username1 = %s"

        with self.con.cursor() as cursor:
            cursor.execute(query, (username,))
            row = cursor.fetchall()
            return row

    def getElo(self, username):
        query = "select elo from player where username1 = %s"

        with self.con.cursor() as cursor:
            cursor.execute(query, (username,))
            row = cursor.fetchall()
            return row