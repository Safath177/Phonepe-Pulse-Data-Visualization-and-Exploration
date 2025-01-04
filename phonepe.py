import streamlit as st
import psycopg2
import pandas as pd
import plotly_express as px
import requests
import json
import uuid
from PIL import Image
# Dataframe Creation

db = psycopg2.connect(host = 'localhost',
                      user = 'postgres',
                      port = '5432',
                      database = 'PhonePe',
                      password = '1177')

cursor = db.cursor()


#aggregated_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
db.commit()
table_agg_ins = cursor.fetchall()
aggregated_insurance = pd.DataFrame(table_agg_ins,columns=("States","Years","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#aggregated_transaction_df

cursor.execute("SELECT * FROM aggregated_transaction")
db.commit()
table_agg_trans = cursor.fetchall()
aggregated_transaction = pd.DataFrame(table_agg_trans,columns=("States","Years","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#aggregated_user_df

cursor.execute("SELECT * FROM aggregated_user")
db.commit()
table_agg_user = cursor.fetchall()
aggregated_user = pd.DataFrame(table_agg_user,columns=("States","Years","Quarter","brands","Transaction_Count","percentage"))

#map_insurance_df

cursor.execute("SELECT * FROM map_insurance")
db.commit()
table_map_ins = cursor.fetchall()
map_insurance = pd.DataFrame(table_map_ins,columns=("States","Years","Quarter","District","Transaction_Count","Transaction_Amount"))

#map_transaction_df

cursor.execute("SELECT * FROM map_transaction")
db.commit()
table_map_trans = cursor.fetchall()
map_transaction = pd.DataFrame(table_map_trans,columns=("States","Years","Quarter","District","Transaction_Count","Transaction_Amount"))

#map_user_df

cursor.execute("SELECT * FROM map_user")
db.commit()
table_map_user = cursor.fetchall()
map_user = pd.DataFrame(table_map_user,columns=("States","Years","Quarter","District","Registered_Users","App_Opens"))

#top_insurance_df

cursor.execute("SELECT * FROM top_insurance")
db.commit()
table_top_ins = cursor.fetchall()
top_insurance = pd.DataFrame(table_top_ins,columns=("States","Years","Quarter","Pincodes","Transaction_Count","Transaction_Amount"))

#top_transaction_df

cursor.execute("SELECT * FROM top_transaction")
db.commit()
table_top_trans = cursor.fetchall()
top_transaction = pd.DataFrame(table_top_trans,columns=("States","Years","Quarter","Pincodes","Transaction_Count","Transaction_Amount"))

#top_user_df

cursor.execute("SELECT * FROM top_user")
db.commit()
table_top_user = cursor.fetchall()
top_user = pd.DataFrame(table_top_user,columns=("States","Years","Quarter","Pincodes","Registered_Users"))





def Transaction_amount_count_year(df,year):
    unique_id = uuid.uuid4()
    tacy = df[df['Years'] == year]
    tacy.reset_index(drop=True,inplace=True)

    tacy_gr = tacy.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tacy_gr.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:

        amount_char = px.bar(tacy_gr,x="States",y="Transaction_Amount",title=f"Transaction Amount for {year}",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(amount_char,key=f"amount_char{unique_id}")
    with col2:
        count_char = px.bar(tacy_gr,x="States",y="Transaction_Count",title=f"Transaction Count for {year}",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(count_char,key=f"count_char{unique_id}")
    
    map_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    res = requests.get(map_url)
    res_data = json.loads(res.content)
    state_name = []
    for feature in res_data['features']:
        state_name.append(feature['properties']['ST_NM'])
    state_name.sort()

    col1,col2 = st.columns(2)

    with col1:

        Ind_amount = px.choropleth(tacy_gr,geojson=res_data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_Amount",color_continuous_scale="Rainbow",
                            range_color=(tacy_gr["Transaction_Amount"].min(),tacy_gr["Transaction_Amount"].max()),
                            hover_name="States",title=f"Transaction Amount for {year}",fitbounds="locations",height=650,width=600)
        Ind_amount.update_geos(visible = False)
        st.plotly_chart(Ind_amount,key=f"Ind_amount{unique_id}")
    with col2:
        Ind_count = px.choropleth(tacy_gr,geojson=res_data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_Count",color_continuous_scale="Rainbow",
                            range_color=(tacy_gr["Transaction_Count"].min(),tacy_gr["Transaction_Count"].max()),
                            hover_name="States",title=f"Transaction Count for {year}",fitbounds="locations",height=650,width=600)
        Ind_count.update_geos(visible = False)
        st.plotly_chart(Ind_count,key=f"Ind_count{unique_id}")  

    return tacy

def Transaction_amount_count_quarter(df,quarter):
    unique_code = uuid.uuid4()
    tacq = df[df['Quarter'] == quarter]
    tacq.reset_index(drop=True,inplace=True)

    tacq_gr = tacq.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    tacq_gr.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:

        amount_char_quarter = px.bar(tacq_gr,x="States",y="Transaction_Amount",title=f"Transaction Amount for year {tacq['Years'].min()} {quarter} Quarter",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(amount_char_quarter,key=f"amount_char_quarter{unique_code}")
    with col2:
        count_char_quarter = px.bar(tacq_gr,x="States",y="Transaction_Count",title=f"Transaction Count for year {tacq['Years'].min()} {quarter} Quarter",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(count_char_quarter,key=f"count_char_quarter{unique_code}")

    map_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    res = requests.get(map_url)
    res_data = json.loads(res.content)
    state_name = []
    for feature in res_data['features']:
        state_name.append(feature['properties']['ST_NM'])
    state_name.sort()
    col1,col2 = st.columns(2)

    with col1:

        Ind_amount_quarter = px.choropleth(tacq_gr,geojson=res_data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_Amount",color_continuous_scale="Rainbow",
                            range_color=(tacq_gr["Transaction_Amount"].min(),tacq_gr["Transaction_Amount"].max()),
                            hover_name="States",title=f"Transaction Amount for year {tacq['Years'].min()} {quarter} Quarter",fitbounds="locations",height=650,width=600)
        Ind_amount_quarter.update_geos(visible = False)
        st.plotly_chart(Ind_amount_quarter,key=f"Ind_amount_quarter{unique_code}")
    with col2:

        Ind_count_quarter = px.choropleth(tacq_gr,geojson=res_data,locations="States",featureidkey="properties.ST_NM",
                            color="Transaction_Count",color_continuous_scale="Rainbow",
                            range_color=(tacq_gr["Transaction_Count"].min(),tacq_gr["Transaction_Count"].max()),
                            hover_name="States",title=f"Transaction Count for year {tacq['Years'].min()} {quarter} Quarter",fitbounds="locations",height=650,width=600)
        Ind_count_quarter.update_geos(visible = False)
        st.plotly_chart(Ind_count_quarter,key=f"Ind_count_quarter{unique_code}")

    return tacq

def aggregated_Transaction_type(df,state):

    tty = df[df['States'] == state]
    tty.reset_index(drop=True, inplace=True)

    tty_gr = tty.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum()
    tty_gr.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        trans_char_pie_amount = px.pie(tty_gr,"Transaction_Type","Transaction_Amount",width=600,title=f"Transaction Amount for {state}"
                                ,hole=0.5)
        st.plotly_chart(trans_char_pie_amount)
    with col2:
        trans_char_pie_count = px.pie(tty_gr,"Transaction_Type","Transaction_Count",width=600,title=f"Transaction Count for {state}"
                                ,hole=0.5)
        st.plotly_chart(trans_char_pie_count)

# aggregated user year
def aggregated_user_year(df,year):
    auy = df[df['Years']== year]
    auy.reset_index(drop=True,inplace=True)

    auy_gr = pd.DataFrame(auy.groupby("brands")["Transaction_Count"].sum())
    auy_gr.reset_index(inplace=True)

    auy_bar = px.bar(auy_gr,x="brands",y="Transaction_Count",title=f"Transaction Count of Brands for {year}",width=800,
                    color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(auy_bar)

    return auy

# aggregated user quarter
def aggregated_user_year_quarter(df,quarter):
    auyq = df[df['Quarter']== quarter]
    auyq.reset_index(drop=True,inplace=True)

    auyq_gr = pd.DataFrame(auyq.groupby("brands")["Transaction_Count"].sum())
    auyq_gr.reset_index(inplace=True)

    auyq_bar = px.bar(auyq_gr,x="brands",y="Transaction_Count",title=f"Transaction Count of Brands for {quarter} Quarter",width=800,
                        color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(auyq_bar)

    return auyq

# aggregated user year quarter states    
def aggregated_user_year_quarter_states(df,state):
    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop=True,inplace=True)

    auyqs_char = px.pie(auyqs,"brands","Transaction_Count",width=600,title=f"Transaction Count of {state}",hover_data="percentage",hole=0.5)
    st.plotly_chart(auyqs_char)

# map insurance district
def map_ins_dist(df,state):

    tty = df[df['States'] == state]
    tty.reset_index(drop=True, inplace=True)

    tty_gr = tty.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    tty_gr.reset_index(inplace=True)

    trans_char_bar_amount = px.bar(tty_gr,x="Transaction_Amount",y="District",orientation="h",title=f"District wise Transaction Amount Split for {state}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                                   height=600)
    st.plotly_chart(trans_char_bar_amount)

    trans_char_bar_count = px.bar(tty_gr,x="Transaction_Count",y="District",orientation="h",title=f"District wise Transaction Count Split for {state}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                                  height=600)
    st.plotly_chart(trans_char_bar_count)

# map user year
def map_user_year(df,year):
    muy = df[df['Years']== year]
    muy.reset_index(drop=True,inplace=True)

    muy_gr = pd.DataFrame(muy.groupby("States")[["Registered_Users","App_Opens"]].sum())
    muy_gr.reset_index(inplace=True)

    muy_reg_char = px.line(muy_gr,x="States",y=["Registered_Users","App_Opens"],title=f"Registered Users and App Opens Count for {year}",width=1000,height=800,markers=True)

    st.plotly_chart(muy_reg_char)

    return muy

# map user year quarter
def map_user_year_quarter(df,quarter):
    muyq = df[df['Quarter']== quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyq_gr = pd.DataFrame(muyq.groupby("States")[["Registered_Users","App_Opens"]].sum())
    muyq_gr.reset_index(inplace=True)

    muyq_reg_char = px.line(muyq_gr,x="States",y=["Registered_Users","App_Opens"],title=f"Registered Users and App Opens Chart for {df['Years'].min()} {quarter} Quarter",width=1000,height=800,markers=True)

    st.plotly_chart(muyq_reg_char)

    return muyq

# map user year quarter states
def map_user_year_quarter_state(df,state):
    muyqs = df[df['States']== state]
    muyqs.reset_index(drop=True,inplace=True)

    muyqs_gr = pd.DataFrame(muyqs.groupby("District")[["Registered_Users","App_Opens"]].sum())
    muyqs_gr.reset_index(inplace=True)

    muyqs_reg_char = px.bar(muyqs_gr,x="Registered_Users",y="District",orientation="h",title=f"District wise Split for Registered User of {state}",color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(muyqs_reg_char)

    muyqs_app_char = px.bar(muyqs_gr,x="App_Opens",y="District",orientation="h",title=f"District wise Split for App Opens of {state}",color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(muyqs_app_char)

# top insurance pincode
def top_insu_tac_Y_P(df,state):
    tiy = df[df['States']== state]
    tiy.reset_index(drop=True,inplace=True)
    
    tiy_amount_char = px.bar(tiy,x="Quarter",y="Transaction_Amount",title=f"Pincode wise Transaction Amount Split",color_discrete_sequence=px.colors.sequential.Bluered_r,hover_data="Pincodes")
    st.plotly_chart(tiy_amount_char)

    tiy_count_char = px.bar(tiy,x="Quarter",y="Transaction_Count",title=f"Pincode wise Transaction Count Split",color_discrete_sequence=px.colors.sequential.Bluered_r,hover_data="Pincodes")
    st.plotly_chart(tiy_count_char)

def top_user_year(df,year):
    tuy = df[df['Years']== year]
    tuy.reset_index(drop=True,inplace=True)

    tuy_gr = tuy.groupby(["States","Quarter"])[["Registered_Users"]].sum()
    tuy_gr.reset_index(inplace=True)

    tuy_char = px.bar(tuy_gr,x="States",y="Registered_Users",color="Quarter",width=1000,height=800,
                    color_discrete_sequence=px.colors.sequential.thermal_r,hover_name="States",title=f"Registered Users Across States for {year}")

    st.plotly_chart(tuy_char)

    return tuy

# top use year and pincode
def top_user_year_pin(df,state):
    tuys = df[df['States']== state]
    tuys.reset_index(drop=True,inplace=True)

    tuys_char = px.bar(tuys,x="Quarter",y="Registered_Users",color="Registered_Users",width=1000,height=800,hover_data="Pincodes",
                    color_continuous_scale=px.colors.sequential.solar_r,title=f"Registered Users Pincodes Split for {state}")

    st.plotly_chart(tuys_char)

def top_chart_transaction_amount(table_name):
    db = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        port = '5432',
                        database = 'PhonePe',
                        password = '1177')

    cursor = db.cursor()

    q1 = f'''SELECT states, SUM(transaction_amount) AS Transaction FROM {table_name}
            GROUP BY states
            ORDER BY Transaction DESC
            LIMIT 10;'''

    cursor.execute(q1)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("States","Transaction Amount"))
    df_q1_char = px.bar(df_q1,x="States",y="Transaction Amount",title=f"Top 10 States with Highest Transaction Amount on {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                    hover_name="States",height=800,width=1000)
    st.plotly_chart(df_q1_char)

    q2 = f'''SELECT states, SUM(transaction_amount) AS Transaction FROM {table_name}
            GROUP BY states
            ORDER BY Transaction
            LIMIT 10;'''

    cursor.execute(q2)
    table = cursor.fetchall()
    db.commit()

    df_q2 = pd.DataFrame(table,columns=("States","Transaction Amount"))
    df_q2_char = px.bar(df_q2,x="States",y="Transaction Amount",title=f"Top 10 States with Least Transaction Amount on {table_name}",color_discrete_sequence=px.colors.sequential.thermal_r,
                    hover_name="States",height=800,width=1000)
    st.plotly_chart(df_q2_char)

    q3 = f'''SELECT states, AVG(transaction_amount) AS Transaction FROM {table_name}
            GROUP BY states
            ORDER BY Transaction;
            '''

    cursor.execute(q3)
    table = cursor.fetchall()
    db.commit()

    df_q3 = pd.DataFrame(table,columns=("States","Transaction Amount"))
    df_q3_char = px.bar(df_q3,x="Transaction Amount",y="States",title=f"Average Trend of Transaction Amount on {table_name}",color_discrete_sequence=px.colors.sequential.Agsunset_r,
                    hover_name="States",height=800,width=1000,orientation="h")
    st.plotly_chart(df_q3_char)

def top_chart_transaction_count(table_name):
    db = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        port = '5432',
                        database = 'PhonePe',
                        password = '1177')

    cursor = db.cursor()

    q1 = f'''SELECT states, SUM(transaction_count) AS Transaction FROM {table_name}
            GROUP BY states
            ORDER BY Transaction DESC
            LIMIT 10;'''

    cursor.execute(q1)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("States","Transaction Count"))
    df_q1_char = px.bar(df_q1,x="States",y="Transaction Count",title=f"Top 10 States with Highest Transaction Count on {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                    hover_name="States",height=800,width=1000)
    st.plotly_chart(df_q1_char)

    q2 = f'''SELECT states, SUM(transaction_count) AS Transaction FROM {table_name}
            GROUP BY states
            ORDER BY Transaction
            LIMIT 10;'''

    cursor.execute(q2)
    table = cursor.fetchall()
    db.commit()

    df_q2 = pd.DataFrame(table,columns=("States","Transaction Count"))
    df_q2_char = px.bar(df_q2,x="States",y="Transaction Count",title=f"Top 10 States with Least Transaction Count on {table_name}",color_discrete_sequence=px.colors.sequential.thermal_r,
                    hover_name="States",height=800,width=1000)
    st.plotly_chart(df_q2_char)

    q3 = f'''SELECT states, AVG(transaction_count) AS Transaction FROM {table_name}
            GROUP BY states
            ORDER BY Transaction;
            '''

    cursor.execute(q3)
    table = cursor.fetchall()
    db.commit()

    df_q3 = pd.DataFrame(table,columns=("States","Transaction Count"))
    df_q3_char = px.bar(df_q3,x="Transaction Count",y="States",title=f"Average Trend of Transaction Count on {table_name}",color_discrete_sequence=px.colors.sequential.Agsunset_r,
                    hover_name="States",height=800,width=1000,orientation="h")
    st.plotly_chart(df_q3_char)

def top_chart_reg_user(table_name,state):
    db = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        port = '5432',
                        database = 'PhonePe',
                        password = '1177')

    cursor = db.cursor()

    q1 = f'''SELECT district,SUM(registered_user) AS Registered_Users FROM {table_name}
                WHERE states = '{state}'
                GROUP BY district
                ORDER BY Registered_Users DESC
                LIMIT 10
                ;'''

    cursor.execute(q1)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("District","Registered Users"))
    df_q1_char = px.bar(df_q1,x="District",y="Registered Users",title=f"Top 10 Districts with Highest Registered Users on {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                    hover_name="District",height=650,width=600)
    st.plotly_chart(df_q1_char)

    q2 = f'''SELECT district,SUM(registered_user) AS Registered_Users FROM {table_name}
                WHERE states = '{state}'
                GROUP BY district
                ORDER BY Registered_Users
                LIMIT 10;'''

    cursor.execute(q2)
    table = cursor.fetchall()
    db.commit()

    df_q2 = pd.DataFrame(table,columns=("District","Registered Users"))
    df_q2_char = px.bar(df_q2,x="District",y="Registered Users",title=f"Top 10 Districts with Least Registered Users on {table_name}",color_discrete_sequence=px.colors.sequential.thermal_r,
                    hover_name="District",height=650,width=600)
    st.plotly_chart(df_q2_char)

    q3 = f'''SELECT district,SUM(registered_user) AS Registered_Users FROM {table_name}
                WHERE states = '{state}'
                GROUP BY district
                ORDER BY Registered_Users
                ;'''

    cursor.execute(q3)
    table = cursor.fetchall()
    db.commit()

    df_q3 = pd.DataFrame(table,columns=("District","Registered Users"))
    df_q3_char = px.bar(df_q3,x="Registered Users",y="District",title=f"Average Trend of Registered Users on {table_name}",color_discrete_sequence=px.colors.sequential.Agsunset_r,
                    hover_name="District",height=650,width=600,orientation="h")
    st.plotly_chart(df_q3_char)

def top_chart_app_opens_user(table_name,state):
    db = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        port = '5432',
                        database = 'PhonePe',
                        password = '1177')

    cursor = db.cursor()

    q1 = f'''SELECT district,SUM(app_opens) AS App_Opens FROM {table_name}
                WHERE states = '{state}'
                GROUP BY district
                ORDER BY app_opens DESC
                LIMIT 10
                ;'''

    cursor.execute(q1)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("District","App Opens"))
    df_q1_char = px.bar(df_q1,x="District",y="App Opens",title=f"Top 10 Districts with Highest App Opens on {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                    hover_name="District",height=650,width=600)
    st.plotly_chart(df_q1_char)

    q2 = f'''SELECT district,SUM(app_opens) AS App_Opens FROM {table_name}
                WHERE states = '{state}'
                GROUP BY district
                ORDER BY app_opens
                LIMIT 10;'''

    cursor.execute(q2)
    table = cursor.fetchall()
    db.commit()

    df_q2 = pd.DataFrame(table,columns=("District","App Opens"))
    df_q2_char = px.bar(df_q2,x="District",y="App Opens",title=f"Top 10 Districts with Least App Opens on {table_name}",color_discrete_sequence=px.colors.sequential.thermal_r,
                    hover_name="District",height=650,width=600)
    st.plotly_chart(df_q2_char)

    q3 = f'''SELECT district,SUM(app_opens) AS App_Opens FROM {table_name}
                WHERE states = '{state}'
                GROUP BY district
                ORDER BY app_opens
                ;'''

    cursor.execute(q3)
    table = cursor.fetchall()
    db.commit()

    df_q3 = pd.DataFrame(table,columns=("District","App Opens"))
    df_q3_char = px.bar(df_q3,x="App Opens",y="District",title=f"Average Trend of App Opens on {table_name}",color_discrete_sequence=px.colors.sequential.Agsunset_r,
                    hover_name="District",height=650,width=600,orientation="h")
    st.plotly_chart(df_q3_char)

def top_chart_reg_user_map(table_name):
    db = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        port = '5432',
                        database = 'PhonePe',
                        password = '1177')

    cursor = db.cursor()

    q1 = f'''SELECT states,SUM(registered_users) AS registered_users FROM {table_name}
                GROUP BY states
                ORDER BY registered_users DESC
                LIMIT 10;'''

    cursor.execute(q1)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("States","Registered Users"))
    df_q1_char = px.bar(df_q1,x="States",y="Registered Users",title=f"Top 10 States with Highest Registered Users on {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                    hover_name="States",height=650,width=600)
    st.plotly_chart(df_q1_char)

    q2 = f'''SELECT states,SUM(registered_users) AS registered_users FROM {table_name}
                GROUP BY states
                ORDER BY registered_users
                LIMIT 10;'''

    cursor.execute(q2)
    table = cursor.fetchall()
    db.commit()

    df_q2 = pd.DataFrame(table,columns=("States","Registered Users"))
    df_q2_char = px.bar(df_q2,x="States",y="Registered Users",title=f"Top 10 States with Least Registered Users on {table_name}",color_discrete_sequence=px.colors.sequential.thermal_r,
                    hover_name="States",height=650,width=600)
    st.plotly_chart(df_q2_char)

    q3 = f'''SELECT states,AVG(registered_users) AS registered_users FROM {table_name}
                GROUP BY states
                ORDER BY registered_users
                ;'''

    cursor.execute(q3)
    table = cursor.fetchall()
    db.commit()

    df_q3 = pd.DataFrame(table,columns=("States","Registered Users"))
    df_q3_char = px.bar(df_q3,x="Registered Users",y="States",title=f"Average Trend of Registered Users on {table_name}",color_discrete_sequence=px.colors.sequential.Agsunset_r,
                    hover_name="States",height=650,width=600,orientation="h")
    st.plotly_chart(df_q3_char)

def top_chart_transaction_type(table_name,transaction_type):
    db = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                         port = '5432',
                        database = 'PhonePe',
                        password = '1177')

    cursor = db.cursor()

    q1 = f'''SELECT states,SUM(transaction_amount) AS total_amount FROM {table_name}
                WHERE transaction_type = '{transaction_type}'
                GROUP BY states
                ORDER BY total_amount DESC
                LIMIT 5;
                '''

    cursor.execute(q1)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("States","Transaction Amount"))
    df_q1_char = px.bar(df_q1,x="States",y="Transaction Amount",title=f"Top 5 States with thier respective transaction types",color_discrete_sequence=px.colors.sequential.Bluered_r,
                    hover_name="States",height=650,width=600)
    st.plotly_chart(df_q1_char)

def top_chart_district(table_name):
    db = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                         port = '5432',
                        database = 'PhonePe',
                        password = '1177')

    cursor = db.cursor()

    q1 = f'''SELECT district,states,SUM(transaction_amount) AS total_transaction
                FROM {table_name}
                GROUP BY district,states
                ORDER BY total_transaction DESC
                LIMIT 10;
                '''

    cursor.execute(q1)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("District","States","Transaction Amount"))
    df_q1_char = px.bar(df_q1,x="District",y="Transaction Amount",title=f"Top 10 Districts with Highest Transaction on {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                    hover_name="States",height=800,width=800)
    st.plotly_chart(df_q1_char)

    q2 = f'''SELECT district,states,SUM(transaction_amount) AS total_transaction
                FROM {table_name}
                GROUP BY district,states
                ORDER BY total_transaction
                LIMIT 10;
                '''

    cursor.execute(q2)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("District","States","Transaction Amount"))
    df_q1_char = px.bar(df_q1,x="District",y="Transaction Amount",title=f"Top 10 Districts with Least Transaction on {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,
                    hover_name="States",height=800,width=800)
    st.plotly_chart(df_q1_char)

def top_chart_brands(table_name):
    db = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                         port = '5432',
                        database = 'PhonePe',
                        password = '1177')

    cursor = db.cursor()

    q1 = f'''SELECT
                states,
                brands,
                total_transaction
            FROM (
                SELECT
                    states,
                    brands,
                    SUM(transaction_count) AS total_transaction,
                    ROW_NUMBER() OVER (PARTITION BY states ORDER BY SUM(transaction_count) DESC) AS rank
                FROM
                    {table_name}
                GROUP BY
                    states, brands
            ) ranked_data
            WHERE rank = 1
            ORDER BY total_transaction DESC;

                            '''

    cursor.execute(q1)
    table = cursor.fetchall()
    db.commit()

    df_q1 = pd.DataFrame(table,columns=("States","brands","Total Transaction"))
    df_q1_char = px.bar(df_q1,x="States",y="Total Transaction",title=f"Top Phone Brand of the respective states",color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    hover_name="brands",height=800,width=800,color="brands")
    st.plotly_chart(df_q1_char)
    

#streamlit part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
t1,t2,t3 = st.tabs(["Home","Data Exploration","Top Charts"])

image = Image.open("C:/Users/Shafa/Downloads/PhonePe Logo _ 01 - PNG Logo Vector Brand Downloads (SVG, EPS).jpg")
image_1 = Image.open("C:/Users/Shafa/Downloads/Phonepe_ep.jpg")
with t1:
    st.title("About")
    st.write("PhonePe is one of India's leading digital payment platforms, offering a seamless and user-friendly experience for managing your finances."
              "Launched in 2015 and based in Bengaluru, it allows users to make a variety of transactions such as sending money, paying bills, recharging mobiles, and even shopping online."
              "With the introduction of the Unified Payments Interface (UPI), PhonePe has made these services accessible in multiple Indian languages, broadening its reach across the country.")
    
    st.image(image)
    st.title("Understanding the Terminologies:")
    st.subheader("Aggregated Data:")
    st.write("Aggregated data represents the country-level information that is further broken down into detailed insights at the state level."
              "This provides a comprehensive overview of national trends while allowing for in-depth analysis of individual states. And also gives us the transaction types used to make the transactions")
    st.subheader("Map Data:")
    st.write("Map data focuses on state-level information, segmented into districts." 
             "This hierarchical structure enables a detailed examination of each state's performance across its various districts, offering a clearer picture of regional dynamics.")
    st.subheader("Top Data:")
    st.write("Top data refers to the district-level information, further divided into specific pin codes or areas."
              "This granular approach allows for precise analysis and understanding of localized trends and activities within each district.")
    st.image(image_1)
    
with t2:
    tab1,tab2,tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        method_agg = st.radio("Select The Method:",["Aggregated Insurance Analysis","Aggregated Transaction Analysis","Aggregated User Analysis"])
        if method_agg ==  "Aggregated Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year:",aggregated_insurance['Years'].unique())
            tac_Y =Transaction_amount_count_year(aggregated_insurance,years)
            with col2:
                quarters = st.selectbox("Select The Quarter:",tac_Y['Quarter'].unique())
            Transaction_amount_count_quarter(tac_Y,quarters)
        elif method_agg == "Aggregated Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year:",aggregated_transaction['Years'].unique())
            agg_trans_tac_Y =Transaction_amount_count_year(aggregated_transaction,years)
            col1,col2 = st.columns(2)
            with col1:
                st.header("Transaction Type Split")    
                states = st.selectbox("Select The State:",agg_trans_tac_Y['States'].unique())
            aggregated_Transaction_type(agg_trans_tac_Y,states)
            col1,col2 = st.columns(2)
            with col1:
                st.header("Quarter Split")
                quarters = st.selectbox("Select The Quarter:",agg_trans_tac_Y['Quarter'].unique())
            aggre_trans_tac_Y_Q = Transaction_amount_count_quarter(agg_trans_tac_Y,quarters)
            with col2:
                st.header("Transaction Type Split Based On Quarter")
                states = st.selectbox("Select The State For Quarter Split:",aggre_trans_tac_Y_Q['States'].unique())
            aggregated_Transaction_type(aggre_trans_tac_Y_Q,states)




        elif method_agg == "Aggregated User Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year:",aggregated_user['Years'].unique())
                agg_user_Y =aggregated_user_year(aggregated_user,years)
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter:",agg_user_Y['Quarter'].unique())
                aggre_user_Y_Q = aggregated_user_year_quarter(agg_user_Y,quarters)
            col1,col2 = st.columns(2)
            with col1:    
        
                states = st.selectbox("Select The State:",aggre_user_Y_Q['States'].unique())
                aggre_user_Y_Q_S = aggregated_user_year_quarter_states(aggre_user_Y_Q,states)

    with tab2:
        method_map = st.radio("Select The Method:",["Map Insurance Analysis","Map Transaction Analysis","Map User Analysis"])
        if method_map ==  "Map Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year for State Split:",map_insurance['Years'].unique())
            map_ins_Y = Transaction_amount_count_year(map_insurance,years)
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for District Split:",map_ins_Y['States'].unique())
            map_ins_dist(map_ins_Y,states)
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter for State wise Split:",map_ins_Y['Quarter'].unique())
            map_ins_Y_Q = Transaction_amount_count_quarter(map_ins_Y,quarters)
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for Quarter wise Split:",map_ins_Y_Q['States'].unique())
            map_ins_dist(map_ins_Y_Q,states)





        elif method_map == "Map Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year for State Transaction Split:",map_transaction['Years'].unique())
            map_trans_Y = Transaction_amount_count_year(map_transaction,years)
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for District Split:",map_trans_Y['States'].unique())
            map_ins_dist(map_trans_Y,states)
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter for State wise Split:",map_trans_Y['Quarter'].unique())
            map_trans_Y_Q = Transaction_amount_count_quarter(map_trans_Y,quarters)
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for Quarter wise Split:",map_trans_Y_Q['States'].unique())
            map_ins_dist(map_trans_Y_Q,states)




        elif method_map == "Map User Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year for State's Registered Users and App Opens:",map_user['Years'].unique())
            map_user_Y = map_user_year(map_user,years)
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter for State's Registered Users and App Opens:",map_user_Y['Quarter'].unique())
            map_user_Y_Q = map_user_year_quarter(map_user_Y,quarters)
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for District's Registered Users and App Opens:",map_user_Y_Q['States'].unique())
            map_user_year_quarter_state(map_user_Y_Q,states)




    with tab3:
        method_top = st.radio("Select The Method:",["Top Insurance Analysis","Top Transaction Analysis","Top User Analysis"])
        if method_top ==  "Top Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year for Top Insurance Metrics:",top_insurance['Years'].unique())
            top_ins_Y = Transaction_amount_count_year(top_insurance,years)
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for Top Insurance Metrics:",top_ins_Y['States'].unique())
            top_ins_Y_P = top_insu_tac_Y_P(top_ins_Y,states)
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter for Top Insurance Metrics:",top_ins_Y['Quarter'].unique())
            top_ins_Y_Q = Transaction_amount_count_quarter(top_ins_Y,quarters)
            col1,col2 = st.columns(2)
            
            

        
        
        elif method_top == "Top Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year for Top Transaction Metrics:",top_transaction['Years'].unique())
            top_trans_Y = Transaction_amount_count_year(top_transaction,years)
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for Top Transaction Metrics:",top_trans_Y['States'].unique())
            top_ins_Y_P = top_insu_tac_Y_P(top_trans_Y,states)
            col1,col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("Select The Quarter for Top Transaction Metrics:",top_trans_Y['Quarter'].unique())
            top_ins_Y_Q = Transaction_amount_count_quarter(top_trans_Y,quarters)
            col1,col2 = st.columns(2)
            



        elif method_top == "Top User Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.selectbox("Select The Year for Top Users Metrics:",top_user['Years'].unique())
            top_user_Y = top_user_year(top_user,years)
            col1,col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State for Top Users Metrics:",top_user_Y['States'].unique())
            top_user_Y_P = top_user_year_pin(top_user_Y,states)

            
