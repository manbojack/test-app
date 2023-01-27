import os
import psycopg2
from flask import Flask, request

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('TEST_APP_DB_SERVICE_HOST'),
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    return conn


def create_table(table):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {table};')
    cur.execute(f'CREATE TABLE {table} (id serial PRIMARY KEY,' 'value varchar (16));')
    conn.commit()
    cur.close()
    conn.close()


@app.route('/')
def write_ip_to_db(table='ip'):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
    except:
        return 'ERROR: not connected to database!'
    client_ip = str(request.remote_addr)
    try:
        cur.execute(f"INSERT INTO {table} (value) VALUES (\'{client_ip}\')")
    except:
        try:
            create_table(table)
        except:
            return f'ERROR: can\'t create table {table}!'
        return f'INFO: table {table} was created. Press F5 for refresh page.'
    conn.commit()
    cur.close()
    conn.close()
    return f'ip {client_ip} added to database'


@app.route('/get_all_ip')
def get_all_ip(table='ip'):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
    except:
        return 'ERROR: not connected to database!'
    try:
        cur.execute(f'SELECT * FROM {table};')
    except:
        try:
            create_table(table)
        except:
            return f'ERROR: can\'t create table {table}!'
        return f'INFO: table {table} was created. Press F5 for refresh page.'
    all_ip = cur.fetchall()
    cur.close()
    conn.close()
    return f'{all_ip}'
