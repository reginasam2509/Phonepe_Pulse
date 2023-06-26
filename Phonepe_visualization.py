import pandas as pd
import sys
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy import create_engine
from PIL import Image
from git.repo.base import Repo
import json
import urllib
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

icon = Image.open("D:\phonepe\phonepe.PNG")

st.set_page_config(
    page_title="Phonepe Pulse Data Visualization | BY Sam",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """# This dashboard app is created by *Sam*!
                     Data has been cloned from Phonepe Pulse Github Repo"""
    }
)

st.title("😃 🔍 [**Phonepe Pulse Visualization**]")

# Create database connection
host = 'localhost'
port = 3306
user = 'root'
password = 'regina'
database = 'phonepe'
connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(connection_string)

# Creating option menu as tabs
tabs = ["Home", "TopLevelCharts","BottomLevelCharts", "Overall Data", "Live Visual","About"]
selected_tab = st.sidebar.radio("Menu", tabs)

#State Mapping
state_mapping={
    'andaman-&-nicobar-islands': 'Andaman and Nicobar',
    'andhra-pradesh':'Andhra Pradesh',
    'arunachal-pradesh':'Arunachal Pradesh',
    'assam':'Assam',
    'bihar':'Bihar',
    'chandigarh':'Chandigarh',
    'chhattisgarh':'Chhattisgarh',
    'dadra-&-nagar-haveli-&-daman-&-diu':'Dadra and Nagar Haveli',
    'delhi':'Delhi',
    'goa':'Goa',
    'gujarat':'Gujarat',
    'haryana':'Haryana',
    'himachal-pradesh':'Himachal Pradesh',
    'jammu-&-kashmir':'Jammu & Kashmir',
    'jharkhand':'Jharkhand',
    'karnataka':'Karnataka',
    'kerala':'Kerala',
    'ladakh':'Ladakh',
    'lakshadweep':'Lakshadweep',
    'madhya-pradesh':'Madhya Pradesh',
    'maharashtra':'Maharashtra',
    'manipur':'Manipur',
    'meghalaya':'Meghalaya',
    'mizoram':'Mizoram',
    'nagaland':'Nagaland',
    'odisha':'Odisha',
    'puducherry':'Puducherry',
    'punjab':'Punjab',
    'rajasthan':'Rajasthan',
    'sikkim':'Sikkim',
    'tamil-nadu':'Tamil Nadu',
    'telangana':'Telangana',
    'tripura':'Tripura',
    'uttar-pradesh':'Uttar Pradesh',
    'uttarakhand':'Uttarakhand',
    'west-bengal':'West Bengal'
}



# MENU 1 - HOME
if selected_tab == "Home":
    st.image("phonepe_1.PNG")
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL,Streamlit, and Plotly.")
    with col2:
        st.image("home.png")

