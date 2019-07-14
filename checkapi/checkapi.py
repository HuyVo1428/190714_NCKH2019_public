import json
import sqlite3
from sqlite3 import Error
import requests
import safebrowsing
import os
import re
import time

class checkapi():

    def __init__(self, sourcedb, desdb, startiddb, stopiddb):
        self.sourcedb = sourcedb
        self.desdb = desdb
        self.stariddb = startiddb
        self.stopiddb = stopiddb

    def run(self):

        database = self.sourcedb 
        connt = sqlite3.connect(database)
        #create_database("result.sqlite")
        result = self.desdb 
        connt2 = sqlite3.connect(result)
        cur = connt.cursor()
        rows = cur.execute("SELECT url FROM http_requests")        
        # rows = cur.execute("SELECT url FROM http_requests WHERE id BETWEEN "+str(startid)+" AND "+str(stopid)+";")
        connt2.cursor().execute("""CREATE TABLE IF NOT EXISTS unsafe_url
                    (URL           TEXT    NOT NULL,
                    RESULT           TEXT    NOT NULL);""")
        
        for row in rows:
            url = row[0]
            print(url)
            apikey = 'AIzaSyArUsQxoVRRMQ4YhDR9ae51gWmuXsP5sw4'
            sb = safebrowsing.LookupAPI(apikey)
            resp = sb.threat_matches_find(url)
            if "matches" in resp:
                connt2.cursor().execute("""INSERT INTO unsafe_url
                (URL, RESULT)
                values (?,?)""",(str(url), str(resp)))
                connt2.commit()

    def create_connection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return None

    def follow(file):
        file.seek(0,2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.001)
                continue
            yield line

    def create_database(db_file):
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        return None

    def start(conn, conn2, startid, stopid):
        cur = conn.cursor()
        rows = cur.execute("SELECT url FROM http_requests")        
        # rows = cur.execute("SELECT url FROM http_requests WHERE id BETWEEN "+str(startid)+" AND "+str(stopid)+";")
        conn2.cursor().execute("""CREATE TABLE IF NOT EXISTS unsafe_url
                    (URL           TEXT    NOT NULL,
                    RESULT           TEXT    NOT NULL);""")
        
        for row in rows:
            url = row[0]
            print(url)
            apikey = 'AIzaSyArUsQxoVRRMQ4YhDR9ae51gWmuXsP5sw4'
            sb = safebrowsing.LookupAPI(apikey)
            resp = sb.threat_matches_find(url)
            if "matches" in resp:
                conn2.cursor().execute("""INSERT INTO unsafe_url
                (URL, RESULT)
                values (?,?)""",(str(url), str(resp)))
                conn2.commit()

