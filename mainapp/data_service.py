from utilities import amount_crores, formated
import streamlit  as st
import pandas as pd

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