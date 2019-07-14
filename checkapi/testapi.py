import json
import sqlite3
from sqlite3 import Error
import requests
import safebrowsing
import os
import re
import time




# url = "http://wunmanchishome.com"
# print(url)
# apikey = 'AIzaSyArUsQxoVRRMQ4YhDR9ae51gWmuXsP5sw4'
# sb = safebrowsing.LookupAPI(apikey)
# resp = sb.threat_matches_find(url)
# print(str(resp))

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


database = "../database/requestdata3/crawl-data.sqlite"
connt = create_connection(database)

result = "../database/apichecked/result.sqlite"
connt2 = create_connection(result)


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