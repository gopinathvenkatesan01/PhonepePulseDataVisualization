import pandas as pd
import json
import plotly.express as px
import os
import pprint as pprint
import streamlit as st


def extract_data():
    transaction_data_mp = map_transaction()
    india_state, state_id_map, state_df = geo_json()
    user_data_mp = map_user()
    return transaction_data_mp, user_data_mp, india_state, state_id_map


def format_number(number):
    return "{:.0f}".format(number)


@st.cache_data
def geo_json():
    india_state = json.load(open("states_india.geojson", "r"))
    state_id_map = {}
    state_df_new_columuns = {"State": "state_name", "Id": "id"}
    for feature in india_state["features"]:
        feature["id"] = feature["properties"]["state_code"]

        if (
            feature["properties"]["st_nm"] == "Dadara & Nagar Havelli"
            or feature["properties"]["st_nm"] == "Daman & Diu"
        ):
            feature["properties"]["st_nm"] = "Dadra & Nagar Haveli & Daman & Diu"
            feature["id"] = 25
            # state_id_map['Dadra & Nagar Haveli & Daman & Diu'] = 25

        elif feature["properties"]["st_nm"] == "Andaman & Nicobar Island":
            feature["properties"]["st_nm"] = "Andaman & Nicobar Islands"
            feature["id"] = 35
            # state_id_map['Andaman & Nicobar Islands'] = 35

        elif feature["properties"]["st_nm"] == "Arunanchal Pradesh":
            feature["properties"]["st_nm"] = "Arunachal Pradesh"
            feature["id"] = 12
            # state_id_map['Arunachal Pradesh'] = 12

        elif feature["properties"]["st_nm"] == "NCT of Delhi":
            feature["properties"]["st_nm"] = "Delhi"
            feature["id"] = 7
            # state_id_map['Delhi'] = 7

        state_id_map[feature["properties"]["st_nm"]] = feature["id"]
        state_id_map["Ladakh"] = 26

        state_df = pd.DataFrame(list(state_id_map.items()), columns=["State", "Id"])
        state_df.rename(columns=state_df_new_columuns, inplace=True)
        state_df = state_df.sort_values(by="id")

    return india_state, state_id_map, state_df


@st.cache_data
def map_transaction():
    map_transaction_path = "D:/Learning/Projects/PhonepePulseDataVisualization/src/phonepeData/data/map/transaction/hover/country/india/"

    map_transaction = {
        "Year": [],
        "Quarter": [],
        "State": [],
        "Transaction_count": [],
        "Transaction_amount": [],
    }

    year_list = os.listdir(map_transaction_path)

    for year in year_list:
        if year == "state":
            continue
        path = map_transaction_path + year + "/"
        quarter_list = os.listdir(path)
        for quarter in quarter_list:
            qtr_path = path + quarter
            D = open(qtr_path, "r")
            data = json.load(D)
            for value in data["data"]["hoverDataList"]:
                Name = value["name"]
                count = value["metric"][0]["count"]
                amount = format_number(value["metric"][0]["amount"])
                map_transaction["Transaction_amount"].append(amount)
                map_transaction["Transaction_count"].append(count)
                map_transaction["State"].append(Name)
                map_transaction["Year"].append(year)
                map_transaction["Quarter"].append(int(quarter.strip(".json")))

    map_transcation_df = pd.DataFrame(map_transaction)
    map_transcation_df["State"] = map_transcation_df["State"].str.title()

    return map_transcation_df


