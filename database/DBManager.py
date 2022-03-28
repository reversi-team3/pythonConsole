from mysql.connector import connect, Error
from getpass import getpass


class DBManager:
    def __init__(self):
        #     self.conn = None

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
                    DROP TABLE IF EXISTS leaderboard;
                    DROP TABLE IF EXISTS disk;
                    DROP TABLE IF EXISTS game;
                    DROP TABLE IF EXISTS player;
                    
                    CREATE TABLE IF NOT EXISTS player(
                    username char(255),
                    pw char(255),
                    elo int DEFAULT 0,
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
                    
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user2', '1234', 29, 0,72,22);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user3', '1234', 29, 100,2,23);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user4', '1234', 12, 15,23,24);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user5', '1234', 12, 19,7,21);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user6', '1234', 62, 91,7,22);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user7', '1234', 12, 31,76,21);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user8', '1234', 27, 21,5,20);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user9', '1234', 12, 523,4,2);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user10','1234', 2, 1,3,2);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user11','1234', 12, 134,72,2);
                    INSERT INTO player (username, pw, elo, win, loss, tie) VALUES ('user12','1234', 23, 1,7,2);"""

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