# MENU 2 - TOP CHARTS
if selected_tab == "TopLevelCharts":
    st.markdown("## :violet[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    colum1, colum2 = st.columns([1,2], gap="large")
   

    with colum1:
        Year = st.selectbox("Year", [2018, 2019, 2020, 2021, 2022])
        Quarter = st.selectbox("Quarter", [1, 2, 3, 4])

    with colum2:
        st.info(
            """
            #### From this menu we can get insights like:
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transactions and Total amount spent on Phonepe.
            - Top 10 State, District, Pincode based on Total Phonepe users and their app opening frequency.
            - Top 10 mobile brands and their percentage based on the number of people using Phonepe.
            """,
            icon="🔍"
        )
    
    # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2=st.columns([2,2],gap="small")
        col3,col4=st.columns([2,2],gap="small")
        col5,col6=st.columns([2,2],gap="small")

        with col1:
            st.markdown("### :violet[State]")
            query = "SELECT State, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM agg_trans WHERE year = %s AND quarter = %s GROUP BY state ORDER BY Total DESC LIMIT 10"
            params = (Year, Quarter)
            df_state = pd.read_sql(query, engine, params=params)
            df_state['State_mapped'] = df_state['State'].apply(lambda x: state_mapping.get(x, x))
            fig = px.pie(df_state, values='Total', names='State_mapped', title='Top 10',
                color_discrete_sequence=px.colors.sequential.Agsunset,
                hover_data=['Total_Transactions_Count'],
                labels={'Transactions_Count': 'Transactions_Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[CountryMap]")
            query = "SELECT State, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM agg_trans WHERE year = %s AND quarter = %s GROUP BY state ORDER BY Total DESC LIMIT 10"
            fig1= px.choropleth(
                df_state,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State_mapped',
                color='Total_Transactions_Count',
                color_continuous_scale="sunset",
                range_color=(0, df_state['Total_Transactions_Count'].max()),
                labels={'Total': 'Total'})
            fig1.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig1)
        
        with col3:
            st.markdown("### :violet[District]")
            # query="select district ,MAX(State) as State , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = %s and quarter = %s group by district order by Total desc limit 10"
            query="select district ,MAX(State) as State , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = %s and quarter = %s group by district,State order by Total desc limit 10"
            params=(Year,Quarter)
            df_district = pd.read_sql(query,engine,params=params)
            df_district['District_State'] = df_district['district'] + ' (' + df_district['State'] + ')'
            df_district['State_mapped'] = df_district['State'].apply(lambda x: state_mapping.get(x, x))
            fig2 = px.pie(df_district ,values='Total',
                             names='District_State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Viridis,
                             hover_data=['Total_Count'],
                             labels={'Total_Count':'Transactions_Count'})
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2,use_container_width=True)
        with col4:
            st.markdown("### :violet[CountryMap]")
            fig3 = px.choropleth(
            df_district,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State_mapped',
            color='Total_Count',
            color_continuous_scale="viridis",
            range_color=(0, df_district['Total_Count'].max()),
            labels={'Total': 'Total'})
            fig3.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig3)

        with col5:
            st.markdown("### :violet[Pincodes]")
            query="select Pincode_entityname,MAX(State) as State,sum(Pincode_Count) as Total_Pincode_Count,sum(Pincode_amount) as Total_Pincode_Amount from top_trans2 where year = %s and quarter = %s group by Pincode_entityname order by Total_Pincode_Amount desc limit 10"
            params=(Year,Quarter)
            df_pincode=pd.read_sql(query,engine,params=params)
            df_pincode['Pincode_State']=df_pincode['Pincode_entityname']+'('+df_pincode['State']+')'
            df_pincode['State_mapped'] = df_pincode['State'].apply(lambda x: state_mapping.get(x, x))

            fig4=px.pie(
                df_pincode,
                values='Total_Pincode_Amount',
                names='Pincode_State',
                title='Top 10',
                color_discrete_sequence=px.colors.sequential.Cividis,
                hover_data=['Total_Pincode_Count'],
                labels={'Transactions_Count':'Pincode_count'}
            )
            fig4.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig4,use_container_width=True)

        with col6:
            st.markdown("### :violet[CountryMap]")
            fig5=px.choropleth(
            df_pincode,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            locations='State_mapped',
            featureidkey='properties.ST_NM',
            color='Total_Pincode_Count',
            color_continuous_scale="cividis",
            range_color=(0,df_pincode['Total_Pincode_Count'].max()),
            labels={'Total_Pincode_Count':'Total_Count_10_Pincode'}
        )
            fig5.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig5)

    #Top charts User

    if Type == "Users":
        col1,col2=st.columns([2,2],gap="small")
        col3,col4=st.columns([2,2],gap="small")
        col5,col6=st.columns([2,2],gap="small")

        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4 😞")
            else:
                query="select Brands,sum(Count) as Total_Count,max(State) as State,avg(Percentage)*100 as Avg_Percentage  from agg_user where year = %s and quarter = %s group by Brands order by Total_Count desc limit 10 "
                params=(Year,Quarter)
                df_agg=pd.read_sql(query,engine,params=params)
                df_agg['Brand_State']=df_agg['Brands']+'('+df_agg['State']+')'
                fig = px.bar(df_agg,
                             title='Top 10',
                             x="Total_Count",
                             y="Brand_State",
                            #  orientation='v',
                             color='Total_Count',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True) 

        with col2:
            st.markdown("### :violet[CountryMap]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4 😞")
            else:
                df_agg['State_mapped'] = df_agg['State'].apply(lambda x: state_mapping.get(x, x))
                fig1=px.choropleth(
                df_agg,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                locations='State_mapped',
                featureidkey='properties.ST_NM',
                color='Total_Count',
                color_continuous_scale="cividis",
                range_color=(0,df_agg['Total_Count'].max()),
                labels={'Total_Count':'Total_Count'}
        )
                fig1.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig1)

        
        with col3:
            st.markdown("### :violet[District]")
            query="select District,max(State) as State,sum(Registered_users)as Total_User,sum(App_opens)as Total_App_opens from map_user where year = %s and quarter = %s group by District order by Total_User desc limit 10"
            params=(Year,Quarter)
            df_map=pd.read_sql(query,engine,params=params)
            df_map['District_State']=df_map['District']+'('+df_map['State']+')'
            fig1= px.bar(df_map,
                         title='Top 10',
                         x="Total_User",
                         y="District_State",
                         orientation='h',
                         color='Total_User',
                         color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig1,use_container_width=True)

        with col4:
            st.markdown("### :violet[District]")
            query = "SELECT District, MAX(State) AS State, SUM(Registered_users) AS Total_User, SUM(App_opens) AS Total_App_opens FROM map_user WHERE year = %s AND quarter = %s GROUP BY District ORDER BY Total_User DESC LIMIT 10"
            params = (Year, Quarter)
            df_map = pd.read_sql(query, engine, params=params)
            df_map['District_State'] = df_map['District'] + ' (' + df_map['State'] + ')'

            fig2= px.scatter_3d(df_map,
                    x='Total_User',
                    y='Total_App_opens',
                    z='District',
                    color='Total_User',
                    size='Total_User',
                    title='Top 10',
                    color_continuous_scale=px.colors.sequential.Viridis)

            st.plotly_chart(fig2, use_container_width=True)

        with col5:
            st.markdown("###:violet[Pincode]")
            query="select Pincode_name,max(State)as State,sum(Pincode_registeredusers) as Total_User from top_user2 where year = %s and quarter = %s group by Pincode_name order by Total_User desc limit 10"
            params=(Year,Quarter)
            df_top=pd.read_sql(query,engine,params=params)
            df_top['Pincode_State']=df_top['Pincode_name']+'('+df_top['State']+')'
            fig3=px.bar(
                df_top,
                title='Top 10',
                x='Total_User',
                y='Pincode_State',
                orientation='h',
                color='Total_User',
                color_continuous_scale=px.colors.sequential.Cividis
            )
            st.plotly_chart(fig3,use_container_width=True) 

        with col6:
            st.markdown("### :violet[Pincode]")
            query = "SELECT Pincode_name, MAX(State) AS State, SUM(Pincode_registeredusers) AS Total_User FROM top_user2 WHERE year = %s AND quarter = %s GROUP BY Pincode_name ORDER BY Total_User DESC LIMIT 10"
            params = (Year, Quarter)
            df_top = pd.read_sql(query, engine, params=params)
            df_top['Pincode_State'] = df_top['Pincode_name'] + ' (' + df_top['State'] + ')'

            fig4= px.scatter_3d(df_top,
                    x='Pincode_name',
                    y='State',
                    z='Total_User',
                    color='Total_User',
                    size='Total_User',
                    title='Top 10',
                    color_continuous_scale=px.colors.sequential.Cividis)

            st.plotly_chart(fig4, use_container_width=True)