@st.cache_data
def map_user():
    map_user_path = "D:/Learning/Projects/PhonepePulseDataVisualization/src/phonepeData/data/map/user/hover/country/india/"

    mp_user = {"Year": [], "Quarter": [], "State": [], "Count": []}

    year_list = os.listdir(map_user_path)
    for year in year_list:
        if year == "state":
            continue
        path = map_user_path + year + "/"
        quarter_list = os.listdir(path)
        for quarter in quarter_list:
            qtr_path = path + quarter
            D = open(qtr_path, "r")
            data = json.load(D)
            # try:
            # Extract state names and data
            states = list(data["data"]["hoverData"].keys())
            for value in states:
                state = value
                count = data["data"]["hoverData"][state]["registeredUsers"]
                mp_user["State"].append(state)
                mp_user["Count"].append(count)
                mp_user["Year"].append(year)
                mp_user["Quarter"].append(int(quarter.strip(".json")))
            # except Exception as e:
            # print(e)
            # pass

    map_user_df = pd.DataFrame(mp_user)
    return map_user_df


@st.cache_data
def aggregated_transcn_st():

    aggreated_transcn_state_path = "D:/Learning/Projects/PhonepePulseDataVisualization/src/phonepeData/data/aggregated/transaction/country/india/state/"

    state_transcation = {
        "State": [],
        "Year": [],
        "Quarter": [],
        "Transaction_type": [],
        "Transaction_count": [],
        "Transaction_amount": [],
    }
    state_list = os.listdir(aggreated_transcn_state_path)
    for state in state_list:
        year_path = aggreated_transcn_state_path + state + "/"
        year_list = os.listdir(year_path)
        for year in year_list:
            path = year_path + year + "/"
            quarter_list = os.listdir(path)
            for quarter in quarter_list:
                qtr_path = path + quarter
                D = open(qtr_path, "r")
                data = json.load(D)
                for value in data["data"]["transactionData"]:
                    Name = value["name"]
                    count = value["paymentInstruments"][0]["count"]
                    amount = format_number(value["paymentInstruments"][0]["amount"])
                    state_transcation["Transaction_amount"].append(amount)
                    state_transcation["Transaction_count"].append(count)
                    state_transcation["Transaction_type"].append(Name)
                    state_transcation["Year"].append(year)
                    state_transcation["State"].append(state)
                    state_transcation["Quarter"].append(int(quarter.strip(".json")))

    st_transcation_df = pd.DataFrame(state_transcation)
    st_transcation_df["State"] = st_transcation_df["State"].str.title()
    india_state, state_id_map, state_df = geo_json()

    return st_transcation_df, state_df


@st.cache_data
def arrgregated_usr_st():
    aggreated_user_state_path = "D:/Learning/Projects/PhonepePulseDataVisualization/src/phonepeData/data/aggregated/user/country/india/state/"

    state_user = {
        "State": [],
        "Year": [],
        "Quarter": [],
        "Brands": [],
        "Count": [],
        "Percentage": [],
        "Users_count": [],
        "App_opening": [],
    }
    state_list = os.listdir(aggreated_user_state_path)
    for state in state_list:
        year_path = aggreated_user_state_path + state + "/"
        year_list = os.listdir(year_path)
        for year in year_list:
            path = year_path + year + "/"
            quarter_list = os.listdir(path)
            for quarter in quarter_list:
                qtr_path = path + quarter
                D = open(qtr_path, "r")
                data = json.load(D)
                user_count = data["data"]["aggregated"]["registeredUsers"]
                app_open = data["data"]["aggregated"]["appOpens"]
                try:
                    for value in data["data"]["usersByDevice"]:
                        Brand = value["brand"]
                        count = value["count"]
                        percent = value["percentage"]
                        state_user["Brands"].append(Brand)
                        state_user["Count"].append(count)
                        state_user["Percentage"].append(percent)
                        state_user["Year"].append(year)
                        state_user["State"].append(state)
                        state_user["Quarter"].append(int(quarter.strip(".json")))
                        state_user["Users_count"].append(user_count)
                        state_user["App_opening"].append(app_open)
                except:
                    pass

    st_user_df = pd.DataFrame(state_user)
    st_user_df["State"] = st_user_df["State"].str.title()
    return st_user_df


