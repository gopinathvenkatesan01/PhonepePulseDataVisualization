import streamlit as st
import pandas as pd
import plotly.express as px
import json
import pandas as pd
import os
import json
import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt

from data_extraction import extract_data
from data_service import (
    process_transaction_data,
    process_user_data,
    get_transaction_data,
    get_users_location,
    agg_transcn,
    top_districts_transcn,
    top_districts_usr,
    top_pincodes_user,
    top_states_transcn,
    top_states_user,
    user_chart_data,
    trans_chart_data,
    top_pincodes_transcn,
)
from data_insertion import init
from utilities import amount_crores, amount_rupees, formated, format_amount


def main():
    if "firstrun" not in st.session_state:
        st.session_state.firstrun = True

    st.set_page_config(page_title="Phonepe Dashboard", page_icon="🌏", layout="wide")
    transaction_data_mp, user_data_mp, india_state, state_id_map = extract_data()
    if st.session_state.firstrun:
        # st.balloons()
        init()
        st.session_state.firstrun = False

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
    tab1, tab2 = st.tabs(["Map Metrics", "Top Metrics"])

    # Map Metrics
    with tab1:

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
                width=900,
                height=900,
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

                trans_data = get_transaction_data()
                trans_df = trans_data.loc[
                    (trans_data["quarter"] == int(quarter))
                    & (trans_data["year"] == int(year))
                ]
                agg_trans_count_df = trans_df.agg({"transaction_count": ["sum"]})
                trans_count = agg_trans_count_df.iloc[0, 0]
                agg_trnas_amt_count_df = trans_df.agg(
                    {"transaction_amount": ["sum", "mean"]}
                )
                sum_value = agg_trnas_amt_count_df.iloc[0, 0]  # Accessing sum value
                mean_value = agg_trnas_amt_count_df.iloc[1, 0]  # Accessing mean value

                st.header(":violet[" + metric + "]")
                st.write()
                html_code = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body>
                  <div class="container">
                    <div class="data-wrapper" style="margin-top: 20px;">
                      <h4><strong>All PhonePe transactions (UPI + Cards + Wallets) for {quarter} {year}</strong> </h4>
                      <p style="color: #05c3de; font-size:20px;">{trans_count}</p>
                      <h4><strong>Total payment value</strong></h4>
                      <p style="color: #05c3de; font-size:20px;">{amount_crores(sum_value)}</p>
                      <h4><strong>Avg. transaction value</strong></h4>
                      <p style="color: #05c3de; font-size:20px;">{amount_rupees(sum_value / trans_count)}</p>
                    </div>
                  </div>
                </body>
                </html>
                """
                st.markdown(html_code, unsafe_allow_html=True)
                st.write()
                st.write()
                agg_transaction = agg_transcn(quarter, year)
                if agg_transaction is not None:
                    fig = px.pie(
                        agg_transaction,
                        values="sum",
                        title="Categories",
                        names="transaction_method",
                    )
                    # Updating height and width of the pie chart
                    fig.update_layout(
                        height=400,
                        width=600,
                        legend=dict(
                            orientation="h",  # horizontal orientation
                            yanchor="auto",  # anchor to the auto
                            y=1.25,  # position slightly above the plot
                            xanchor="right",  # anchor to the right
                            x=2,  # position to the right
                        ),
                    )
                    fig.update_traces(
                        hoverinfo="label+percent", textinfo="value", textfont_size=15
                    )
                    st.plotly_chart(fig)

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
                width=900,
                height=900,
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
                users_data = get_users_location()
                users_df = users_data.loc[
                    (users_data["quarter"] == int(quarter))
                    & (users_data["year"] == int(year))
                ]
                agg_users_df = users_df.agg({"users_count": ["sum", "mean"]})
                sum_value = agg_users_df.iloc[0, 0]  # Accessing sum value
                mean_value = agg_users_df.iloc[1, 0]  # Accessing mean value
                html_code = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body>
                  <div class="container">
                    <div class="data-wrapper" style="margin-top: 20px;">
                      <h4><strong>Registered PhonePe users till Q{quarter} {year}</strong> </h4>
                      <p style="color: #05c3de; font-size:20px;">{round(sum_value)}</p>
                      <h4><strong>PhonePe app opens in Q{quarter} {year}</strong></h4>
                      <p style="color: #05c3de; font-size:20px;">{round(mean_value)}</p>
                    </div>
                  </div>
                </body>
                </html>
                """
                st.markdown(html_code, unsafe_allow_html=True)

        slct4, slct5, slct6, slct7, slct8, slct9 = st.columns([2, 1, 1, 1, 2, 2])
        with slct4:
            states_list = [
                "Andaman-&-Nicobar-Islands",
                "Andhra-Pradesh",
                "Arunachal-Pradesh",
                "Assam",
                "Bihar",
                "Chandigarh",
                "Chhattisgarh",
                "Dadra-&-Nagar-Haveli-&-Daman-&-Diu",
                "Delhi",
                "Goa",
                "Gujarat",
                "Haryana",
                "Himachal-Pradesh",
                "Jammu-&-Kashmir",
                "Jharkhand",
                "Karnataka",
                "Kerala",
                "Ladakh",
                "Lakshadweep",
                "Madhya-Pradesh",
                "Maharashtra",
                "Manipur",
                "Meghalaya",
                "Mizoram",
                "Nagaland",
                "Odisha",
                "Puducherry",
                "Punjab",
                "Rajasthan",
                "Sikkim",
                "Tamil-Nadu",
                "Telangana",
                "Tripura",
                "Uttar-Pradesh",
                "Uttarakhand",
                "West-Bengal",
            ]
            state = st.selectbox(
                "State",
                options=states_list,
                index=states_list.index("Tamil-Nadu"),
                key="state",
            )

        with slct5:
            graph_styles = ["Bar", "Line", "Area"]
            graph = st.selectbox(
                "Graph",
                options=graph_styles,
                index=graph_styles.index("Line"),
                key="graph",
            )

        with slct6:
            y1 = ["2018", "2019", "2020", "2021", "2022", "2023"]
            year1 = st.selectbox("Year", y1, key="year1", index=y1.index("2023"))

        with slct7:
            quarter_list = ["1", "2", "3", "4"]
            quarter1 = st.selectbox(
                "Quarter",
                options=quarter_list,
                index=quarter_list.index("1"),
                key="quarter1",
            )

        with slct8:
            user_input_list = ["Users", "Transactions"]
            user_input = st.selectbox(
                "Metric",
                options=user_input_list,
                index=user_input_list.index("Transactions"),
                key="userinput",
            )

        with slct9:
            if user_input == "Transactions":
                trans_list = ["TransactionAmount", "TransactionCount"]
                trans_opt = st.selectbox(
                    "TransactionMetric",
                    options=trans_list,
                    index=trans_list.index("TransactionAmount"),
                    key="transactiontype",
                )
            else:
                user_list = ["NoOfUsers", "NoOfAppOpens"]
                usesr_opt = st.selectbox(
                    "UserMetric",
                    options=user_list,
                    index=user_list.index("NoOfUsers"),
                    key="usertype",
                )

        india_states = gpd.read_file("test.geojson")
        jk = india_states.loc[india_states["ST_NM"] == str(state), "geometry"]

        # Plot the selected area using Geopandas' plot function
        stfig, ax = plt.subplots(figsize=(90 / 10, 70 / 10))
        jk.plot(ax=ax, facecolor="green", edgecolor="blue")
        ax.axis("off")  # Remove the axis ticks and labels

        # user_chart_data
        usr_chart_df = user_chart_data()
        usr_chart_df["state_name"] = usr_chart_df["state_name"].str.title()
        chart_usr = usr_chart_df.loc[
            (usr_chart_df["year"] == int(year1))
            & (usr_chart_df["quarter"] == int(quarter1))
            & (usr_chart_df["state_name"] == str(state))
        ]
        chart_usr["district_name"] = chart_usr["district_name"].str.title()
        usr_count = chart_usr[["district_name", "users_count"]]
        usr_app_opening = chart_usr[["district_name", "app_openig"]]

        # trans_chart_data
        trans_chart_df = trans_chart_data()
        trans_chart_df["state_name"] = trans_chart_df["state_name"].str.title()
        chart_transcn = trans_chart_df.loc[
            (trans_chart_df["year"] == int(year1))
            & (trans_chart_df["quarter"] == int(quarter1))
            & (trans_chart_df["state_name"] == str(state))
        ]
        chart_transcn["district_name"] = chart_transcn["district_name"].str.title()
        transcn_amnt = chart_transcn[["district_name", "total_transaction_amount"]]
        transcn_count = chart_transcn[["district_name", "total_transaction_count"]]

        state_, chart = st.columns([3, 6])

        # Users
        if user_input == "Users":
            with state_:
                st.write(f"### {str(state)}")
                st.pyplot(stfig)

            with chart:
                if usesr_opt == "NoOfUsers":

                    if graph == "Line":
                        st.write(str(state))
                        fig_chart = px.line(
                            usr_count,
                            x="district_name",
                            y="users_count",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                    elif graph == "Bar":
                        st.write(str(state))
                        fig_chart = px.bar(
                            usr_count,
                            x="district_name",
                            y="users_count",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                    elif graph == "Area":
                        st.write(str(state))
                        fig_chart = px.area(
                            usr_count,
                            x="district_name",
                            y="users_count",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                # AppOpenings
                else:

                    if graph == "Line":
                        st.write(str(state))
                        fig_chart = px.line(
                            usr_app_opening,
                            x="district_name",
                            y="app_openig",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                    elif graph == "Bar":
                        st.write(str(state))
                        fig_chart = px.bar(
                            usr_app_opening,
                            x="district_name",
                            y="app_openig",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                    elif graph == "Area":
                        st.write(str(state))
                        fig_chart = px.area(
                            usr_app_opening,
                            x="district_name",
                            y="app_openig",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )
        # transactions
        else:
            with state_:
                st.write(f"### {str(state)}")
                st.pyplot(stfig)

            with chart:
                if trans_opt == "TransactionAmount":

                    if graph == "Line":
                        st.write(str(state))
                        fig_chart = px.line(
                            transcn_amnt,
                            x="district_name",
                            y="total_transaction_amount",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                    elif graph == "Bar":
                        st.write(str(state))
                        fig_chart = px.bar(
                            transcn_amnt,
                            x="district_name",
                            y="total_transaction_amount",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                    elif graph == "Area":
                        st.write(str(state))
                        fig_chart = px.area(
                            transcn_amnt,
                            x="district_name",
                            y="total_transaction_amount",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                # TransactionCount
                else:

                    if graph == "Line":
                        st.write(str(state))
                        fig_chart = px.line(
                            transcn_count,
                            x="district_name",
                            y="total_transaction_count",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                    elif graph == "Bar":
                        st.write(str(state))
                        fig_chart = px.bar(
                            transcn_count,
                            x="district_name",
                            y="total_transaction_count",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )

                    elif graph == "Area":
                        st.write(str(state))
                        fig_chart = px.area(
                            transcn_count,
                            x="district_name",
                            y="total_transaction_count",
                            width=850,
                            height=525,
                        )
                        st.plotly_chart(
                            fig_chart,
                            config=dict(
                                {"displayModeBar": False}, **{"displaylogo": False}
                            ),
                            use_container_width=False,
                            layout=dict({"width": "100%"}, **{"height": "100%"}),
                        )
    with tab2:
        states, districts, pincodes = st.tabs(["States", "Districts", "Postal Codes"])
        # Transaction Metrics

        if metric == "Transactions":
            with states:
                top_states_df = top_states_transcn(quarter, year)
                custom_colors = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                    "#e377c2",
                    "#7f7f7f",
                    "#bcbd22",
                    "#17becf",
                ]
                # Format amounts
                top_states_df["formatted_amount"] = top_states_df[
                    "transaction_amount"
                ].apply(format_amount)

                # Create pie chart
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=top_states_df["state_name"],
                            values=top_states_df["transaction_amount"],
                            text=top_states_df["formatted_amount"],
                            insidetextorientation="radial",
                            hole=0.3,
                            marker=dict(colors=custom_colors),
                        )
                    ]
                )
                fig.update_traces(
                    textposition="inside", textinfo="text", hoverinfo="label+text"
                )
                fig.update_layout(title="Transaction Amount Distribution by State")
                st.plotly_chart(fig)

            with districts:
                top_districts_df = top_districts_transcn(quarter, year)
                custom_colors = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                    "#e377c2",
                    "#7f7f7f",
                    "#bcbd22",
                    "#17becf",
                ]
                # Format amounts
                top_districts_df["formatted_amount"] = top_districts_df[
                    "transaction_amount"
                ].apply(format_amount)

                # Create pie chart
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=top_districts_df["district_name"],
                            values=top_districts_df["transaction_amount"],
                            text=top_districts_df["formatted_amount"],
                            insidetextorientation="radial",
                            hole=0.3,
                            marker=dict(colors=custom_colors),
                        )
                    ]
                )
                fig.update_traces(
                    textposition="inside", textinfo="text", hoverinfo="label+text"
                )
                fig.update_layout(title="Transaction Amount Distribution by District")
                st.plotly_chart(fig)

            with pincodes:
                top_pincodes_df = top_pincodes_transcn(quarter, year)
                custom_colors = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                    "#e377c2",
                    "#7f7f7f",
                    "#bcbd22",
                    "#17becf",
                ]

                # Format amounts
                top_pincodes_df["formatted_amount"] = top_pincodes_df[
                    "transaction_amount"
                ].apply(format_amount)

                # Create pie chart
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=top_pincodes_df["pincode"],
                            values=top_pincodes_df["transaction_amount"],
                            text=top_pincodes_df["formatted_amount"],
                            insidetextorientation="radial",
                            hole=0.3,
                            marker=dict(colors=custom_colors),
                        )
                    ]
                )
                fig.update_traces(
                    textposition="inside", textinfo="text", hoverinfo="label+text"
                )
                fig.update_layout(title="Transaction Amount Distribution by Pincode")
                st.plotly_chart(fig)

        elif metric == "User":

            with states:
                top_states_df = top_states_user(quarter, year)
                custom_colors = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                    "#e377c2",
                    "#7f7f7f",
                    "#bcbd22",
                    "#17becf",
                ]

                # Create pie chart
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=top_states_df["state_name"],
                            values=top_states_df["user_count"],
                            text=top_states_df["user_count"],
                            insidetextorientation="radial",
                            hole=0.3,
                            marker=dict(colors=custom_colors),
                        )
                    ]
                )
                fig.update_traces(
                    textposition="inside", textinfo="text", hoverinfo="label+text"
                )
                fig.update_layout(title="User Count Distribution by State")
                st.plotly_chart(fig)

            with districts:
                top_districts_df = top_districts_usr(quarter, year)
                custom_colors = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                    "#e377c2",
                    "#7f7f7f",
                    "#bcbd22",
                    "#17becf",
                ]
                # Create pie chart
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=top_districts_df["district_name"],
                            values=top_districts_df["user_count"],
                            text=top_districts_df["user_count"],
                            insidetextorientation="radial",
                            hole=0.3,
                            marker=dict(colors=custom_colors),
                        )
                    ]
                )
                fig.update_traces(
                    textposition="inside", textinfo="text", hoverinfo="label+text"
                )
                fig.update_layout(title="User  Count Distribution by District")
                st.plotly_chart(fig)

            with pincodes:
                top_pincodes_df = top_pincodes_user(quarter, year)
                custom_colors = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                    "#e377c2",
                    "#7f7f7f",
                    "#bcbd22",
                    "#17becf",
                ]

                # Create pie chart
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=top_pincodes_df["pincode"],
                            values=top_pincodes_df["transaction_amount"],
                            text=top_pincodes_df["transaction_amount"],
                            insidetextorientation="radial",
                            hole=0.3,
                            marker=dict(colors=custom_colors),
                        )
                    ]
                )
                fig.update_traces(
                    textposition="inside", textinfo="text", hoverinfo="label+text"
                )
                fig.update_layout(title="user Count Distribution by Pincode")
                st.plotly_chart(fig)


if __name__ == "__main__":
    main()