if selected_tab=="BottomLevelCharts":
    st.markdown("## :violet[Bottom Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    colum1, colum2 = st.columns([1,2], gap="large")
   

    with colum1:
        Year = st.selectbox("Year", [2018, 2019, 2020, 2021, 2022])
        Quarter = st.selectbox("Quarter", [1, 2, 3, 4])

    with colum2:
        st.info(
            """
            #### From this menu we can get insights like:
            - Overall ranking on a particular Year and Quarter.
            - Bottom 10 State, District, Pincode based on Total number of transactions and Total amount spent on Phonepe.
            - Bottom 10 State, District, Pincode based on Total Phonepe users and their app opening frequency.
            - Bottom 10 mobile brands and their percentage based on the number of people using Phonepe.
            """,
            icon="🔍"
        )

    if Type == "Transactions":
        col1,col2=st.columns([2,2],gap="small")
        col3,col4=st.columns([2,2],gap="small")
        col5,col6=st.columns([2,2],gap="small")

        with col1:
            st.markdown("### :violet[State]")
            query = "SELECT State, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM agg_trans WHERE year = %s AND quarter = %s GROUP BY state ORDER BY Total  LIMIT 10"
            params = (Year, Quarter)
            df_state1 = pd.read_sql(query, engine, params=params)
            df_state1['State_mapped'] = df_state1['State'].apply(lambda x: state_mapping.get(x, x))
            fig = px.pie(df_state1, values='Total', names='State_mapped', title='Top 10',
                color_discrete_sequence=px.colors.sequential.Agsunset,
                hover_data=['Total_Transactions_Count'],
                labels={'Transactions_Count': 'Transactions_Count'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :violet[CountryMap]")
            query = "SELECT State, SUM(Transaction_count) AS Total_Transactions_Count, SUM(Transaction_amount) AS Total FROM agg_trans WHERE year = %s AND quarter = %s GROUP BY state ORDER BY Total  LIMIT 10"
            fig1= px.choropleth(
                df_state1,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State_mapped',
                color='Total_Transactions_Count',
                color_continuous_scale="sunset",
                range_color=(0, df_state1['Total_Transactions_Count'].max()),
                labels={'Total': 'Total'})
            fig1.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig1)
        
        with col3:
            st.markdown("### :violet[District]")
            # query="select district ,MAX(State) as State , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = %s and quarter = %s group by district order by Total desc limit 10"
            query="select district ,MAX(State) as State , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = %s and quarter = %s group by district,State order by Total  limit 10"
            params=(Year,Quarter)
            df_district1 = pd.read_sql(query,engine,params=params)
            df_district1['District_State'] = df_district1['district'] + ' (' + df_district1['State'] + ')'
            df_district1['State_mapped'] = df_district1['State'].apply(lambda x: state_mapping.get(x, x))
            fig2 = px.pie(df_district1 ,values='Total',
                             names='District_State',
                             title='Bottom 10',
                             color_discrete_sequence=px.colors.sequential.Viridis,
                             hover_data=['Total_Count'],
                             labels={'Total_Count':'Transactions_Count'})
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2,use_container_width=True)
        with col4:
            st.markdown("### :violet[CountryMap]")
            fig3 = px.choropleth(
            df_district1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State_mapped',
            color='Total_Count',
            color_continuous_scale="viridis",
            range_color=(0, df_district1['Total_Count'].max()),
            labels={'Total': 'Total'})
            fig3.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig3)

        with col5:
            st.markdown("### :violet[Pincodes]")
            query="select Pincode_entityname,MAX(State) as State,sum(Pincode_Count) as Total_Pincode_Count,sum(Pincode_amount) as Total_Pincode_Amount from top_trans2 where year = %s and quarter = %s group by Pincode_entityname order by Total_Pincode_Amount  limit 10"
            params=(Year,Quarter)
            df_pincode1=pd.read_sql(query,engine,params=params)
            df_pincode1['Pincode_State']=df_pincode1['Pincode_entityname']+'('+df_pincode1['State']+')'
            df_pincode1['State_mapped'] = df_pincode1['State'].apply(lambda x: state_mapping.get(x, x))

            fig4=px.pie(
                df_pincode1,
                values='Total_Pincode_Amount',
                names='Pincode_State',
                title='Bottom 10',
                color_discrete_sequence=px.colors.sequential.Cividis,
                hover_data=['Total_Pincode_Count'],
                labels={'Transactions_Count':'Pincode_count'}
            )
            fig4.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig4,use_container_width=True)

        with col6:
            st.markdown("### :violet[Scatter]")
            fig = px.scatter_3d(df_pincode1, x='Pincode_entityname', y='State', z='Total_Pincode_Amount', color='Total_Pincode_Count')
            fig.update_layout(scene=dict(xaxis_title='Pincode Entity', yaxis_title='State', zaxis_title='Total Pincode Amount'))
            st.plotly_chart(fig, use_container_width=True)\
            
    if Type == "Users":
        col1,col2=st.columns([2,2],gap="small")
        col3,col4=st.columns([2,2],gap="small")
        col5,col6=st.columns([2,2],gap="small")

        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4 😞")
            else:
                query="select Brands,sum(Count) as Total_Count,max(State) as State,avg(Percentage)*100 as Avg_Percentage  from agg_user where year = %s and quarter = %s group by Brands order by Total_Count  limit 10 "
                params=(Year,Quarter)
                df_agg=pd.read_sql(query,engine,params=params)
            # df_pincode['Pincode_State']=df_pincode['Pincode_entityname']+'('+df_pincode['State']+')'
                df_agg['Brand_State']=df_agg['Brands']+'('+df_agg['State']+')'
                fig = px.bar(df_agg,
                             title='Bottom 10',
                             x="Total_Count",
                             y="Brand_State",
                            #  orientation='v',
                             color='Total_Count',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True) 

        with col2:
            st.markdown("### :violet[CountryMap]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4 😞")
            else:
                df_agg['State_mapped'] = df_agg['State'].apply(lambda x: state_mapping.get(x, x))
                fig1=px.choropleth(
                df_agg,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                locations='State_mapped',
                featureidkey='properties.ST_NM',
                color='Total_Count',
                color_continuous_scale="cividis",
                range_color=(0,df_agg['Total_Count'].max()),
                labels={'Total_Count':'Total_Count'}
        )
                fig1.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig1)

        
        with col3:
            st.markdown("### :violet[District]")
            query="select District,max(State) as State,sum(Registered_users)as Total_User,sum(App_opens)as Total_App_opens from map_user where year = %s and quarter = %s group by District order by Total_User  limit 10"
            params=(Year,Quarter)
            df_map=pd.read_sql(query,engine,params=params)
            df_map['District_State']=df_map['District']+'('+df_map['State']+')'
            fig1= px.bar(df_map,
                         title='Bottom 10',
                         x="Total_User",
                         y="District_State",
                         orientation='h',
                         color='Total_User',
                         color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig1,use_container_width=True)

        with col4:
            st.markdown("### :violet[District]")
            query = "SELECT District, MAX(State) AS State, SUM(Registered_users) AS Total_User, SUM(App_opens) AS Total_App_opens FROM map_user WHERE year = %s AND quarter = %s GROUP BY District ORDER BY Total_User  LIMIT 10"
            params = (Year, Quarter)
            df_map = pd.read_sql(query, engine, params=params)
            df_map['District_State'] = df_map['District'] + ' (' + df_map['State'] + ')'

            fig2= px.scatter_3d(df_map,
                    x='Total_User',
                    y='Total_App_opens',
                    z='District',
                    color='Total_User',
                    size='Total_User',
                    title='Bottom 10',
                    color_continuous_scale=px.colors.sequential.Viridis)

            st.plotly_chart(fig2, use_container_width=True)

        with col5:
            st.markdown("### :violet[Pincode]")
            query="select Pincode_name,max(State)as State,sum(Pincode_registeredusers) as Total_User from top_user2 where year = %s and quarter = %s group by Pincode_name order by Total_User  limit 10"
            params=(Year,Quarter)
            df_top=pd.read_sql(query,engine,params=params)
            df_top['Pincode_State']=df_top['Pincode_name']+'('+df_top['State']+')'
            fig3=px.bar(
                df_top,
                title='Bottom 10',
                x='Total_User',
                y='Pincode_State',
                orientation='h',
                color='Total_User',
                color_continuous_scale=px.colors.sequential.Cividis
            )
            st.plotly_chart(fig3,use_container_width=True) 

        with col6:
            st.markdown("### :violet[Pincode]")
            query = "SELECT Pincode_name, MAX(State) AS State, SUM(Pincode_registeredusers) AS Total_User FROM top_user2 WHERE year = %s AND quarter = %s GROUP BY Pincode_name ORDER BY Total_User  LIMIT 10"
            params = (Year, Quarter)
            df_top = pd.read_sql(query, engine, params=params)
            df_top['Pincode_State'] = df_top['Pincode_name'] + ' (' + df_top['State'] + ')'

            fig4= px.scatter_3d(df_top,
                    x='Pincode_name',
                    y='State',
                    z='Total_User',
                    color='Total_User',
                    size='Total_User',
                    title='Bottom 10',
                    color_continuous_scale=px.colors.sequential.Cividis)

            st.plotly_chart(fig4, use_container_width=True)



