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
        "state_name",
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
        "state_name",
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


# top 10 states_transcn
def top_states_transcn(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["state_name", "sum"]
    try:
        cursor.execute(
            f"""SELECT s.state_name, SUM(tl.total_transaction_count)
FROM phonepe.trans_location tl 
INNER JOIN phonepe.year y ON y.id = tl.year_key 
INNER JOIN phonepe.state s ON s.id = tl.state_key
WHERE quarter = %s AND y.year = %s
GROUP BY s.state_name
ORDER BY SUM(tl.total_transaction_count) DESC LIMIT 10;""",
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


# top 10 district transcn
def top_districts_transcn(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["district_name", "sum"]
    try:
        cursor.execute(
            f"""SELECT  tl.district_name, SUM(tl.total_transaction_count)
FROM phonepe.trans_location tl 
INNER JOIN phonepe.year y ON y.id = tl.year_key 
INNER JOIN phonepe.state s ON s.id = tl.state_key
WHERE quarter = %s AND y.year = %s 
GROUP BY tl.district_name
ORDER BY SUM(tl.total_transaction_count) DESC LIMIT 10;""",
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


# top 10 pincode transaction


def top_pincodes_transcn(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["pincode", "transaction_amount"]
    try:
        cursor.execute(
            f"""SELECT  pt.pincode, SUM(pt.total_transaction_count)
FROM phonepe.pincode_table_transaction pt 
INNER JOIN phonepe.year y ON y.id = pt.year_key 
INNER JOIN phonepe.state s ON s.id = pt.state_key
WHERE quarter = %s AND y.year = %s 
GROUP BY pt.pincode
ORDER BY SUM(pt.total_transaction_count) DESC LIMIT 10;""",
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


def top_states_transcn(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["state_name", "transaction_amount"]
    try:
        cursor.execute(
            f"""SELECT s.state_name, SUM(tl.total_transaction_count)
FROM phonepe.trans_location tl 
INNER JOIN phonepe.year y ON y.id = tl.year_key 
INNER JOIN phonepe.state s ON s.id = tl.state_key
WHERE quarter = %s AND y.year = %s 
GROUP BY s.state_name
ORDER BY SUM(tl.total_transaction_count) DESC LIMIT 10;""",
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

# top sistricts by transcn
def top_districts_transcn(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["district_name", "transaction_amount"]
    try:
        cursor.execute(
            f"""SELECT  tl.district_name, SUM(tl.total_transaction_count)
FROM phonepe.trans_location tl 
INNER JOIN phonepe.year y ON y.id = tl.year_key 
INNER JOIN phonepe.state s ON s.id = tl.state_key
WHERE quarter = 1 AND y.year = 2018 
GROUP BY tl.district_name
ORDER BY SUM(tl.total_transaction_count) DESC LIMIT 10;""",
            (int(quarter), int(year)),
        )
        tuples_list = cursor.fetchall()
        cursor.close()
        agg_trans = pd.DataFrame(tuples_list, columns=coluumn_names)
        agg_trans["district_name"] = agg_trans["district_name"].str.title()
        return agg_trans
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()

# top district by user
def top_districts_usr(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["district_name", "user_count"]
    try:
        cursor.execute(
            f"""SELECT  ul.district_name, SUM(ul.users_count)
FROM phonepe.users_location ul 
INNER JOIN phonepe.year y ON y.id = ul.year_key 
INNER JOIN phonepe.state s ON s.id = ul.state_key
WHERE quarter = %s AND y.year = %s 
GROUP BY ul.district_name
ORDER BY SUM(ul.users_count) DESC LIMIT 10;""",
            (int(quarter), int(year)),
        )
        tuples_list = cursor.fetchall()
        cursor.close()
        agg_trans = pd.DataFrame(tuples_list, columns=coluumn_names)
        agg_trans["district_name"] = agg_trans["district_name"].str.title()
        return agg_trans
    except (psycopg2.Error, Exception) as e:
        print("An error occurred:", e)
    finally:
        if conn:
            conn.close()

# Top users by state
def top_states_user(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["state_name", "user_count"]
    try:
        cursor.execute(
            f"""SELECT  s.state_name, SUM(ul.users_count)
FROM phonepe.users_location ul 
INNER JOIN phonepe.year y ON y.id = ul.year_key 
INNER JOIN phonepe.state s ON s.id = ul.state_key
WHERE quarter = %s AND y.year = %s 
GROUP BY s.state_name
ORDER BY SUM(ul.users_count) DESC LIMIT 10;""",
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
      
#Pin Code   by user
def top_pincodes_user(quarter, year):
    conn = psql_client()
    cursor = conn.cursor()
    coluumn_names = ["pincode", "transaction_amount"]
    try:
        cursor.execute(
            f"""SELECT  pt.pincode, SUM(pt.total_registered_user)
FROM phonepe.pincode_table pt 
INNER JOIN phonepe.year y ON y.id = pt.year_key 
INNER JOIN phonepe.state s ON s.id = pt.state_key
WHERE quarter = 1 AND y.year = 2018 
GROUP BY pt.pincode
ORDER BY SUM(pt.total_registered_user) DESC LIMIT 10;""",
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
