import pandas as pd
import json
import os
from sqlalchemy import create_engine

#Dataframe Agg
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

df_agg_trans=pd.DataFrame(columns1)
# print(df_agg_trans.shape)

#DATAFRAME AGG USERS

path2="C:\\Users\\HP\\OneDrive\\Desktop\\pulse\\data\\aggregated\\user\\country\\india\\state\\"
agg_user_list=os.listdir(path2)

columns2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [],
            'Percentage': []}

for state in agg_user_list:
    cur_state = path2 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            second= json.load(data)

            try:
                for user in second["data"]["usersByDevice"]:
                    brand_name = user["brand"]
                    counts = user["count"]
                    percents = user["percentage"]
                    columns2["Brands"].append(brand_name)
                    columns2["Count"].append(counts)
                    columns2["Percentage"].append(percents)
                    columns2["State"].append(state)
                    columns2["Year"].append(year)
                    columns2["Quarter"].append(int(file.strip('.json')))
            except:
                pass

df_agg_user = pd.DataFrame(columns2)
# print(df_agg_user.shape)

#DATAFRAME MAP TRANS

path3="C:\\Users\\HP\\OneDrive\\Desktop\\pulse\\data\\map\\transaction\\hover\\country\\india\\state\\"
map_trans_list=os.listdir(path3)

columns3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [],
            'Amount': []}

for state in map_trans_list:
    cur_state = path3 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            third= json.load(data)
            
            for map_transaction in third['data']['hoverDataList']:
                name=map_transaction['name']
                count=map_transaction['metric'][0]['count']
                amount=map_transaction['metric'][0]['amount']
                columns3['District'].append(name)
                columns3['Count'].append(count)
                columns3['Amount'].append(amount)
                columns3["State"].append(state)
                columns3["Year"].append(year)
                columns3["Quarter"].append(int(file.strip('.json')))

df_map_trans=pd.DataFrame(columns3)
# print(df_map_trans.shape)

#DATAFRAME MAP USER

path4="C:\\Users\\HP\\OneDrive\\Desktop\\pulse\\data\\map\\user\\hover\\country\\india\\state\\"
map_user_list=os.listdir(path4)

columns4={'State':[],'Year':[],'Quarter':[],'District':[],'Registered_users':[],'App_opens':[]}
for state in map_user_list:
    cur_state = path4 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            fourth = json.load(data)

            try:
                hover_data = fourth["data"]["hoverData"]
                
                for district, district_data in hover_data.items():
                    registered_users = district_data["registeredUsers"]
                    app_opens = district_data["appOpens"]
                    
                    columns4['District'].append(district)
                    columns4['Registered_users'].append(registered_users)
                    columns4['App_opens'].append(app_opens)
                    columns4['Year'].append(year)
                    columns4['State'].append(state)
                    columns4["Quarter"].append(int(file.strip('.json')))
                    
            except KeyError:
                print("Error: Missing 'hoverData' key or its subkeys")
                print()

df_map_user=pd.DataFrame(columns4)
# print(df_map_user.shape)

#DATAFRAME TOP TRANS1

path5="C:\\Users\\HP\\OneDrive\\Desktop\\pulse\\data\\top\\transaction\\country\\india\state\\"
top_trans_list=os.listdir(path5)

columns5={'State':[],'Year':[],'Quarter':[],'District_entityname':[],'District_count':[],'District_amount':[]}
for state in top_trans_list:
    cur_state = path5 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            fifth = json.load(data)
#             print(fifth)
            
            for top_transaction in fifth['data']['districts']:
                name=top_transaction['entityName']
                count=top_transaction['metric']['count']
                amount=top_transaction['metric']['amount']
                columns5['District_entityname'].append(name)
                columns5['District_count'].append(count)
                columns5['District_amount'].append(amount)
                columns5['Year'].append(year)
                columns5['State'].append(state)
                columns5["Quarter"].append(int(file.strip('.json')))


df_top_trans1=pd.DataFrame(columns5)
# print(df_top_trans1.shape)

#DATAFRAME TOP TRANS2