if selected_tab == "Overall Data":
    st.markdown("## :violet[Overall Data]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    colum1, colum2 = st.columns([1,2], gap="large")
   

    with colum1:
        Year = st.selectbox("Year", [2018, 2019, 2020, 2021, 2022])
        Quarter = st.selectbox("Quarter", [1, 2, 3, 4])
    
    with colum2:
        st.info(
            """
            #### From this menu we can get insights like:
            - Overall ranking on a particular Year and Quarter.
            - Overall info regarding the total_transaction count and type of transactions

            """,
            icon="🔍"
        )
    if Type=='Transactions':
        # with col1:
            st.markdown("## :violet[Overall State Data]")
            st.markdown('## :violet[Aggregate Transaction]')
            query="select State,sum(Transaction_count)as Total_Transaction_Count,sum(Transaction_amount)as Total_Transaction_Amount ,max(Transaction_type)as Transaction_type from agg_trans where year = %s and quarter = %s group by State,Transaction_type order by State"
            params=(Year,Quarter)
            df_agg_overall=pd.read_sql(query,engine,params=params)
            df_agg_overall['State_mapped'] = df_agg_overall['State'].apply(lambda x: state_mapping.get(x, x))

            
            fig = px.choropleth(df_agg_overall,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State_mapped',
                      color='Total_Transaction_Count',
                      color_continuous_scale='sunset',
                      range_color=(0, df_agg_overall['Total_Transaction_Count'].max()),
                      labels={'Total_Transaction_Count':'Total_Count'}
                      )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

            # st.markdown('## : violet[Overall State Data]')
            st.markdown("## :violet[Transaction Count]")
            query1="select State,sum(Count) as Total_Transactions,sum(Amount) as Total_Amount from map_trans where year=%s and quarter=%s group by State order by State"
            params=(Year,Quarter)
            df_map1=pd.read_sql(query1,engine,params=params)
            df_map1['State_mapped'] = df_map1['State'].apply(lambda x: state_mapping.get(x, x))
            fig1=px.choropleth(
                df_map1,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State_mapped',
                color='Total_Transactions',
                hover_name='State_mapped',
                color_continuous_scale='viridis',
                range_color=(0,df_map1['Total_Transactions'].max()),
                labels={'Total_Transactions':'Transaction_count'}
            )           
            fig1.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig1,use_container_width=True)


            st.markdown("## :violet[Top Payment Type]")
            query3="select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= %s and quarter = %s  group by Transaction_type order by Transaction_type"
            params=(Year,Quarter)
            df_agg1=pd.read_sql(query3,engine,params=params)
            fig3= px.bar(df_agg1,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig3,use_container_width=False)

            st.markdown("# ")
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("## :violet[Select any State to explore more]")
            selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
            state_mapped = state_mapping.get(selected_state, selected_state)
            query2 = "SELECT State, District, Year, Quarter, SUM(Count) AS Total_Transactions, SUM(Amount) AS Total_Amount FROM map_trans WHERE Year = %s AND Quarter = %s AND State = %s GROUP BY State, District, Year, Quarter ORDER BY State, District"
            params = (Year, Quarter, selected_state)
            df_map2 = pd.read_sql(query2, engine, params=params)

            fig2 = px.bar(df_map2,
              title=state_mapped,
              x="District",
              y="Total_Transactions",
              orientation='v',
              color='Total_Amount',
              color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig2, use_container_width=True)


    if Type=='Users':  
        st.markdown("## :violet[Overall State Data]")
        st.markdown("## :violet[User App Opening]")
        query="select State,sum(Registered_users)as Total_User,sum(App_opens)as Total_Appopens from map_user where year = %s and quarter = %s group by State order by State"
        params=(Year,Quarter)
        df_map3=pd.read_sql(query,engine,params=params)
        df_map3['State_mapped'] = df_map3['State'].apply(lambda x: state_mapping.get(x, x))

        fig=px.choropleth(
            df_map3,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State_mapped',
            color='Total_Appopens',
            color_continuous_scale='Viridis',
            hover_name='State_mapped',
            range_color=(0,df_map3['Total_Appopens'].max()),
            labels={'Total_Appopens':'Total_Appopens'}

        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)


        fig2=px.choropleth(
            df_map3,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State_mapped',
            color='Total_User',
            color_continuous_scale='sunset',
            hover_name='State_mapped',
            range_color=(0,df_map3['Total_User'].max()),
            labels={'Total_User':'Total_User'}

        )
        fig2.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig2,use_container_width=True)


        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        state_mapped = state_mapping.get(selected_state, selected_state)
        query1="select State,District,Year,Quarter,sum(Registered_users)as Total_user,sum(App_opens)as Total_Appopens from map_user where year=%s and quarter=%s and State=%s group by State,District,Year,Quarter order by State,District"
        params=(Year,Quarter,selected_state)
        df_map4=pd.read_sql(query1,engine,params=params)

        fig1= px.bar(df_map4,
                     title=state_mapped,
                     x="District",
                     y="Total_user",
                     orientation='v',
                     color='Total_user',
                     color_continuous_scale=px.colors.sequential.Cividis)
        st.plotly_chart(fig1,use_container_width=True)


