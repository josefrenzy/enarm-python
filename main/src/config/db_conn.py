import mysql.connector

from mysql.connector import errorcode
from timeit import default_timer as timer

from main.src.logger.app_logging import getlogger


class DBUtils():

    logger = getlogger(__name__)

    def getConnetion(self):
        while True:

            try:
                cnx = mysql.connector.connect(user='admin', password='e5Db4iDRtio927gJ6Zbg',
                                              host='enarm.c8isscxvh2mb.us-east-1.rds.amazonaws.com ',
                                              database='enarm_dev')
                return cnx

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)

    def execute_query(self, query, print_query=True, return_result=True):
        query_result = None
        try:
            db_conn = self.getConnetion()

            if print_query:
                self.logger.debug('Entry on db: {} for query: \n'.format(
                    type(db_conn), str(query)[:5000]
                ))
            start = timer()
            cursor = db_conn.cursor()
            cursor.execute(query)

            if return_result:
                query_result = {
                    "rows": [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                }
            else:
                query_result = True
            cursor.close()
            end = timer()
            self.logger.debug(
                'SQL execution {diff}'.format(diff=str(end-start)))
            self.logger.debug('Exit: normal.')
            return query_result
        except mysql.connector.DatabaseError as err:
            self.logger.debug(err)
            try:
                db_conn
            except NameError as e:
                self.logger(e)
            else:
                db_conn.close()