@st.cache_data
def map_user_st():
    map_st_user_path = "D:/Learning/Projects/PhonepePulseDataVisualization/src/phonepeData/data/map/user/hover/country/india/state/"

    mp_st_user = {
        "Year": [],
        "Quarter": [],
        "State": [],
        "District": [],
        "Count": [],
        "App_Opening": [],
    }

    mp_state_list = os.listdir(map_st_user_path)
    for state in mp_state_list:
        year_path = map_st_user_path + state + "/"
        year_list = os.listdir(year_path)
        for year in year_list:
            path = year_path + year + "/"
            quarter_list = os.listdir(path)
            for quarter in quarter_list:
                qtr_path = path + quarter
                D = open(qtr_path, "r")
                data = json.load(D)
                # try:
                # Extract state names and data
                districts = list(data["data"]["hoverData"].keys())
                for value in districts:
                    district = value
                    count = data["data"]["hoverData"][district]["registeredUsers"]
                    app_opening = data["data"]["hoverData"][district]["appOpens"]
                    mp_st_user["State"].append(state)
                    mp_st_user["Count"].append(count)
                    mp_st_user["App_Opening"].append(app_opening)
                    mp_st_user["Year"].append(year)
                    mp_st_user["Quarter"].append(int(quarter.strip(".json")))
                    mp_st_user["District"].append(district)
                # except Exception as e:
                # print(e)
                # pass
    map_st_user_df = pd.DataFrame(mp_st_user)
    map_st_user_df["State"] = map_st_user_df["State"].str.title()
    return map_st_user_df


@st.cache_data
def map_transcation_st():
    map_state_transaction_path = "D:/Learning/Projects/PhonepePulseDataVisualization/src/phonepeData/data/map/transaction/hover/country/india/state/"

    map_st_transaction = {
        "Year": [],
        "Quarter": [],
        "State": [],
        "District": [],
        "Transaction_count": [],
        "Transaction_amount": [],
    }

    state_list = os.listdir(map_state_transaction_path)

    for state in state_list:
        state_path = map_state_transaction_path + state + "/"
        year_list = os.listdir(state_path)
        for year in year_list:
            path = state_path + year + "/"
            quarter_list = os.listdir(path)
            for quarter in quarter_list:
                qtr_path = path + quarter
                D = open(qtr_path, "r")
                data = json.load(D)
                try:
                    for value in data["data"]["hoverDataList"]:
                        Name = value["name"]
                        count = value["metric"][0]["count"]
                        amount = format_number(value["metric"][0]["amount"])
                        map_st_transaction["Transaction_amount"].append(amount)
                        map_st_transaction["Transaction_count"].append(count)
                        map_st_transaction["District"].append(Name)
                        map_st_transaction["State"].append(state)
                        map_st_transaction["Year"].append(year)
                        map_st_transaction["Quarter"].append(
                            int(quarter.strip(".json"))
                        )
                except:
                    pass

    map_st_transcation_df = pd.DataFrame(map_st_transaction)
    map_st_transcation_df["State"] = map_st_transcation_df["State"].str.title()

    return map_st_transcation_df


