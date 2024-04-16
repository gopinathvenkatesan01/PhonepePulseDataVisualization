import streamlit as st
import pandas as pd
import plotly.express as px
import json
import pandas as pd
import os
import json

from data_extraction import extract_data
from data_service import process_transaction_data, process_user_data
from data_insertion import init
from utilities import formated



def main():
    st.set_page_config(page_title='Phonepe Dashboard',
                       page_icon="🌏",
                       layout="wide")
    transaction_data_mp,user_data_mp,india_state,state_id_map =extract_data()
    init()
    st.subheader("⏩ Phonepe pulse **Data Analysis** | _By Gopi_ ")
    
    slct3,slct1,slct2 = st.columns([2, 1, 1])
    with slct3:
        metric = st.selectbox("Component",
                              options=["User","Transactions"],
                              index=0,
                              key="metric")
    
    with slct1:
        year = st.selectbox("Year",
                            options=transaction_data_mp.Year.unique(),
                            index=0,
                            key="year")
    
    with slct2:
        quarter = st.selectbox("Quarter",
                               options=transaction_data_mp.Quarter.unique(),
                               index=0,
                               key="quarter")  
        
    if metric == "Transactions":
        transaction_data_mp = process_transaction_data(transaction_data_mp,state_id_map)
        
        map_transcation_df_2018 = transaction_data_mp.query("Year == '{}' and Quarter == {}".format(year, quarter))
        
        fig = px.choropleth_mapbox(
                 map_transcation_df_2018,
                 title="Transactions",
                 locations="id",
                 geojson=india_state,
                 color="Transaction_amount",
                 hover_name="State",
                 hover_data={'All Transactions':True,'Total Payment Values':True,'id':False,'Avg.Transaction Value':True,'Transaction_amount':False},
                 mapbox_style="carto-positron",
                 center={'lat':24,'lon':78},
                 color_continuous_scale=px.colors.diverging.PuOr,
                 color_continuous_midpoint=0,
                 zoom=3.6,
                 width=1000, 
                 height=1000  
                 )
    
        
       
    else: 
        user_data_mp = process_user_data(user_data_mp,state_id_map)
        
        map_user_df_2018 = user_data_mp.query("Year == '{}' and Quarter == {}".format(year, quarter))
        
        fig = px.choropleth_mapbox(map_user_df_2018,locations="id",
                    geojson=india_state,
                    title="Users",
                    color="Count",
                    hover_name="State", 
                    mapbox_style="carto-positron",
                    center={'lat':24,'lon':78},
                    color_continuous_scale=px.colors.diverging.PuOr,
                    color_continuous_midpoint=0,
                    zoom=3.6,
                    width=1000, 
                    height=1000 )
        
    
    fig.update_geos(fitbounds="locations",visible =False)        
    fig.update_layout(coloraxis_colorbar=dict(title=' ', showticklabels=True),title={
    'font': {'size': 24}
    },hoverlabel_font={'size': 18})
    st.plotly_chart(fig, config=dict({'displayModeBar': False}, **{'displaylogo': False}), use_container_width=False)    
    


if __name__ == '__main__':
    main()