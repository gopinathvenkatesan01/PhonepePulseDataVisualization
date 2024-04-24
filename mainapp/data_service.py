from data_insertion import psql_client
from utilities import amount_crores, formated
import streamlit as st
import pandas as pd
import psycopg2


@st.cache_data
def process_transaction_data(transaction_data_mp, state_id_map):

    transaction_data_mp["id"] = transaction_data_mp["State"].apply(
        lambda x: state_id_map[x]
    )
    transaction_data_mp["Transaction_amount"] = transaction_data_mp[
        "Transaction_amount"
    ].apply(lambda x: int(x))
    transaction_data_mp["All Transactions"] = (
        transaction_data_mp["Transaction_count"]
        .apply(lambda x: round(x))
        .apply(lambda x: formated(x))
    )
    transaction_data_mp["Total Payment Values"] = (
        transaction_data_mp["Transaction_amount"]
        .apply(lambda x: round(x))
        .apply(lambda x: amount_crores(x))
    )
    transaction_data_mp["Avg.Transaction Value"] = (
        transaction_data_mp["Transaction_amount"]
        / transaction_data_mp["Transaction_count"]
    )
    transaction_data_mp["Avg.Transaction Value"] = (
        transaction_data_mp["Avg.Transaction Value"]
        .apply(lambda x: round(x))
        .apply(lambda x: "₹{:,.0f}".format(x))
    )
    return transaction_data_mp


@st.cache_data
def process_user_data(user_data_mp, state_id_map):
    user_data_mp["State"] = user_data_mp["State"].str.title()
    user_data_mp["id"] = user_data_mp["State"].apply(lambda x: state_id_map[x])
    user_data_mp["Registered Users"] = user_data_mp["Count"].apply(
        lambda x: formated(round(x)) if pd.notnull(x) else ""
    )
    return user_data_mp


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
        "year_id",
        "year",
        "state_id",
        "state_name",
    ]
    try:
        cursor.execute(
            """SELECT * FROM phonepe.users_location u 
    INNER JOIN phonepe.year y ON  y.id = u.year_key  
    INNER JOIN phonepe.state s ON s.id = u.state_key;"""
        )
        tuples_list = cursor.fetchall()
        cursor.close()
        usr_df = pd.DataFrame(tuples_list, columns=coluumn_names)
        return usr_df
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()


def get_transaction_data():
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
        "year_id",
        "year",
        "state_id",
        "state_name",
    ]
    try:
        cursor.execute(
            """SELECT * FROM phonepe.trans_location t 
    INNER JOIN phonepe.year y ON y.id = t.year_key
    INNER JOIN phonepe.state s ON  s.id = t.state_key
     ORDER BY y.year;"""
        )
        tuples_list = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(tuples_list, columns=coluumn_names)
        return df
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()


def agg_transcn(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["transaction_method", "sum"]
    try:
        cursor.execute(
            f"""SELECT transaction_method, SUM(transaction_count) 
    FROM phonepe.trans_method t
    INNER JOIN phonepe.year y ON y.id = t.year_key
    WHERE  quarter = %s AND y.year = %s
    GROUP BY transaction_method 
    ORDER BY transaction_method""",
            (int(quarter), int(year)),
        )
        tuples_list = cursor.fetchall()
        cursor.close()
        agg_trans = pd.DataFrame(tuples_list, columns=coluumn_names)
        return agg_trans
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()


def user_chart_data():
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
        "year",
        "state_name"
    ]
    try:
        cursor.execute(
            """SELECT u.*,y.year,s.state_name FROM phonepe.users_location u 
            INNER JOIN phonepe.year y ON y.id = u.year_key 
            INNER JOIN phonepe.state s ON s.id = u.state_key """
        )
        tuples_list = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(tuples_list, columns=coluumn_names)
        return df
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()


def trans_chart_data():
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = [
        "trans_location_id",
        "district_name",
        "total_transaction_count",
        "total_transaction_amount",
        "quarter",
        "state_key",
        "year_key",
        "year",
        "state_name"
    ]
    try:
        cursor.execute(
            """SELECT t.*,y.year,s.state_name FROM phonepe.trans_location t 
            INNER JOIN phonepe.year y ON y.id = t.year_key 
            INNER JOIN phonepe.state s ON s.id = t.state_key;"""
        )
        tuples_list = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(tuples_list, columns=coluumn_names)
        return df
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()