@st.cache_data
def top_usr_st():
    top_state_user_path = "D:/Learning/Projects/PhonepePulseDataVisualization/src/phonepeData/data/top/user/country/india/state/"

    top_usr_by_st_pincode = {
        "State": [],
        "Year": [],
        "Quarter": [],
        "Pincode": [],
        "Count": [],
    }
    top_usr_by_st_district = {
        "State": [],
        "Year": [],
        "Quarter": [],
        "District": [],
        "Count": [],
    }

    state_list = os.listdir(top_state_user_path)

    for state in state_list:
        state_path = top_state_user_path + state + "/"
        year_list = os.listdir(state_path)
        for year in year_list:
            path = state_path + year + "/"
            quarter_list = os.listdir(path)
            for quarter in quarter_list:
                qtr_path = path + quarter
                D = open(qtr_path, "r")
                data = json.load(D)

                for value in data["data"]["pincodes"]:
                    Name = value["name"]
                    count = value["registeredUsers"]
                    top_usr_by_st_pincode["Count"].append(count)
                    top_usr_by_st_pincode["Pincode"].append(Name)
                    top_usr_by_st_pincode["State"].append(state)
                    top_usr_by_st_pincode["Year"].append(year)
                    top_usr_by_st_pincode["Quarter"].append(int(quarter.strip(".json")))

                for value in data["data"]["districts"]:
                    Name = value["name"]
                    count = value["registeredUsers"]
                    top_usr_by_st_district["Count"].append(count)
                    top_usr_by_st_district["District"].append(Name)
                    top_usr_by_st_district["State"].append(state)
                    top_usr_by_st_district["Year"].append(year)
                    top_usr_by_st_district["Quarter"].append(
                        int(quarter.strip(".json"))
                    )

    top_st_usr_pincode_df = pd.DataFrame(top_usr_by_st_pincode)
    top_st_usr_pincode_df["State"] = top_st_usr_pincode_df["State"].str.title()
    top_st_usr_district_df = pd.DataFrame(top_usr_by_st_district)
    top_st_usr_district_df["State"] = top_st_usr_district_df["State"].str.title()

    return top_st_usr_pincode_df, top_st_usr_district_df


@st.cache_data
def top_transcn_st():
    top_state_transaction_path = "D:/Learning/Projects/PhonepePulseDataVisualization/src/phonepeData/data/top/transaction/country/india/state/"

    top_st_transaction_pincode = {
        "State": [],
        "Year": [],
        "Quarter": [],
        "Pincode": [],
        "Transaction_count": [],
        "Transaction_amount": [],
    }
    top_st_transaction_district = {
        "State": [],
        "Year": [],
        "Quarter": [],
        "District": [],
        "Transaction_count": [],
        "Transaction_amount": [],
    }

    state_list = os.listdir(top_state_transaction_path)

    for state in state_list:
        state_path = top_state_transaction_path + state + "/"
        year_list = os.listdir(state_path)
        for year in year_list:
            path = state_path + year + "/"
            quarter_list = os.listdir(path)
            for quarter in quarter_list:
                qtr_path = path + quarter
                D = open(qtr_path, "r")
                data = json.load(D)

                for value in data["data"]["pincodes"]:
                    Name = value["entityName"]
                    count = value["metric"]["count"]
                    amount = format_number(value["metric"]["amount"])
                    top_st_transaction_pincode["Transaction_amount"].append(amount)
                    top_st_transaction_pincode["Transaction_count"].append(count)
                    top_st_transaction_pincode["Pincode"].append(Name)
                    top_st_transaction_pincode["State"].append(state)
                    top_st_transaction_pincode["Year"].append(year)
                    top_st_transaction_pincode["Quarter"].append(
                        int(quarter.strip(".json"))
                    )

                for value in data["data"]["districts"]:
                    Name = value["entityName"]
                    count = value["metric"]["count"]
                    amount = format_number(value["metric"]["amount"])
                    top_st_transaction_district["Transaction_amount"].append(amount)
                    top_st_transaction_district["Transaction_count"].append(count)
                    top_st_transaction_district["District"].append(Name)
                    top_st_transaction_district["State"].append(state)
                    top_st_transaction_district["Year"].append(year)
                    top_st_transaction_district["Quarter"].append(
                        int(quarter.strip(".json"))
                    )

    top_st_transcation_pincode_df = pd.DataFrame(top_st_transaction_pincode)
    top_st_transcation_pincode_df["State"] = top_st_transcation_pincode_df[
        "State"
    ].str.title()
    top_st_transcation_pincode_df.fillna(0, inplace=True)
    top_st_transcation_district_df = pd.DataFrame(top_st_transaction_district)
    top_st_transcation_district_df["State"] = top_st_transcation_district_df[
        "State"
    ].str.title()
    top_st_transcation_district_df.fillna(0, inplace=True)

    return top_st_transcation_pincode_df, top_st_transcation_district_df
