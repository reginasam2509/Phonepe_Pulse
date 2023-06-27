What is PhonePe Pulse?

The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving back to the digital payments ecosystem. The report is available as a free download on the PhonePe Pulse website and GitHub.

Some Libraries Used In The Project!

Plotly - (To plot and visualize the data)
Pandas - (To Create a DataFrame with the scraped data)
mysql.connector - (To store and retrieve the data)
Streamlit - (To Create Graphical user Interface)
json - (To load the json files)
git.repo.base - (To clone the GitHub repository)

Workflow

Step 1:
Importing the Libraries:

pip install ['library_name']

Already installed some libraries
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy import create_engine
from PIL import Image
from git.repo.base import Repo
import json
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

Step 2:
Data Extract From Git 

Need to clone the github data from the given github url.
from git.repo.base import Repo

Step 3:
Data Preparation

From the data extract from the github,it shows list of JSON files.To retrieve the information from json and structure it in a readable format,by using PYTHON

path1="C:\\Users\\HP\\OneDrive\\Desktop\\pulse\\data\\aggregated\\transaction\\country\\india\\state\\"
agg_trans_list=os.listdir(path1)

columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
            'Transaction_amount': []}

for state in agg_trans_list:
    cur_state= path1 + state + "/"        #Getting All states in given path and given year records of data
    agg_year_list = os.listdir(cur_state)

   
    for year in agg_year_list:
        cur_year = cur_state + year + "/" #Getting Each state with that respective year
        agg_file_list = os.listdir(cur_year)  #List Of json in respective year

        for file in agg_file_list:
            cur_file = cur_year + file      #Getting states,year with respective json
            data = open(cur_file, 'r')
            first=json.load(data)           #Load record of each state with respective years

            for transcation in first['data']['transactionData']:
                name = transcation['name']
                count = transcation['paymentInstruments'][0]['count']
                amount = transcation['paymentInstruments'][0]['amount']
                columns1['Transaction_type'].append(name)
                columns1['Transaction_count'].append(count)
                columns1['Transaction_amount'].append(amount)
                columns1['State'].append(state)
                columns1['Year'].append(year)
                columns1['Quarter'].append(int(file.strip('.json')))

Step 4:
Data Storage:
 
In this project,I created a table manually in the database with respective datatype.By using "from sqlalchemy import create_engine" library push it into database by using command "to_sql".

host='localhost' 
port=3306
user='USERNAME'
password='PASSWORD'
database='DATABASE NAME'
connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
engine=create_engine(connection_string)

Step 5:
Data Visualization

To visualize the data in streamlit, I have used some chart as bar,choropleth,pie chart and scatter 3d plot to look more efficiently and analyse data in a friendly manner.

