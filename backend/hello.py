import os
from flask import Flask
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    def __init__(self, database='example', host=os.getenv("MYSQL_DB_HOST"), user=os.getenv("MYSQL_DB_USER"), password=os.getenv("MYSQL_DB_PASS"), port=os.getenv("MYSQL_DB_PORT")):
        # pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=password,
            host=host, # name of the mysql service as set in the docker compose file
            database=database,
            port=port,
            auth_plugin='mysql_native_password'
        )
        # pf.close()
        self.cursor = self.connection.cursor()
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (title VARCHAR(255))')
        self.cursor.execute('INSERT INTO blog (title) VALUES ("Hello Alibaba Cloud")')
        self.connection.commit()
    
    def query_titles(self):
        self.cursor.execute('SELECT title FROM blog')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


server = Flask(__name__)
conn = None

@server.route('/')
def listBlog():
    global conn
    if not conn:
        conn = DBManager()
        conn.populate_db()
    rec = conn.query_titles()

    response = ''
    for c in rec:
        response = response  + f'<h2>{c}</h2>'

    response = response + '<p><img src="https://nginx-flask-oss.oss-ap-southeast-5.aliyuncs.com/Alibaba-Cloud-logo.png" /></p>'
    print(response)
    return response


if __name__ == '__main__':
    server.run()