columns6={'Pincode_entityname':[],'Pincode_count':[],'Pincode_amount':[],'State':[],'Year':[],'Quarter':[]}
for state in top_trans_list:
    cur_state = path5 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            fifth= json.load(data)
            
            for top_transaction in fifth['data']['pincodes']:
                name=top_transaction['entityName']
                count=top_transaction['metric']['count']
                amount=top_transaction['metric']['amount']
                columns6['Pincode_entityname'].append(name)
                columns6['Pincode_count'].append(count)
                columns6['Pincode_amount'].append(amount)
                columns6['Year'].append(year)
                columns6['State'].append(state)
                columns6['Quarter'].append(int(file.strip('.json')))

df_top_trans2=pd.DataFrame(columns6)
# print(df_top_trans2.shape)


#DATAFRAME TOP USER1

path6="C:\\Users\\HP\\OneDrive\\Desktop\\pulse\\data\\top\\user\\country\\india\\state\\"
top_user_list=os.listdir(path6)

columns7={'State':[],'Year':[],'Quarter':[],'District_name':[],'District_registeredUsers':[]}
for state in top_user_list:
    cur_state = path6 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            sixth= json.load(data)
            
            for top_user in sixth['data']['districts']:
                name=top_user['name']
                registered_user=top_user['registeredUsers']
                columns7['District_name'].append(name)
                columns7['District_registeredUsers'].append(registered_user)
                columns7['State'].append(state)
                columns7['Year'].append(year)
                columns7['Quarter'].append(int(file.strip('.json')))

df_top_user1=pd.DataFrame(columns7)
# print(df_top_user1.shape)

#DATAFRAME TOP USER2

columns8={'State':[],'Year':[],'Quarter':[],'Pincode_name':[],'Pincode_registeredusers':[]}
for state in top_user_list:
    cur_state = path6 + state + "/"
    agg_year_list = os.listdir(cur_state)
    
    for year in agg_year_list:
        cur_year = cur_state + year + "/"
        agg_file_list = os.listdir(cur_year)

        for file in agg_file_list:
            cur_file = cur_year + file
            data = open(cur_file, 'r')
            sixth= json.load(data)
            
            
            for top_user1 in sixth['data']['pincodes']:
                name=top_user1['name']
                registered_user=top_user1['registeredUsers']
                columns8['Pincode_name'].append(name)
                columns8['Pincode_registeredusers'].append(registered_user)
                columns8['Year'].append(year)
                columns8['State'].append(state)
                columns8['Quarter'].append(int(file.strip('.json')))

df_top_user2=pd.DataFrame(columns8)


#SQL CONNECT
host='localhost' 
port=3306
user='root'
password='regina'
database='phonepe'
connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
engine=create_engine(connection_string)

print("AGG TRANS DESCRIBE")
print(df_agg_trans.shape)
df_agg_trans.to_sql('agg_trans',con=engine,if_exists='append',index=False)
print("Inseted successfully table 1")

print("AGG USER DESCRIBE")
print(df_agg_user.shape)
df_agg_user.to_sql('agg_user',con=engine,if_exists='append',index=False)
print("Inserted successfully table 2")

print("MAP TRANS")
print(df_map_trans.shape)
df_map_trans.to_sql('map_trans',con=engine,if_exists='append',index=False)
print("Inserted successfully table 3")

print("MAP USER DESCRIBE")
print(df_map_user.shape)
df_map_user.to_sql('map_user',con=engine,if_exists='append',index=False)
print("Inserted successfully table 4")

print("TOP TRANS1")
print(df_top_trans1.shape)
df_top_trans1.to_sql('top_trans1',con=engine,if_exists='append',index=False)
print("Inserted successfully table 5")

print("TOP TRANS2")
print(df_top_trans2.shape)
df_top_trans2.to_sql('top_trans2',con=engine,if_exists='append',index=False)
print("Inserted successfully table 6")


print("TOP USER1")
print(df_top_user1.shape)
df_top_user1.to_sql('top_user1',con=engine,if_exists='append',index=False)
print("Inserted successfully table 7")


print("TOP USER2")
print(df_top_user2.shape)
df_top_user2.to_sql('top_user2',con=engine,if_exists='append',index=False)
print("Inserted successfully table 8")

engine.dispose()