import psycopg2
import traceback
import time
import json
import base64
import threading

class Postgresql:
    """interface DB class
    
    method:
        connection() -- connect DB
        listen(str) -- start listen DB trigger
        receive_notify() -- receive notify data
        close() -- close dababase connection
        sql_exec(str) -- execute SQL 
    """
    
    def __init__(self, server="127.0.0.1", port=5432, dbname="XXXXXXX", username="XXXXXX", password="XXXXXXXX"):
        self._conn_info = 'host=' + server + ' port=' + str(port) + ' dbname=' + dbname + ' user=' + username + ' password=' + password
        self._connection = None

    def connection(self):
        """connect DB
        
        return:
            True: connect ok
            False: connect failed
        """
        try:
            self._connection = psycopg2.connect(self._conn_info)
            self._connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            return True
        except:
            return False

    def listen(self, trigger):
        """start listen DB trigger
        
        paramater:
            trigger <str> -- trriger name
        return:
            True: able to notify listen
            False: unable to notify listen
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(trigger)
            cursor.close()
            return True
        except:
            return False

    def receive_notify(self):
        """receive notify data
        
        return:
            lsit -- receive notify data list
        """
        try:
            self._connection.poll()
            notify_list = []
            while self._connection.notifies:
                notify_list.append(self._connection.notifies.pop(0))
        except:
            if self._connection is not None and not self._connection.closed:
                self.close()
        finally:
            return notify_list

    def close(self):
        """close dababase connection"""
        self._connection.close()

    #def sql_exec(self, sql):
        """execute SQL
        paramater:
            sql <str> -- sql statement to execute
        return:
        pass
        """
    def sql_exec(self,sql):
        cursor = self._connection.cursor()
        #result = cursor.execute('SELECT image FROM tbl_save_image')
        # ここではsql文を実行しているだけで結果を受け取ってはいない
        cursor.execute(sql)
        # ここでcursorからデータをfetchする
        # result = cursor.fetchone()  # 最初の1件のみ取得
        if 'SELECT' in sql:
            print("--SELECT START--")
            result = cursor.fetchall()  # 全件取得
            #print(result)
            print("--SELECT END--")
            return result
        else:
            return 0

