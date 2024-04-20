import streamlit as st
import pandas as pd
import plotly.express as px
import json
import pandas as pd
import os
import json

from data_extraction import extract_data
from data_service import (
    process_transaction_data,
    process_user_data,
    get_trans_method,
    get_users_location,
)
from data_insertion import init
from utilities import formated

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Transactions Information</title>
</head>
<body>
  <div class="container">
    <h1 style="text-align: left; color: #720FE7 ;">Transactions</h1>
    <div class="data-wrapper" style="margin-top: 20px;">
      <h4><strong>All PhonePe transactions (UPI + Cards + Wallets)</strong> </h4>
      <p style = "color: #05c3de; font-size:20px;">15,10,96,26,850</p>
      <h4><strong>Total payment value</strong></h4>
      <p style = "color: #05c3de; font-size:20px;"> ₹22,91,864Cr</p>
      <h4> <strong>Avg. transaction value</strong></h4>
      <p style = "color: #05c3de; font-size:20px;" > ¥1,517</p>
    </div>
  </div>
</body>
</html>
"""




def main():
    st.set_page_config(page_title="Phonepe Dashboard", page_icon="🌏", layout="wide")
    transaction_data_mp, user_data_mp, india_state, state_id_map = extract_data()
    init()
    st.subheader("⏩ Phonepe pulse **Data Analysis** | _By Gopi_ ")

    slct3, slct1, slct2 = st.columns([2, 1, 1])
    with slct3:
        metric = st.selectbox(
            "Component", options=["User", "Transactions"], index=0, key="metric"
        )

    with slct1:
        year = st.selectbox(
            "Year", options=transaction_data_mp.Year.unique(), index=0, key="year"
        )

    with slct2:
        quarter = st.selectbox(
            "Quarter",
            options=transaction_data_mp.Quarter.unique(),
            index=0,
            key="quarter",
        )

    if metric == "Transactions":
        map, map_details = st.columns([2, 1])
        transaction_data_mp = process_transaction_data(
            transaction_data_mp, state_id_map
        )
        map_transcation_df_2018 = transaction_data_mp.query(
            "Year == '{}' and Quarter == {}".format(year, quarter)
        )
        fig = px.choropleth_mapbox(
            map_transcation_df_2018,
            title=metric,
            locations="id",
            geojson=india_state,
            color="Transaction_amount",
            hover_name="State",
            hover_data={
                "All Transactions": True,
                "Total Payment Values": True,
                "id": False,
                "Avg.Transaction Value": True,
                "Transaction_amount": False,
            },
            mapbox_style="carto-positron",
            center={"lat": 24, "lon": 78},
            color_continuous_scale=px.colors.diverging.PuOr,
            color_continuous_midpoint=0,
            zoom=3.6,
            width=1000,
            height=1000,
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            coloraxis_colorbar=dict(title=" ", showticklabels=True),
            title={"font": {"size": 24}},
            hoverlabel_font={"size": 18},
        )
        with map:
            st.plotly_chart(
                fig,
                config=dict({"displayModeBar": False}, **{"displaylogo": False}),
                use_container_width=False,
            )

        with map_details:
            st.write()
            
            st.markdown(html_code, unsafe_allow_html=True)


    else:
        map, map_details = st.columns([2, 1])
        user_data_mp = process_user_data(user_data_mp, state_id_map)
        map_user_df_2018 = user_data_mp.query(
            "Year == '{}' and Quarter == {}".format(year, quarter)
        )
        fig = px.choropleth_mapbox(
            map_user_df_2018,
            locations="id",
            geojson=india_state,
            title=metric,
            color="Count",
            hover_name="State",
            mapbox_style="carto-positron",
            center={"lat": 24, "lon": 78},
            color_continuous_scale=px.colors.diverging.PuOr,
            color_continuous_midpoint=0,
            zoom=3.6,
            width=1000,
            height=1000,
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            coloraxis_colorbar=dict(title=" ", showticklabels=True),
            title={"font": {"size": 24}},
            hoverlabel_font={"size": 18},
        )
        with map:
            st.plotly_chart(
                fig,
                config=dict({"displayModeBar": False}, **{"displaylogo": False}),
                use_container_width=False,
            )

        with map_details:
            st.write()
            st.header(":violet[" + metric + "]")
            st.subheader(
                ":blue[Registered PhonePe users till Quarter"
                + str(quarter)
                + " "
                + str(year)
                + "]"
            )


if __name__ == "__main__":
    main()