with t3:
    question = st.selectbox("Select The Question",["1. Transaction Summary of Aggregated Insurance.",
                                        "2. Transaction Summary of Map Insurance.",
                                        "3. Transaction Summary of Top Insurance.",
                                        "4. Transaction Summary of Aggregated Transaction.",
                                        "5. Transaction Summary of Map Transaction.",
                                        "6. Transaction Summary of Top Transaction.",
                                        "7. Transaction Summary of Aggregated User.",
                                        "8. Number of Registered Users on District level.",
                                        "9. Number of App Opens on District level.",
                                        "10. Number of Registered Users on State level.",
                                        "11. Top 5 States with thier respective transaction types.",
                                        "12. District level Transaction Summary.",
                                        "13. Top Phone Brands across states"])
    
    if question == "1. Transaction Summary of Aggregated Insurance.":

        st.subheader("Transaction Amount Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction amount and also the average Transaction trend")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("Transaction Count Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction counts and also the average Transaction trend")
        top_chart_transaction_count("aggregated_insurance")
    
    elif question == "2. Transaction Summary of Map Insurance.":

        st.subheader("Transaction Amount Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction amount and also the average Transaction trend")
        top_chart_transaction_amount("map_insurance")
        st.subheader("Transaction Count Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction counts and also the average Transaction trend")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Summary of Top Insurance.":

        st.subheader("Transaction Amount Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction amount and also the average Transaction trend")
        top_chart_transaction_amount("top_insurance")
        st.subheader("Transaction Count Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction counts and also the average Transaction trend")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Summary of Aggregated Transaction.":

        st.subheader("Transaction Amount Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction amount and also the average Transaction trend")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("Transaction Count Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction counts and also the average Transaction trend")
        top_chart_transaction_count("aggregated_transaction")
    
    elif question == "5. Transaction Summary of Map Transaction.":

        st.subheader("Transaction Amount Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction amount and also the average Transaction trend")
        top_chart_transaction_amount("map_transaction")
        st.subheader("Transaction Count Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction counts and also the average Transaction trend")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Summary of Top Transaction.":

        st.subheader("Transaction Amount Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction amount and also the average Transaction trend")
        top_chart_transaction_amount("top_transaction")
        st.subheader("Transaction Count Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction counts and also the average Transaction trend")
        top_chart_transaction_count("top_transaction")
    
    elif question == "7. Transaction Summary of Aggregated User.":

        st.subheader("Transaction Count Metrics:")
        st.write("This data represents the Top 10 states with the most and the least transaction counts and also the average Transaction trend")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Number of Registered Users on District level.":
        
        st.subheader("Registered Users Metrics")
        state = st.selectbox("Select The State",map_user['States'].unique())
        top_chart_reg_user("map_user",state)
    
    elif question == "9. Number of App Opens on District level.":

        st.subheader("App Openings Metrics")
        state = st.selectbox("Select The State",map_user["States"].unique())
        top_chart_app_opens_user("map_user",state)
    
    elif question == "10. Number of Registered Users on State level.":

        st.subheader("Registered Users Metrics")
        top_chart_reg_user_map("top_user")

    elif question == "11. Top 5 States with thier respective transaction types.":

        st.subheader("Top 5 States of the respective transaction type")
        transaction_type = st.selectbox("Select The Transaction Type",aggregated_transaction['Transaction_Type'].unique())
        top_chart_transaction_type("aggregated_transaction",transaction_type)
    
    elif question ==  "12. District level Transaction Summary":
        st.subheader("Transaction Amount Metrics:")
        st.write("This data represents the Top 10 Districts with the most and the least transaction amount")
        top_chart_district("map_transaction")

    elif question == "13. Phone Brands used to make transactions across states":
        st.subheader("Phone Brands and thier market dominance")
        st.write("This data represents the phone brands which comes first on making higher number of transactions in that respective state.")
        top_chart_brands("aggregated_user")






