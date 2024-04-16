from data_extraction import extract_data, geo_json
import psycopg2
import streamlit as st
from psycopg2 import sql

def extract_and_store_data():
    create_database('phonepe')
    configure_database()
    india_state,state_id_map,state_df = geo_json()
    transaction_data_mp = extract_data()
    connection = psql_client()
    cursor = connection.cursor()
    
    
def psql_client():
    try:
        connection = psycopg2.connect(host='localhost',
                user='postgres',
                password='admin',
                database='phonepe')
        return connection
    except Exception as e:
        st.warning(e)    
    
def configure_database():
    connection = psql_client()
    cursor = connection.cursor()
    
    with open('your_sql_file.sql', 'r') as file:
        sql = file.read()
        cursor.execute(sql)
    
    # Commit the transaction
    connection.commit()

    # Close cursor and connection
    connection.close()
    connection.close()
    
def create_database(tenant_id):
  conn = psycopg2.connect(database="postgres", user="postgres", password="admin", host="localhost")
  cursor = conn.cursor()
  conn.autocommit = True #!
  dbname = sql.Identifier(tenant_id)
  create_cmd = sql.SQL('CREATE DATABASE {}').format(dbname)
  drop_db = sql.SQL('DROP DATABASE IF EXISTS{}').format(dbname)
  cursor.execute(drop_db)
  cursor.execute(create_cmd)
  cursor.close()
  conn.close()