if selected_tab=='Live Visual':
    Year = st.selectbox("Year", [2018, 2019, 2020, 2021, 2022])
    Quarter = st.selectbox("Quarter", [1, 2, 3, 4])

    st.markdown("## :violet[Overall State Data]")
    st.markdown("## :violet[User App Opening]")
    query="select State,sum(Registered_users)as Total_User,sum(App_opens)as Total_Appopens from map_user where year = %s and quarter = %s group by State order by State"
    params=(Year,Quarter)
    df_map3=pd.read_sql(query,engine,params=params)
    df_map3['State_mapped'] = df_map3['State'].apply(lambda x: state_mapping.get(x, x))

    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

# # Create a Plotly Choropleth map
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson_url,
        locations=df_map3['State_mapped'],
        z=df_map3['Total_User'],
        featureidkey='properties.ST_NM',
        colorscale='sunset',
        zmin=0,
        zmax=df_map3['Total_User'].max(),
        marker_opacity=0.7,
        marker_line_width=0,
        ))

# Set the layout of the map
    fig.update_layout(
       mapbox_style="carto-positron",
       mapbox_zoom=4,
       mapbox_center={"lat": 20.5937, "lon": 78.9629},
       margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

# Render the map in Streamlit using the st.plotly_chart function
    st.plotly_chart(fig, use_container_width=True)

if selected_tab=="About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
        st.markdown("### :violet[About PhonePe:] ")
        st.write(" PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        st.write("PhonePe is a digital payment platform and financial technology company based in India. It was founded in December 2015 and has become one of the leading mobile payment apps in the country. Here are some key points about PhonePe:Mobile Payment App: PhonePe offers a mobile app that enables users to make various types of digital payments conveniently using their smartphones. Users can link their bank accounts to the app and make payments directly from their bank accounts.UPI Unified Payments Interface: PhonePe is built on the UPI platform, which is a real-time payment system in India that allows users to transfer money between bank accounts instantly using their mobile phones. PhonePe supports UPI-based transactions, making it easy for users to send and receive money.")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("Pulseimg.JPG")
        st.image("Pulseimg1.JPG")




   




