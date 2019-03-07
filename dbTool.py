import pymysql
import config


class Database:
    def __init__(self):
        host = config.Default.host
        user = config.Default.user
        password = config.Default.password
        db = config.Default.db

        self.con = pymysql.connect(host=host, user=user, password=password, db=db,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def sql_commit(self):
        self.con.commit()
        return 'OK'

    def list_ranking(self):
        self.cur.execute("SELECT * FROM Ranking ORDER BY CID, GID, Ranking")
        result = self.cur.fetchall()

        return result

    def add_score(self, UID, GID, Score, Time, Manip, Time_score, Manip_score, CID):
        self.cur.execute('INSERT INTO user_score (UID, GID, Score, Time, Manip, Time_score, Manip_score, CID)'
                         ' VALUES (%d, %d, %d, %d, %d, %d, %d, %d);'
                         % (UID, GID, Score, Time, Manip, Time_score, Manip_score, CID))
        return 'OK'

    def update_score(self, UID, GID, Score, Time, Manip, Time_score, Manip_score, CID):
        self.cur.execute('''UPDATE user_score 
                            SET Score=%d, Time=%d, Manip=%d, Time_score=%d, Manip_score=%d, Ranking=NULL
                            WHERE UID=%d AND GID=%d AND CID=%d;'''
                         % (Score, Time, Manip, Time_score, Manip_score, UID, GID, CID))
        return 'OK'
    def update_ranking(self, GID, CID):
        # sql ranking command for MySQL 5.x
        sql_5 = '''
                UPDATE user_score
                SET Ranking = (
                    SELECT Ranking
                    FROM (
                        SELECT UID, GID, Score, CID, @curRank := @curRank + 1 AS Ranking
                        FROM user_score T, (SELECT @curRank := 0) r
                        WHERE CID = %d AND GID = %d
                    ) D
                    WHERE D.UID = user_score.UID AND D.GID = user_score.GID
                )
                WHERE CID = %d AND GID = %d;
        ''' % (CID, GID, CID, GID)

        # sql ranking command for MySQL 8.x
        sql_8 = '''
                UPDATE user_score
                SET Ranking = (
                    SELECT Ranking
                    FROM (
                        SELECT UID, GID, Score, CID, RANK() OVER(ORDER BY Score DESC) AS Ranking
                        FROM user_score T
                        WHERE CID = %d AND GID = %d
                    ) D
                    WHERE D.UID = user_score.UID AND D.GID = user_score.GID
                )
                WHERE CID = %d AND GID = %d;
        ''' % (CID, GID, CID, GID)

        self.cur.execute(sql_5)
        return 'OK'