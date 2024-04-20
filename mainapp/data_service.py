from data_insertion import psql_client
from utilities import amount_crores, formated
import streamlit  as st
import pandas as pd
import psycopg2

@st.cache_data
def process_transaction_data(transaction_data_mp,state_id_map):
    
    transaction_data_mp['id'] = transaction_data_mp["State"].apply(lambda x: state_id_map[x])
    transaction_data_mp['Transaction_amount'] =  transaction_data_mp["Transaction_amount"].apply(lambda x: int(x))
    transaction_data_mp['All Transactions'] = transaction_data_mp['Transaction_count'].apply(lambda x: round(x)).apply(lambda x: formated(x))
    transaction_data_mp['Total Payment Values'] = transaction_data_mp['Transaction_amount'].apply(lambda x: round(x)).apply(lambda x: amount_crores(x))
    transaction_data_mp['Avg.Transaction Value'] = transaction_data_mp['Transaction_amount'] / transaction_data_mp['Transaction_count']
    transaction_data_mp['Avg.Transaction Value'] = transaction_data_mp['Avg.Transaction Value'].apply(lambda x: round(x)).apply(lambda x: "₹{:,.0f}".format(x))
    return transaction_data_mp

@st.cache_data
def process_user_data(user_data_mp,state_id_map):
    user_data_mp['State'] = user_data_mp['State'].str.title()
    user_data_mp['id'] = user_data_mp['State'].apply(lambda x:state_id_map[x])
    user_data_mp['Registered Users'] = user_data_mp['Count'].apply(lambda x: formated(round(x)) if pd.notnull(x) else '')
    return user_data_mp

def get_trans_method():
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = [
        "transaction_method_key",
        "transaction_method",
        "transaction_count",
        "transaction_amount",
        "quarter",
        "state_key",
        "year_key",
    ]
    try:
        cursor.execute("select * from phonepe.trans_method")
        tuples_list = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(
            tuples_list,columns=coluumn_names
        )
        return df
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()
            

def get_users_location():
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = [
        "user_location_key",
        "district_name",
        "users_count",
        "app_openig",
        "quarter",
        "state_key",
        "year_key",
    ]
    try:
        cursor.execute("select * from phonepe.users_location")
        tuples_list = cursor.fetchall()
        cursor.close()
        usr_df = pd.DataFrame(
            tuples_list,columns=coluumn_names
        )
        return usr_df
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()

