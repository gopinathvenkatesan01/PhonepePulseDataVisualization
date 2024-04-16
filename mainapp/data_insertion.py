import psycopg2
from psycopg2 import sql
import uuid
import streamlit as st
from data_extraction import aggregated_transcn_st,map_user_st,map_transcation_st,arrgregated_usr_st



def psql_client():
    try:
        connection = psycopg2.connect(host='localhost',
                user='postgres',
                password='admin',
                database='phonepe')
        return connection
    except Exception as e:
        print(e)

def init():
    data_insertion.configure_database()
    data_insertion.insert_data()
    

class data_insertion():
    
    def create_database(tenant_id):
      conn = psycopg2.connect(database="postgres", user="postgres", password="admin", host="localhost")
      cursor = conn.cursor()
      conn.autocommit = True
      dbname = sql.Identifier(tenant_id)
      create_cmd = sql.SQL('CREATE DATABASE {}').format(dbname)
      drop_db = sql.SQL('DROP DATABASE IF EXISTS{}').format(dbname)
      cursor.execute(drop_db)
      cursor.execute(create_cmd)
      cursor.close()
      conn.close()
      
      

    
    def configure_database():
        try:
            # Create the 'phonepe' database if it doesn't exist
            data_insertion.create_database('phonepe')

            # Connect to the database
            connection = psql_client()
            cursor = connection.cursor()

            # Read the SQL script to create tables
            with open('table_script.sql', 'r') as file:
                sql = file.read()
                # Execute the SQL script
                cursor.execute(sql)

            # Commit the transaction
            connection.commit()

        except (psycopg2.Error, Exception) as e:
            # Handle database-related errors
            print("An error occurred:", e)

        finally:
            # Close cursor and connection in the 'finally' block
            if 'connection' in locals():
                # Close the cursor
                cursor.close()
                # Close the connection
                connection.close()
    



    def insert_data():
        connection = None
        # trans_method_insert
        try:
            agg_transcn,state_df = aggregated_transcn_st()
            connection = psql_client()
            cursor = connection.cursor()
            states_list = agg_transcn['State'].unique().tolist()
            states_list_tuples = [(state,) for state in states_list]
            if states_list is not None:
                cursor.executemany(f"""INSERT INTO phonepe.state(state_name)VALUES (%s);""",states_list_tuples)
                connection.commit()


            year_list = agg_transcn['Year'].unique().tolist()
            for year_value in year_list:
                cursor.execute(f"""INSERT INTO phonepe.year(year)VALUES ({year_value});""") 
                connection.commit() 

            for index, row in agg_transcn.iterrows():
                # Get state_id
                state_name = row['State']
                cursor.execute(f"SELECT id FROM phonepe.state WHERE state_name='{state_name}'")
                state_id = cursor.fetchone()[0]
                cursor.fetchall()
                # Get year_id
                year_value = row['Year']
                cursor.execute(f"SELECT id FROM phonepe.year WHERE year={year_value}")
                year_id = cursor.fetchone()[0]
                cursor.fetchall()  # Fetch all results to clear the unread result
                # Insert transaction data
                cursor.execute(f"INSERT INTO phonepe.trans_method (transaction_method_key, transaction_method, transaction_count, transaction_amount, quarter, state_key, year_key) VALUES ('{uuid.uuid4()}','{row['Transaction_type']}', {row['Transaction_count']}, {row['Transaction_amount']},{row['Quarter']}, {state_id}, {year_id})")
                connection.commit()   
        except (psycopg2.Error, Exception) as e:
            st.write("An error occurred:", e)
        finally:
            if connection:
                connection.close()    
                
     #user location insert 
        try:
            agg_user = map_user_st()
            connection = psql_client()
            cursor = connection.cursor()

            for index, row in agg_user.iterrows():
                # Get state_id
                state_name = row['State']
                cursor.execute(f"SELECT id FROM phonepe.state WHERE state_name='{state_name}'")
                state_id = cursor.fetchone()[0]
                cursor.fetchall()
                # Get year_id
                year_value = row['Year']
                cursor.execute(f"SELECT id FROM phonepe.year WHERE year={year_value}")
                year_id = cursor.fetchone()[0]
                cursor.fetchall()  # Fetch all results to clear the unread result
                # Insert transaction data
                cursor.execute(f"""INSERT INTO phonepe.users_location(user_location_key,
                               district_name,
                               users_count,
                               app_openig,
                               quarter,
                               state_key,
                               year_key)
	                            VALUES ('{uuid.uuid4()}','{row['District']}',{row['Count']},{row['App_Opening']},{row['Quarter']},{state_id},{year_id});""")
                connection.commit()   
        except (psycopg2.Error, Exception) as e:
            st.write("An error occurred:", e)
        finally:
            if connection:
                connection.close()   
                
    # trans location insert
    
        try:
            mp_transcn = map_transcation_st()
            connection = psql_client()
            cursor = connection.cursor()

            for index, row in mp_transcn.iterrows():
                # Get state_id
                state_name = row['State']
                cursor.execute(f"SELECT id FROM phonepe.state WHERE state_name='{state_name}'")
                state_id = cursor.fetchone()[0]
                cursor.fetchall()
                # Get year_id
                year_value = row['Year']
                cursor.execute(f"SELECT id FROM phonepe.year WHERE year={year_value}")
                year_id = cursor.fetchone()[0]
                cursor.fetchall()  # Fetch all results to clear the unread result
                # Insert transaction data
                cursor.execute(f"""INSERT INTO phonepe.trans_location(trans_location_id, 
                               district_name, 
                               total_transaction_count,
                               total_transaction_amount,
                               quarter, 
                               state_key,
                               year_key)
	                           VALUES('{uuid.uuid4()}','{row['District']}',{row['Transaction_count']},{row['Transaction_amount']},{row['Quarter']},{state_id},{year_id});""")
                connection.commit()   
        except (psycopg2.Error, Exception) as e:
            st.write("An error occurred:", e)
        finally:
            if connection:
                connection.close()   
                
        # users_device_insert
        try:
            agg_usr = arrgregated_usr_st()
            connection = psql_client()
            cursor = connection.cursor()
            
            for index, row in agg_usr.iterrows():
                # Get state_id
                state_name = row['State']
                cursor.execute(f"SELECT id FROM phonepe.state WHERE state_name='{state_name}'")
                state_id = cursor.fetchone()[0]
                cursor.fetchall()
                # Get year_id
                year_value = row['Year']
                cursor.execute(f"SELECT id FROM phonepe.year WHERE year={year_value}")
                year_id = cursor.fetchone()[0]
                cursor.fetchall()  # Fetch all results to clear the unread result
                # Insert transaction data
                cursor.execute(f"""INSERT INTO phonepe.users_device(user_device_key,
                               device_brand_name,
                               brand_count, 
                               percentage,
                               no_of_users, 
                               app_opening, 
                               quarter,
                               state_key,
                               year_key)
	                           VALUES (
                                '{uuid.uuid4()}',
                                '{row['Brands']}',
                                 {row['Count']},
                                {row['Percentage']}, 
                                {row['Users_count']},
                                {row['App_opening']},
                                {row['Quarter']}, 
                                {state_id}, 
                                {year_id})""")
                connection.commit()   
        except (psycopg2.Error, Exception) as e:
            st.write("An error occurred:", e)
        finally:
            if connection:
                connection.close()     
    